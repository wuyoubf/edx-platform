"""
:class:`~django_require.staticstorage.OptimizedCachedRequireJsStorage`
"""

from pipeline.storage import PipelineCachedStorage
from require.storage import OptimizedFilesMixin


class OptimizedCachedRequireJsStorage(PipelineCachedStorage, OptimizedFilesMixin):
    """
    Custom storage backend that is used by Django-require.
    """
    pass
