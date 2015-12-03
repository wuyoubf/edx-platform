"""
Serializers for Bookmarks.
"""
from rest_framework import serializers

from . import DEFAULT_FIELDS
from .models import Bookmark


class BookmarkSerializer(serializers.ModelSerializer):
    """
    Serializer for the Bookmark model.
    """
    id = serializers.Field(source='resource_id')  # pylint: disable=invalid-name
    course_id = serializers.Field(source='course_key')
    usage_id = serializers.Field(source='usage_key')
    block_type = serializers.Field(source='usage_key.block_type')
    display_name = serializers.Field(source='display_name')
    path = serializers.SerializerMethodField('path_data')

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        try:
            fields = kwargs['context'].pop('fields', DEFAULT_FIELDS) or DEFAULT_FIELDS
        except KeyError:
            fields = DEFAULT_FIELDS
        # Instantiate the superclass normally
        super(BookmarkSerializer, self).__init__(*args, **kwargs)

        # Drop any fields that are not specified in the `fields` argument.
        required_fields = set(fields)
        all_fields = set(self.fields.keys())
        for field_name in all_fields - required_fields:
            self.fields.pop(field_name)

    class Meta(object):
        """ Serializer metadata. """
        model = Bookmark
        fields = (
            'id',
            'course_id',
            'usage_id',
            'block_type',
            'display_name',
            'path',
            'created',
        )

    def resource_id(self, bookmark):
        """
        Return the REST resource id: {username,usage_id}.
        """
        return "{0},{1}".format(bookmark.user.username, bookmark.usage_key)

    def path_data(self, bookmark):
        """
        Serialize and return the path data of the bookmark.
        """
        return [path_item._asdict() for path_item in bookmark.path]
