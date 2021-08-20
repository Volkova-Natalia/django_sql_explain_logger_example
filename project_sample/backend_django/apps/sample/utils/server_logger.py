import logging
from django.conf import settings

logger = logging.getLogger(__name__)


def server_logger(request, result):
    if settings.DEBUG:
        logger.debug('"' + request.META['REQUEST_METHOD'] + ' ' +
                     request.META['PATH_INFO'] + ' ' +
                     request.META['SERVER_PROTOCOL'] + '" ' +
                     str(result.status_code) + ' ' +
                     str(len(str(result.data)) if result.data is not None else 0))
