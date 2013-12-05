
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
    <head>
        <script src="//ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min.js"></script>
        <script src="//ajax.googleapis.com/ajax/libs/jqueryui/1.10.3/jquery-ui.min.js"></script>
        <link href="http://netdna.bootstrapcdn.com/bootstrap/3.0.0/css/bootstrap.min.css" rel="stylesheet">
        <script src="http://netdna.bootstrapcdn.com/bootstrap/3.0.0/js/bootstrap.min.js"></script>
        <link href="http://code.jquery.com/ui/1.10.3/themes/smoothness/jquery-ui.css" rel="stylesheet">
        <script src="http://code.jquery.com/jquery-1.9.1.js"></script>
        <script src="http://code.jquery.com/ui/1.10.3/jquery-ui.js"></script>
        <link href="http://plato.cs.virginia.edu/~cs4720f13arugula/phase5/extraCSS.css" rel="stylesheet">
    </head>
    <body>
        
        <div class="navbar navbar-default" role="navigation">
            <div class="navbar-header">
            <button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-collapse">
                <span class="sr-only">Toggle navigation</span>
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
            </button>
          
            </div>
            <div class="navbar-collapse collapse">
              <ul class="nav navbar-nav">
            <li><a href="">Home</a></li>
            <li class="dropdown">
                <a href="" class="dropdown-toggle" data-toggle="dropdown">Class Info<b class="caret"></b></a>
                <ul class="dropdown-menu">
                  <li><a href="http://openpiazzacs4414.appspot.com/viewclasses">View Class Posts</a></li>
                  <li><a href="http://openpiazzacs4414.appspot.com/registerclass">Register a class</a></li>
                  <li><a href="http://openpiazzacs4414.appspot.com/displayPost/119/hiuvlqlyk4925d/nid=hiuvlqlyk4925d&auth=ee64796">Test Get Post</a></li>
                </ul>
            </li>
            <li>
                <li><a href="http://openpiazzacs4414.appspot.com/registerpost">Add a Post</a></li>
            </li>
            </div>
        </div>
        <h2>Open Piazza</h2>
        <h4>Not a part of the home page, just for demo purposes</h4>
        <form action="/displayPosts" method="post">
            Demo account link: <input type="text" name="demoaccount"><br>
            <input type="submit" value="Submit">
        </form>
        <br>
        <br>
        <br>
        <br>
        <p>By Evan Boyle, Josh Lisko, and Evan Teague</p>
    </body>
</html>
"""

PostsPerClass_HTML = """\
<html>
    <head>
        <script src="//ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min.js"></script>
        <script src="//ajax.googleapis.com/ajax/libs/jqueryui/1.10.3/jquery-ui.min.js"></script>
        <link href="http://netdna.bootstrapcdn.com/bootstrap/3.0.0/css/bootstrap.min.css" rel="stylesheet">
        <script src="http://netdna.bootstrapcdn.com/bootstrap/3.0.0/js/bootstrap.min.js"></script>
        <link href="http://code.jquery.com/ui/1.10.3/themes/smoothness/jquery-ui.css" rel="stylesheet">
        <script src="http://code.jquery.com/jquery-1.9.1.js"></script>
        <script src="http://code.jquery.com/ui/1.10.3/jquery-ui.js"></script>
        <link href="http://plato.cs.virginia.edu/~cs4720f13arugula/phase5/extraCSS.css" rel="stylesheet">
    </head>
    <body>
        
        <div class="navbar navbar-default" role="navigation">
            <div class="navbar-header">
            <button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-collapse">
                <span class="sr-only">Toggle navigation</span>
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
            </button>
          
            </div>
            <div class="navbar-collapse collapse">
              <ul class="nav navbar-nav">
            <li><a href="http://openpiazzacs4414.appspot.com/">Home</a></li>
            <li class="dropdown">
                <a href="" class="dropdown-toggle" data-toggle="dropdown">Class Info<b class="caret"></b></a>
                <ul class="dropdown-menu">
                  <li><a href="http://openpiazzacs4414.appspot.com/viewclasses">View Class Posts</a></li>
                  <li><a href="http://openpiazzacs4414.appspot.com/registerclass">Register a class</a></li>
                </ul>
            </li>
            <li>
                <li><a href="http://openpiazzacs4414.appspot.com/registerpost">Add a Post</a></li>
            </li>
            </div>
        </div>
        <h2>View Class Posts</h2>
        <select>
            <option value="1">1</option>
            <option value="2">2</option>
            <option value="3">3</option>
            <option value="4">4</option>
        </select>
    </body>
