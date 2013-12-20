import json
import logging

from google.appengine.api import namespace_manager

from webapp2_extras import jinja2
from webapp2 import RequestHandler
import webapp2


class BaseHandler(RequestHandler):
    @property
    def request_json(self):
        """
        Interperts the request body as a json string.
        """
        try:
            return json.loads(self.request.body)
        except Exception:
            logging.info('No JSON payload in request body.')
            return {}

    @webapp2.cached_property
    def jinja2(self):
        return jinja2.get_jinja2(app=self.app)

    def respond_json(self, message, status_code=200, pretty=False):
        self.response.set_status(status_code)
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.headers[
            'Access-Control-Allow-Headers'] = 'Authorization,Content-Type'
        self.response.headers['Content-type'] = 'application/json'

        if isinstance(message, basestring):
            message = {'message': message}

        json_string = json.dumps(message)
        return self.response.out.write(json_string)

    def render(self, _template, context=None):
        """
        Renders a template and writes the result to the response.
        """
        variables = {}
        if context:
            variables.update(context)
        rv = self.jinja2.render_template(_template, **variables)
        self.response.write(rv)

    @webapp2.cached_property
    def current_user(self):
        """
        Returns currently logged in user
        """
        user_dict = self.auth.get_user_by_session()
        if user_dict is None:
            logging.debug("User dict is None.")
            return None
        return self.auth.store.user_model.get_by_id(
            user_dict['user_id'], namespace=namespace_manager.get_namespace())
