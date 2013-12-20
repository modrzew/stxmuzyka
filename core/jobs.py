from datetime import date, datetime, timedelta

from google.appengine.ext import ndb
from webapp2 import Route, WSGIApplication

from core.models import Config, Result
from core import parser
from ext.handlers import BaseHandler


# What is the oldest log available?
START_FROM = date(2013, 12, 17)


class FreshStart(BaseHandler):
    """
    Removes everything and then reads all logs.
    TODO: will need some deferring here in future.
    """
    def get(self):
        # Reset config
        config = Config.get_master()
        config.last_refresh = None
        config.put()
        # Remove all results
        keys = []
        for result_key in Result.query().iter(keys_only=True):
            keys.append(result_key)
        ndb.delete_multi(keys)
        # Refresh from start
        current = START_FROM
        today = date.today()
        day = timedelta(days=1)
        while current <= today:
            results = parser.parse(current)
            ndb.put_multi(results)
            current += day
        config.last_refresh = datetime.now()
        config.put()


app = WSGIApplication([
    Route('/jobs/fresh_start', FreshStart),
])
