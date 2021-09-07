from .. import compat_attr as attr
from .base import PushItem


@attr.s()
class ModuleMdPushItem(PushItem):
    """A :class:`~pushsource.PushItem` representing a modulemd stream.

    For push items of this type, the :meth:`~pushsource.PushItem.src` attribute
    refers to a file containing a YAML document stream. The stream is expected
    to contain one or more modulemd or modulemd-defaults documents.

    This library does not verify that the referenced file is a valid
    modulemd stream.
    """
