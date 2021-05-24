import logging
import threading
from functools import partial
from contextlib import contextmanager

from six.moves.xmlrpc_client import ServerProxy
from more_executors import Executors
from more_executors.futures import f_zip, f_map
from monotonic import monotonic

from ...compat_attr import attr

LOG = logging.getLogger("pushsource.errata_client")


@contextmanager
def et_log(method_name, advisory_id):
    # Helper to gather metrics around calls to ET's API.
    # Some of these methods have historically had performance issues,
    # so let's enable gathering of structured data as we call them to serve
    # as evidence of performance improvements or regressions.
    now = monotonic()

    LOG.debug(
        "Call %s - %s",
        method_name,
        advisory_id,
        extra={
            "event": {
                "type": "et-call-start",
                "method": method_name,
                "advisory": advisory_id,
            }
        },
    )

    try:
        yield
        LOG.debug(
            "End call %s - %s",
            method_name,
            advisory_id,
            extra={
                "event": {
                    "type": "et-call-end",
                    "method": method_name,
                    "advisory": advisory_id,
                    "duration": monotonic() - now,
                }
            },
        )
    except:
        LOG.debug(
            "Failed call %s - %s",
            method_name,
            advisory_id,
            extra={
                "event": {
                    "type": "et-call-fail",
                    "method": method_name,
                    "advisory": advisory_id,
                    "duration": monotonic() - now,
                }
            },
        )
        raise


@attr.s()
class ErrataRaw(object):
    # Helper to collect raw responses of all ET APIs for a single advisory
    advisory_cdn_metadata = attr.ib(type=dict)
    advisory_cdn_file_list = attr.ib(type=dict)
    advisory_cdn_docker_file_list = attr.ib(type=dict)
    ftp_paths = attr.ib(type=dict)


class ErrataClient(object):
    def __init__(self, threads, url):
        self._executor = Executors.thread_pool(max_workers=threads).with_retry()
        self._url = url
        self._tls = threading.local()

        self._get_advisory_cdn_metadata = partial(
            self._call_et, "get_advisory_cdn_metadata"
        )
        self._get_advisory_cdn_file_list = partial(
            self._call_et, "get_advisory_cdn_file_list"
        )
        self._get_advisory_cdn_docker_file_list = partial(
            self._call_et, "get_advisory_cdn_docker_file_list"
        )
        self._get_ftp_paths = partial(self._call_et, "get_ftp_paths")

    @property
    def _errata_service(self):
        # XML-RPC client connected to errata_service.
        # Each thread uses a separate client.
        if not hasattr(self._tls, "errata_service"):
            LOG.debug("Creating XML-RPC client for Errata Tool: %s", self._url)
            self._tls.errata_service = ServerProxy(self._url)
        return self._tls.errata_service

    def get_raw_f(self, advisory_id):
        """Returns Future[ErrataRaw] holding all ET responses for a particular advisory."""
        all_responses = f_zip(
            self._executor.submit(self._get_advisory_cdn_metadata, advisory_id),
            self._executor.submit(self._get_advisory_cdn_file_list, advisory_id),
            self._executor.submit(self._get_advisory_cdn_docker_file_list, advisory_id),
            self._executor.submit(self._get_ftp_paths, advisory_id),
        )
        return f_map(all_responses, lambda tup: ErrataRaw(*tup))

    def _call_et(self, method_name, advisory_id):
        method = getattr(self._errata_service, method_name)
        with et_log(method_name, advisory_id):
            return method(advisory_id)
