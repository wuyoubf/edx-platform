"""
Course API Serializers.  Representing course catalog data
"""

import urllib

from django.core.urlresolvers import reverse
from django.template import defaultfilters

from rest_framework import serializers

from lms.djangoapps.courseware.courses import get_course_about_section
from openedx.core.lib.courses import course_image_url
from openedx.core.djangoapps.models.course_details import CourseDetails
from xmodule.course_module import DEFAULT_START_DATE


class _MediaSerializer(serializers.Serializer):  # pylint: disable=abstract-method
    """
    Nested serializer to represent a media object.
    """
    def __init__(self, uri_parser, *args, **kwargs):
        super(_MediaSerializer, self).__init__(*args, **kwargs)
        self.uri_parser = uri_parser

    uri = serializers.SerializerMethodField(source='*')

    def get_uri(self, course):
        """
        Get the representation for the media resource's URI
        """
        return self.uri_parser(course)


class _CourseApiMediaCollectionSerializer(serializers.Serializer):  # pylint: disable=abstract-method
    """
    Nested serializer to represent a collection of media objects
    """
    course_image = _MediaSerializer(source='*', uri_parser=course_image_url)
    course_video = _MediaSerializer(
        source='*',
        uri_parser=lambda course: CourseDetails.fetch_video_url(course.id),
    )


class CourseSerializer(serializers.Serializer):  # pylint: disable=abstract-method
    """
    Serializer for Course objects
    """

    course_id = serializers.CharField(source='id', read_only=True)
    name = serializers.CharField(source='display_name_with_default')
    number = serializers.CharField(source='display_number_with_default')
    org = serializers.CharField(source='display_org_with_default')
    short_description = serializers.SerializerMethodField()
    effort = serializers.SerializerMethodField()

    media = _CourseApiMediaCollectionSerializer(source='*')

    start = serializers.DateTimeField()
    start_type = serializers.SerializerMethodField()
    start_display = serializers.SerializerMethodField()
    end = serializers.DateTimeField()

    enrollment_start = serializers.DateTimeField()
    enrollment_end = serializers.DateTimeField()

    blocks_url = serializers.SerializerMethodField()

    def get_start_type(self, course):
        """
        Get the representation for SerializerMethodField `start_type`
        """
        if course.advertised_start is not None:
            return u'string'
        elif course.start != DEFAULT_START_DATE:
            return u'timestamp'
        else:
            return u'empty'

    def get_start_display(self, course):
        """
        Get the representation for SerializerMethodField `start_display`
        """
        if course.advertised_start is not None:
            return course.advertised_start
        elif course.start != DEFAULT_START_DATE:
            return defaultfilters.date(course.start, "DATE_FORMAT")
        else:
            return None

    def get_short_description(self, course):
        """
        Get the representation for SerializerMethodField `short_description`
        """
        return get_course_about_section(self.context['request'], course, 'short_description').strip()

    def get_blocks_url(self, course):
        """
        Get the representation for SerializerMethodField `blocks_url`
        """
        base_url = '?'.join([
            reverse('blocks_in_course'),
            urllib.urlencode({'course_id': course.id}),
        ])
        return self.context['request'].build_absolute_uri(base_url)

    def get_effort(self, course):
        """
        Get the representation for SerializerMethodField `effort`
        """
        return CourseDetails.fetch_effort(course.id)
