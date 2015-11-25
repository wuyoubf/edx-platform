"""
This tests that the completion XBlock correctly stores state. This
is a fairly simple XBlock, and a correspondingly simple test suite.
"""

import json
import unittest

from django.conf import settings
from django.core.urlresolvers import reverse

from xmodule.modulestore.tests.factories import CourseFactory, ItemFactory
from xmodule.modulestore.tests.django_utils import SharedModuleStoreTestCase

from lms.djangoapps.courseware.tests.helpers import LoginEnrollmentTestCase
from lms.djangoapps.courseware.tests.factories import GlobalStaffFactory
from lms.djangoapps.lms_xblock.runtime import quote_slashes


class TestRate(SharedModuleStoreTestCase, LoginEnrollmentTestCase):
    """
    Simple tests for the completion XBlock. We set up a page with two
    of the block, make sure the page renders, toggle them a few times,
    make sure they've toggled, and reconfirm the page renders.
    """
    STUDENTS = [
        {'email': 'view@test.com', 'password': 'foo'},
        {'email': 'view2@test.com', 'password': 'foo'}
    ]

    @classmethod
    def setUpClass(cls):
        """
        Create a page with two of the XBlock on it
        """
        # Nose runs setUpClass methods even if a class decorator says to skip
        # the class: https://github.com/nose-devs/nose/issues/946
        # So, skip the test class here if we are not in the LMS.
        if settings.ROOT_URLCONF != 'lms.urls':
            raise unittest.SkipTest('Test only valid in lms')

        super(TestRate, cls).setUpClass()
        cls.course = CourseFactory.create(
            display_name='Rate_Test_Course'
        )
        with cls.store.bulk_operations(cls.course.id, emit_signals=False):
            cls.chapter = ItemFactory.create(
                parent=cls.course, display_name='Overview'
            )
            cls.section = ItemFactory.create(
                parent=cls.chapter, display_name='Welcome'
            )
            cls.unit = ItemFactory.create(
                parent=cls.section, display_name='New Unit'
            )
            cls.xblock1 = ItemFactory.create(
                parent=cls.unit,
                category='rate',
                display_name='rate_0'
            )
            cls.xblock2 = ItemFactory.create(
                parent=cls.unit,
                category='rate',
                display_name='rate_1'
            )

        cls.course_url = reverse(
            'courseware_section',
            kwargs={
                'course_id': cls.course.id.to_deprecated_string(),
                'chapter': 'Overview',
                'section': 'Welcome',
            }
        )

    def setUp(self):
        """
        Create users
        """
        super(TestRate, self).setUp()
        for idx, student in enumerate(self.STUDENTS):
            username = "u{}".format(idx)
            self.create_account(username, student['email'], student['password'])
            self.activate_user(student['email'])

        self.staff_user = GlobalStaffFactory()

    def get_handler_url(self, handler, xblock_name=None):
        """
        Get url for the specified xblock handler
        """
        return reverse('xblock_handler', kwargs={
            'course_id': self.course.id.to_deprecated_string(),
            'usage_id': quote_slashes(self.course.id.make_usage_key('rate', xblock_name).to_deprecated_string()),
            'handler': handler,
            'suffix': ''
        })

    def login_student(self, student):
        """
        Student login and enroll for the course
        """
        self.login(student['email'], student['password'])

    def login_staff(self):
        """
        Staff login and enroll for the course
        """
        email = self.staff_user.email
        password = 'test'
        self.login(email, password)

    def check_ajax(self, block, data, desired_state):
        """
        Make an AJAX call to the XBlock, and assert the state is as
        desired.
        """
        url = self.get_handler_url('feedback', 'rate_' + str(block))
        resp = self.client.post(url, json.dumps(data), '')
        resp_data = json.loads(resp.content)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp_data, desired_state)
        return resp_data

    def test_rate(self):
        """
        We would like to confirm the rater XBlock correctly aggregates
        date from many users, and can handle votes with and without
        feedback submissions. This is a test which has two positive
        votes, one negative vote, and then a swap from positive to
        negative. We confirm student state is maintained, and that
        the final counts are accurate. This tests essentially all of
        the block's functionality.
        """
        # Enroll students
        self.login_student(self.STUDENTS[0])
        self.enroll(self.course, verify=True)
        self.login_student(self.STUDENTS[1])
        self.enroll(self.course, verify=True)
        self.login_staff()
        self.enroll(self.course, verify=True)

        # We confirm we don't have errors rendering the student view
        self.assert_request_status_code(200, self.course_url)

        # We confirm the block is initialized correctly
        # All zeros for aggregate would also be sensible
        request = {}
        expected_response = {
            u'aggregate': None,
            u'freeform': u'',
            u'response': u'Please vote!',
            u'success': False,
            u'vote': -1
        }
        self.check_ajax(0, request, expected_response)

        # Staff votes up #4 and submits feedback
        request = {'vote': 4,
                   'freeform': 'Yay!'}
        expected_response = {
            u'aggregate': [0, 0, 0, 0, 1],
            u'freeform': u'Yay!',
            u'response': u'Thank you for voting!',
            u'success': True,
            u'vote': 4
        }
        self.check_ajax(0, request, expected_response)

        # Student 1 upvotes submitting feedback
        self.login_student(self.STUDENTS[0])
        request = {'vote': 4,
                   'freeform': 'Yes!'}
        expected_response = {
            u'freeform': u'Yes!',
            u'response': u'Thank you for voting!',
            u'success': True,
            u'vote': 4
        }
        self.check_ajax(0, request, expected_response)

        # Student 2 downvotes without submitting feedback
        self.login_student(self.STUDENTS[1])
        request = {'vote': 0}
        expected_response = {
            u'freeform': '',
            u'response': u'Thank you for voting!',
            u'success': True,
            u'vote': 0
        }
        self.check_ajax(0, request, expected_response)

        # Staff downvotes without submitting feedback
        # We confirm aggregate votes, as well as old feedback as staff
        self.login_staff()
        request = {'vote': 0}
        expected_response = {
            u'aggregate': [2, 0, 0, 0, 1],
            u'freeform': u'Yay!',
            u'response': u'Thank you for voting!',
            u'success': True,
            u'vote': 0
        }
        self.check_ajax(0, request, expected_response)

        # We reconfirm we don't have errors rendering the student view
        self.assert_request_status_code(200, self.course_url)
