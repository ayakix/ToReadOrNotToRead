import os

from google.appengine.ext.webapp import template
from google.appengine.ext import webapp

class Top(webapp.RequestHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__), "../views/index.html")
        self.response.out.write(template.render(path, None))
