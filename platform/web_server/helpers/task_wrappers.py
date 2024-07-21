import logging
import requests

import celery
from rest_framework import status

logger = logging.getLogger(__name__)


class PeriodicTaskExceptionHandler(celery.Task):
    def __call__(self, *args, **kwargs):
        """In celery task this function call the run method, here you can
        set some environment variable before the run of the task"""
        try:
            return self.run(*args, **kwargs)
        except requests.JSONDecodeError as e:
            logger.info(f"{e.__class__.__name__}: {e}")
        except requests.HTTPError as e:
            message = (
                f"[{e.response.status_code}] {e.__class__.__name__} received. "
                f"Request url: {e.request.url}. "
                f"Response content: {e.response.content}."
            )

            if e.response.status_code == status.HTTP_429_TOO_MANY_REQUESTS:
                message += f" Request limit reset in {e.response.headers.get('Retry-After')}."

            if e.response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
                logger.info(message)
            else:
                logger.error(message)
        except requests.ConnectionError as e:
            logger.warning(
                f"{e.__class__.__name__} received. "
                f"Request url: {e.request.url}."
            )
        except Exception as e:
            logger.exception(e)


    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        #exit point of the task whatever is the state
        pass