</html>
"""

RegisterClass_HTML = """\
<html>
    <head>
        <script src="//ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min.js"></script>
        <script src="//ajax.googleapis.com/ajax/libs/jqueryui/1.10.3/jquery-ui.min.js"></script>
        <link href="http://netdna.bootstrapcdn.com/bootstrap/3.0.0/css/bootstrap.min.css" rel="stylesheet">
        <script src="http://netdna.bootstrapcdn.com/bootstrap/3.0.0/js/bootstrap.min.js"></script>
        <link href="http://code.jquery.com/ui/1.10.3/themes/smoothness/jquery-ui.css" rel="stylesheet">
        <script src="http://code.jquery.com/jquery-1.9.1.js"></script>
        <script src="http://code.jquery.com/ui/1.10.3/jquery-ui.js"></script>
        <link href="http://plato.cs.virginia.edu/~cs4720f13arugula/phase5/extraCSS.css" rel="stylesheet">
    </head>
    <body>
        
         <div class="navbar navbar-default" role="navigation">
            <div class="navbar-header">
            <button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-collapse">
                <span class="sr-only">Toggle navigation</span>
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
            </button>
          
            </div>
            <div class="navbar-collapse collapse">
              <ul class="nav navbar-nav">
            <li><a href="http://openpiazzacs4414.appspot.com/">Home</a></li>
            <li class="dropdown">
                <a href="" class="dropdown-toggle" data-toggle="dropdown">Class Info<b class="caret"></b></a>
                <ul class="dropdown-menu">
                  <li><a href="http://openpiazzacs4414.appspot.com/viewclasses">View Class Posts</a></li>
                  <li><a href="http://openpiazzacs4414.appspot.com/registerclass">Register a class</a></li>
                </ul>
            </li>
            <li>
                <li><a href="http://openpiazzacs4414.appspot.com/registerpost">Add a Post</a></li>
            </li>
            </div>
        </div>
        <h2>Register a Class</h2>
        <form action="/addclass" method="post">
            Class Name: <input type="text" name = "classname"><br>
            Class suffix: <input type="text" name="suffix"><br>
            Demo account link: <input type="text" name="demoaccount"><br>
            <input type="submit" value="Submit">
        </form>
    </body>
</html>
"""


AddPost_HTML = """\
<html>
    <head>
        <script src="//ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min.js"></script>
        <script src="//ajax.googleapis.com/ajax/libs/jqueryui/1.10.3/jquery-ui.min.js"></script>
        <link href="http://netdna.bootstrapcdn.com/bootstrap/3.0.0/css/bootstrap.min.css" rel="stylesheet">
        <script src="http://netdna.bootstrapcdn.com/bootstrap/3.0.0/js/bootstrap.min.js"></script>
        <link href="http://code.jquery.com/ui/1.10.3/themes/smoothness/jquery-ui.css" rel="stylesheet">
        <script src="http://code.jquery.com/jquery-1.9.1.js"></script>
        <script src="http://code.jquery.com/ui/1.10.3/jquery-ui.js"></script>
        <link href="http://plato.cs.virginia.edu/~cs4720f13arugula/phase5/extraCSS.css" rel="stylesheet">
    </head>
    <body>
        
         <div class="navbar navbar-default" role="navigation">
            <div class="navbar-header">
            <button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-collapse">
                <span class="sr-only">Toggle navigation</span>
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
            </button>
          
            </div>
            <div class="navbar-collapse collapse">
              <ul class="nav navbar-nav">
            <li><a href="http://openpiazzacs4414.appspot.com/">Home</a></li>
            <li class="dropdown">
                <a href="" class="dropdown-toggle" data-toggle="dropdown">Class Info<b class="caret"></b></a>
                <ul class="dropdown-menu">
                  <li><a href="http://openpiazzacs4414.appspot.com/viewclasses">View Class Posts</a></li>
                  <li><a href="http://openpiazzacs4414.appspot.com/registerclass">Register a class</a></li>
                </ul>
            </li>
            <li>
                <li><a href="http://openpiazzacs4414.appspot.com/registerpost">Add a Post</a></li>
            </li>
            </div>
        </div>
        <h2>Add a Post</h2>
            <form action="/addpost" method="post">
                Post Title: <input type="text" name= "posttitle"><br>
                CID: <input type="text" name = "cidvalue"><br>
                Class suffix: <input type="text" name="suffix"><br>
                <input type="submit" value="Submit">
            </form>
            
    </body>
