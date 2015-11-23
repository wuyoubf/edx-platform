"""
Convenience methods for working with course objects
"""
from django.http import Http404
from opaque_keys import InvalidKeyError
from opaque_keys.edx.keys import CourseKey


def from_string_or_404(course_key_string):
    """
    Parses course key from string(containing course key) or raises 404 if the string's format is invalid.
    :param course_key_string: it is string containing the course key
    :return: course key
    :raises: 404 not found error
    """
    try:
        course_key = CourseKey.from_string(course_key_string)
    except InvalidKeyError:
        raise Http404

    return course_key
