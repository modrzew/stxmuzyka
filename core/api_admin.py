from google.appengine.api import memcache
from google.appengine.ext import ndb

from ext.handlers import BaseHandler
from models import Result


class ResultHandler(BaseHandler):
    """
    Handler for managing single result.
    """
    def delete(self, result_id):
        """
        Removes a result.
        """
        try:
            result_id = int(result_id)
        except ValueError:
            self.respond_json({'error': 'invalid key'}, status_code=400)
        key = ndb.Key(Result, result_id)
        key.delete()
        # Purge memcache aferwards
        memcache.delete('results')