</html>
"""

class classes(db.Model):
    class_name = db.StringProperty()
    url_suffix = db.StringProperty()
    demo_account = db.StringProperty()

class posts(db.Model):
    title = db.StringProperty()
    cid = db.StringProperty()
    url_suffix = db.StringProperty()
    

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

class DisplayClassesHandler(webapp2.RequestHandler):
    def get(self):
        #self.response.out.write(PostsPerClass_HTML)
        #allPosts = db.GqlQuery("""SELECT * FROM posts""")
        allClasses = db.GqlQuery("""SELECT * FROM classes""")
        allPosts = db.GqlQuery("""SELECT * FROM posts""")
        template_values = {
            #'postsArray': allPosts,
            'classArray': allClasses,
            'postsArray': allPosts,
        }
        template = JINJA_ENVIRONMENT.get_template('displayPostsPerClass.html')
        self.response.write(template.render(template_values))

class DisplayRegisterClassHandler(webapp2.RequestHandler):
    def get(self):
        self.response.out.write(RegisterClass_HTML)

class DisplayAddPostHandler(webapp2.RequestHandler):
    def get(self):
        self.response.out.write(AddPost_HTML)

class AddPostHandler(webapp2.RequestHandler):
    def post(self):
        #Insert code to add a post CID
        posttitle = self.request.get('posttitle')
        postcid = self.request.get('cidvalue')
        urlsuffix = self.request.get('suffix')
        posts(title=posttitle, cid=postcid, url_suffix=urlsuffix).put()
        #self.response.out.write()

class RegisterClassHandler(webapp2.RequestHandler):
    def post(self):
        #Insert code to add a class and credentials
        urlsuffix = self.request.get('suffix')
        classname = self.request.get('classname')
        demoaccount = self.request.get('demoaccount')
        classes(class_name=classname, url_suffix=urlsuffix, demo_account=demoaccount).put()
        #self.response.out.write()

class ChooseClassHandler(webapp2.RequestHandler):
    def get(self, classtitle):
        classTitle = "\'" + classtitle + "\'"
        foundClass = db.GqlQuery("""SELECT * FROM classes WHERE class_name = """+classTitle)
        url_suffix = ""
        demo_account = ""
        for class1 in foundClass:
            url_suffix = class1.url_suffix
            demo_account = class1.demo_account

        url_Suffix = "\'" + url_suffix + "\'"
        foundCIDs = db.GqlQuery("""SELECT * FROM posts WHERE url_suffix = """+url_Suffix)


        template_values2 = {
            #'postsArray': allPosts,
            'postsArray': foundCIDs,
            'url_suffix': url_suffix,
            'demo_account': demo_account,
        }
        template = JINJA_ENVIRONMENT.get_template('displayPostsPerClass2.html')
        self.response.write(template.render(template_values2))

        
        
        #Add another /url handler to handle passing the class to this file then it will load the appropriate CID
class DisplayPostHandler(webapp2.RequestHandler):
    def get(self, postCID, url_suffix, demo_account):

        cj = CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        #url = 'https://piazza.com/demo_login?nid=hiuvlqlyk4925d&auth=ee64796'
        #params = '{"method":"user.login","params":{"email":"' + piazza_email + '","pass":"' + piazza_password + '"}}'
        url = 'https://piazza.com/demo_login?' + demo_account
        cid = postCID
        suffix = url_suffix

        response = opener.open(url)

        
        self.response.out.write("CID Post: " + str(cid))
        self.response.out.write("\n")
        page_url = 'https://piazza.com/logic/api?method=get.content'
        page_params = '{"method":"content.get","params":{"cid":"' + str(cid) + '","nid":"' + str(suffix) + '"}}'
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
                                  ('/chooseClass/(.*)', ChooseClassHandler),
                                  ('/viewclasses', DisplayClassesHandler),
                                  ('/registerclass', DisplayRegisterClassHandler),
                                  ('/registerpost', DisplayAddPostHandler),
                                  ('/addpost', AddPostHandler),
                                  ('/addclass', RegisterClassHandler),
                                  ('/displayPost/(.*)/(.*)/(.*)', DisplayPostHandler),
                                  #('/viewpostsperclass/(.*)/(.*)', DisplayPostsPerClassHandler),
                                  
                                 
                                 
                                  
                              ], debug=True)
