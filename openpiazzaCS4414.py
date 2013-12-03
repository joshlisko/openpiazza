
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
import json

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


def getComments(firstComment, depth, self):
    if len(firstComment)!=0:
        self.response.write('<dl>')
        for i in firstComment:
            #prefix = '----'*depth
            #self.response.write(prefix)
            self.response.out.write('<dd>')
            self.response.out.write(i['subject'])
            getComments(i['children'],depth+1, self)
            self.response.out.write('</dd>')
        self.response.write('</dl>')


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
        

        cid = 1
        
        self.response.out.write("CID Post: " + str(cid))
        self.response.out.write("\n")
        page_url = 'https://piazza.com/logic/api?method=get.content'
        page_params = '{"method":"content.get","params":{"cid":"' + str(cid) + '","nid":"hiuvlqlyk4925d"}}'
        page_response = opener.open(page_url, page_params)
        jarray = json.loads(str(page_response.read()))

        self.response.out.write(jarray['result']['history'][0]['subject'])
        self.response.out.write("\n")
        self.response.out.write(jarray['result']['history'][0]['content'])
        self.response.out.write("\n")
        self.response.out.write("\t")
        #self.response.out.write(jarray['result']['children'][0]['subject'])
        getComments(jarray['result']['children'], 1, self)


    



        
        
        


application = webapp2.WSGIApplication([
                                  ('/', MainHandler),
                                  ('/displayPosts', DisplayPostsHandler),
                                  
                                 
                                 
                                  
                              ], debug=True)
