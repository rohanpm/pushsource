from .base import PushItem
from .. import compat_attr as attr
from .conv import optional_str, instance_of


@attr.s()
class ContainerPushItem(PushItem):
    """A :class:`~pushsource.PushItem` representing a container image.

    More specifically, this item represents an object which can be pulled
    from a container image registry (i.e. an object identified by a
    ``NAME[:TAG|@DIGEST]`` string). This means a single push item may
    represent multiple images via the same manifest list.
    """

    # Raw metadata from atomic-reactor 'image' dict
    WIP_image_raw = attr.ib(
        type=dict, validator=instance_of(dict), default=attr.Factory(dict)
    )

    # Raw metadata from ET
    WIP_external_repos = attr.ib(
        type=dict, validator=instance_of(dict), default=attr.Factory(dict)
    )
