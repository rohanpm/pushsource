from .. import compat_attr as attr
from .base import PushItem


@attr.s()
class RpmPushItem(PushItem):
    """A :class:`~pushsource.PushItem` representing a single RPM."""
