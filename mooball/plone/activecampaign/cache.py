import time
import plone.memoize.volatile


class PurgableCleanupDict(plone.memoize.volatile.CleanupDict):
    """
    A cache storage which can be purged by setting a value with the key
    ``-1``

        >>> d = PurgableCleanupDict()
        >>> d['foo'] = 'bar'
        >>> d['foo']
        'bar'

    The '-1' key purges the dict and therefore the cache storage:

        >>> d['foo:-1'] = 'ignored'
        >>> d['foo:-1'] # doctest: +ELLIPSIS
        Traceback (most recent call last):
        ...
        KeyError: 'foo:-1'
        >>> d['foo'] # doctest: +ELLIPSIS
        Traceback (most recent call last):
        ...
        KeyError: 'foo'
    """

    def __setitem__(self, key, value):
        if key.endswith('-1'):
            self.purge()
        else:
            super(PurgableCleanupDict, self).__setitem__(key, value)

    def purge(self):
        for key, timestamp in self._last_access.items():
            del self._last_access[key]
            super(PurgableCleanupDict, self).__delitem__(key)


def _get_list_information_cachekey(method, tool, forcereload=False):
    cachekey = forcereload and -1 or time.time() // (60 * 60)
    return cachekey


def store_on_self(method, obj, *args, **kwargs):
    return obj.__dict__.setdefault(
        plone.memoize.volatile.ATTR, PurgableCleanupDict())
