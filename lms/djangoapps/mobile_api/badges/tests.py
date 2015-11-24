"""
Tests for the badges API views.
"""
from django.conf import settings
from django.test.utils import override_settings

from badges.tests.factories import BadgeAssertionFactory, BadgeClassFactory, RandomBadgeClassFactory
from util.testing import UrlResetMixin
from xmodule.modulestore.tests.factories import CourseFactory
from ..testutils import MobileAPITestCase, MobileAuthUserTestMixin


FEATURES_WITH_BADGES_ENABLED = settings.FEATURES.copy()
FEATURES_WITH_BADGES_ENABLED['ENABLE_OPENBADGES'] = True


class UserAssertionMixin(object):
    """
    Mixin for badge API tests.
    """
    WILDCARD = False

    def setUp(self, **kwargs):
        super(UserAssertionMixin, self).setUp('mobile_api.urls', **kwargs)

    def check_class_structure(self, badge_class, json_class):
        """
        Check a JSON response against a known badge class.
        """
        self.assertEqual(badge_class.issuing_component, json_class['issuing_component'])
        self.assertEqual(badge_class.slug, json_class['slug'])
        self.assertIn(badge_class.image.url, json_class['image'])
        self.assertEqual(badge_class.description, json_class['description'])
        self.assertEqual(badge_class.criteria, json_class['criteria'])
        self.assertEqual(badge_class.course_id and unicode(badge_class.course_id), json_class['course_id'])

    def check_assertion_structure(self, assertion, json_assertion):
        """
        Check a JSON response against a known assertion object.
        """
        self.assertEqual(assertion.image_url, json_assertion['image_url'])
        self.assertEqual(assertion.assertion_url, json_assertion['assertion_url'])
        self.assertTrue(json_assertion['user'].startswith('http'))
        self.check_class_structure(assertion.badge_class, json_assertion['badge_class'])

    def get_course_id(self, badge_class):
        """
        Used for tests which may need to test for a course_id or a wildcard.
        """
        if self.WILDCARD:
            return '*'
        else:
            return unicode(badge_class.course_id)

    def create_badge_class(self, **kwargs):
        """
        Create a badge class, using a course id if it's relevant to the URL pattern.
        """
        if 'course_id' in self.REVERSE_INFO['params']:
            return RandomBadgeClassFactory.create(course_id=self.course.location.course_key, **kwargs)
        return RandomBadgeClassFactory.create(**kwargs)

    def get_reverse_args(self, badge_class):
        """
        Get the reverse args for a URL lookup based on class settings.
        """
        reverse_args = {
            'issuing_component': badge_class.issuing_component,
            'slug': badge_class.slug,
        }
        if 'course_id' in self.REVERSE_INFO['params']:
            reverse_args['course_id'] = self.get_course_id(badge_class)
        return reverse_args


@override_settings(FEATURES=FEATURES_WITH_BADGES_ENABLED)
class TestUserBadgeAssertions(UserAssertionMixin, UrlResetMixin, MobileAPITestCase, MobileAuthUserTestMixin):
    """
    Test the general badge assertions retrieval view.
    """
    REVERSE_INFO = {'name': 'user-assertions', 'params': ['username']}

    def test_get_assertions(self):
        """
        Verify we can get all of a user's badge assertions.
        """
        self.login()
        for dummy in range(3):
            BadgeAssertionFactory(user=self.user)
        # Add in a course scoped badge-- these should not be excluded from the full listing.
        BadgeAssertionFactory(user=self.user, badge_class=BadgeClassFactory(course_id=self.course.location.course_key))
        # Should not be included.
        for dummy in range(3):
            self.create_badge_class()
        response = self.api_response(username=self.user.username, expected_response_code=200)
        # pylint: disable=no-member
        self.assertEqual(len(response.data['results']), 4)

    def test_assertion_structure(self):
        self.login()
        badge_class = self.create_badge_class()
        assertion = BadgeAssertionFactory.create(user=self.user, badge_class=badge_class)
        response = self.api_response(username=self.user.username, expected_response_code=200)
        # pylint: disable=no-member
        self.check_assertion_structure(assertion, response.data['results'][0])


@override_settings(FEATURES=FEATURES_WITH_BADGES_ENABLED)
class TestUserCourseBadgeAssertions(UserAssertionMixin, UrlResetMixin, MobileAPITestCase, MobileAuthUserTestMixin):
    """
    Test the Badge Assertions view with the course_id filter.
    """
    REVERSE_INFO = {'name': 'user-course-assertions', 'params': ['username', 'course_id']}

    def test_get_assertions(self):
        """
        Verify we can get assertions via the course_id and username.
        """
        self.login()
        course_key = self.course.location.course_key
        badge_class = BadgeClassFactory.create(course_id=course_key)
        for dummy in range(3):
            BadgeAssertionFactory.create(user=self.user, badge_class=badge_class)
        # Should not be included.
        for dummy in range(3):
            BadgeAssertionFactory.create(user=self.user)
        # Also should not be included
        for dummy in range(6):
            BadgeAssertionFactory.create(badge_class=badge_class)
        response = self.api_response(username=self.user.username, course_id=course_key)
        # pylint: disable=no-member
        self.assertEqual(len(response.data['results']), 3)
        unused_course = CourseFactory.create()
        response = self.api_response(username=self.user.username, course_id=unused_course.location.course_key)
        # pylint: disable=no-member
        self.assertEqual(len(response.data['results']), 0)

    def test_assertion_structure(self):
        """
        Verify the badge assertion structure is not mangled in this mode.
        """
        self.login()
        course_key = self.course.location.course_key
        badge_class = BadgeClassFactory.create(course_id=course_key)
        assertion = BadgeAssertionFactory.create(badge_class=badge_class, user=self.user)
        response = self.api_response(username=self.user.username, expected_response_code=200)
        # pylint: disable=no-member
        self.check_assertion_structure(assertion, response.data['results'][0])


