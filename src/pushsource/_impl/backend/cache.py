import os

from six.moves import intern

import attr
from frozenlist2 import frozenlist


# This var is mainly intended to allow for easily testing the memory
# usage impact of turning the cache on or off.
USE_CACHE = (os.environ.get("PUSHSOURCE_ATTR_CACHE") or "1") != "0"

# String fields worthy of caching.
#
# Note that all of these fields today belong to the PushItem base class,
# hence there is no need to separate fields by push item type as of yet.
INTERN_FIELDS = ["origin", "signing_key", "state"]


def intern_maybe(x):
    # intern x if and only if it's a str.
    if isinstance(x, str):
        return intern(x)
    return x


class AttrCacher(object):
    def __init__(self, enabled=USE_CACHE):
        self._dest = {}
        if not enabled:
            self.with_cached_fields = lambda x: x

    def _cached_dest(self, dest):
        cached = self._dest.get(dest)
        if cached is None:
            cached = frozenlist([intern_maybe(d) for d in dest])
            self._dest[cached] = cached
        return cached

    def with_cached_fields(self, item):
        updates = {}

        # intern any worthy strings.
        for field in INTERN_FIELDS:
            value = getattr(item, field)
            updates[field] = intern_maybe(value)

        # dest field uses something a bit more special to ensure
        # both the dest strings and the containing list are cached.
        updates["dest"] = self._cached_dest(item.dest)

        return attr.evolve(item, **updates)
