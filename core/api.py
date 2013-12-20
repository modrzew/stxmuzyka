from datetime import datetime

from google.appengine.api import memcache

from ext.handlers import BaseHandler
from models import Result, Config


# How often do we refresh?
REFRESH_MINUTES = 10


class ResultsHandler(BaseHandler):
    """
    Handler for collection of Results.
    """

    def get(self):
        """
        Gets 50 last results.
        """
        config = Config.get_master()
        # First, check memcache
        results = memcache.get('results')
        if not results:
            results_raw = Result.query().order(-Result.when).fetch(50)
            results = [r.to_dict() for r in results_raw]
            memcache.add('results', results)
        # next_refresh: seconds to next refresh
        elapsed = datetime.now() - config.last_refresh
        next_refresh = REFRESH_MINUTES * 60 - elapsed.total_seconds()
        self.respond_json({
            'results': results,
            'next_refresh': int(next_refresh)
        })