@override_settings(FEATURES=FEATURES_WITH_BADGES_ENABLED)
class TestUserBadgeAssertionsByClass(UserAssertionMixin, UrlResetMixin, MobileAPITestCase):
    """
    Test the Badge Assertions view with the badge class filter.
    """
    REVERSE_INFO = {'name': 'user-class-assertions', 'params': ['username', 'issuing_component', 'slug']}

    def test_get_assertions(self):
        """
        Verify we can get assertions via the badge class and username.
        """
        self.login()
        badge_class = self.create_badge_class()
        for dummy in range(3):
            BadgeAssertionFactory.create(user=self.user, badge_class=badge_class)
        if badge_class.course_id:
            # Also create a version of this badge under a different course.
            alt_class = BadgeClassFactory.create(
                slug=badge_class.slug, issuing_component=badge_class.issuing_component,
                course_id=CourseFactory.create().location.course_key
            )
            BadgeAssertionFactory.create(user=self.user, badge_class=alt_class)
        # Should not be in list.
        for dummy in range(5):
            BadgeAssertionFactory.create(badge_class=badge_class)
        # Also should not be in list.
        for dummy in range(6):
            BadgeAssertionFactory.create()

        response = self.api_response(
            username=self.user.username,
            reverse_args=self.get_reverse_args(badge_class),
            expected_response_code=200,
        )
        if self.WILDCARD:
            expected_length = 4
        else:
            expected_length = 3
        # pylint: disable=no-member
        self.assertEqual(len(response.data['results']), expected_length)
        unused_class = self.create_badge_class(slug='unused_slug', issuing_component='unused_component')

        response = self.api_response(
            username=self.user.username,
            reverse_args=self.get_reverse_args(unused_class),
            expected_response_code=200,
        )
        # pylint: disable=no-member
        self.assertEqual(len(response.data['results']), 0)

    def check_badge_class_assertion(self, badge_class):
        """
        Given a badge class, create an assertion for the current user and fetch it, checking the structure.
        """
        assertion = BadgeAssertionFactory.create(badge_class=badge_class, user=self.user)
        response = self.api_response(
            username=self.user.username,
            reverse_args=self.get_reverse_args(badge_class),
            expected_response_code=200
        )
        # pylint: disable=no-member
        self.check_assertion_structure(assertion, response.data['results'][0])

    def test_assertion_structure(self):
        self.login()
        self.check_badge_class_assertion(self.create_badge_class())

    def test_empty_issuing_component(self):
        self.login()
        self.check_badge_class_assertion(self.create_badge_class(issuing_component=''))


# pylint: disable=test-inherits-tests
class TestUserBadgeAssertionsByClassCourse(TestUserBadgeAssertionsByClass):
    """
    Test searching all assertions for a user with a course bound badge class.
    """
    REVERSE_INFO = {'name': 'user-class-assertions', 'params': ['username', 'issuing_component', 'slug', 'course_id']}


# pylint: disable=test-inherits-tests
class TestUserBadgeAssertionsByClassWildCard(TestUserBadgeAssertionsByClassCourse):
    """
    Test searching slugs/issuing_components across all course IDs.
    """
    WILDCARD = True


@override_settings(FEATURES=FEATURES_WITH_BADGES_ENABLED)
class TestBadgeClass(UserAssertionMixin, UrlResetMixin, MobileAPITestCase):
    """
    Test the badge class view.
    """
    REVERSE_INFO = {'name': 'badge_class-detail', 'params': ['issuing_component', 'slug']}

    def test_get_badge_class(self):
        """
        Test fetching a badge class.
        """
        badge_class = self.create_badge_class()
        self.get_reverse_args(badge_class)
        response = self.api_response(
            reverse_args=self.get_reverse_args(badge_class),
            expected_response_code=200
        )
        # pylint: disable=no-member
        self.check_class_structure(badge_class, response.data)


# pylint: disable=test-inherits-tests
class TestBadgeClassCourseSet(TestBadgeClass):
    """
    Test searching by course-bound badge class.
    """
    REVERSE_INFO = {'name': 'badge_class-detail', 'params': ['issuing_component', 'slug', 'course_id']}
