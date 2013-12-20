from datetime import date, datetime

from google.appengine.api import memcache
from google.appengine.ext import ndb
from webapp2 import Route, WSGIApplication

from core.models import Config
from core import parser
from ext.handlers import BaseHandler


class ParseItems(BaseHandler):
    """
    Refreshes today links.
    """
    def get(self):
        today = date.today()
        results = parser.parse(today)
        if results:
            ndb.put_multi(results)
            memcache.delete('results')
        config = Config.get_master()
        config.last_refresh = datetime.now()
        config.put()


app = WSGIApplication([
    Route('/cron/refresh', ParseItems),
])
