
import webapp2
import cgi
import os
from webapp2_extras import routes
from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.ext import db
import math
import json
import jinja2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

import urllib2
from cookielib import CookieJar


MAIN_PAGE_HTML = """\
<html>
  <body>
    <h2>Open Piazza</h2>
    <form action="/displayPosts" method="post">
        Piazza email: <input type="text" name="email"><br>
        Password: <input type="text" name="password">
        <input type="submit" value="Submit">
    </form>
  </body>
</html>
"""


class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.out.write(MAIN_PAGE_HTML)

class DisplayPostsHandler(webapp2.RequestHandler):
    def post(self):

        piazza_email = self.request.get('email')
        piazza_password = self.request.get('password')

        cj = CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        url = 'https://piazza.com/logic/api?method=user.login'
        params = '{"method":"user.login","params":{"email":"' + piazza_email + '","pass":"' + piazza_password + '"}}'

 
        # if the user/password match, the server respond will contain a session cookie
        # that you can use to authenticate future requests.
        response = opener.open(url, params)

        #print login_resp.read()
        #self.response.out.write("Login: " + str(response.read()))
        
        #while null_string != "null":
        cid = 8
        while cid < 10:
            if cid == 1:
                self.response.out.write("CID Post: " + str(cid))
                page_url = 'https://piazza.com/logic/api?method=get.content'
                page_params = '{"method":"content.get","params":{"cid"' + str(cid) + '","nid":"hiuvlqlyk4925d"}}'
                page_response = opener.open(page_url, page_params)
                page_response_string = str(page_response.read())
                #self.response.out.write(page_response_string)

                result_location = page_response_string.find("\"result\":")
                result_string = page_response_string[result_location+9:]
                null_string = result_string[:4]
                #self.response.out.write(null_string)

                content_location = page_response_string.find("\"content\":")
                content_string = page_response_string[content_location+10:]
                #self.response.out.write(str(page_response.read()))
                self.response.out.write(str(content_string) + "\n")
                cid += 1
            else:
                self.response.out.write("CID Post: " + str(cid))
                page_url = 'https://piazza.com/logic/api?method=get.content'
                page_params = '{"method":"content.get","params":{"cid":"' + str(cid) + '","nid":"hiuvlqlyk4925d"}}'

                page_response = opener.open(page_url, page_params)
                page_response_string = str(page_response.read())
                #self.response.out.write(page_response_string)

                result_location = page_response_string.find("\"result\":")
                result_string = page_response_string[result_location+9:]
                null_string = result_string[:4]
                #self.response.out.write(null_string)

                content_location = page_response_string.find("\"content\":")
                content_string = page_response_string[content_location+10:]
                #self.response.out.write(str(page_response.read()))
                self.response.out.write(str(content_string) + "\n")
                cid += 1


application = webapp2.WSGIApplication([
                                  ('/', MainHandler),
                                  ('/displayPosts', DisplayPostsHandler),
                                  
                                 
                                 
                                  
                              ], debug=True)
