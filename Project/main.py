import sys
sys.path.insert(0, 'libs')
import webapp2
import os
import jinja2
import logging
import time
from validate import validation
from hashes import *
from databases import *

#get current directory
template_dir = os.path.join(os.getcwd(),'templates')
#initialize template engine
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=True)

#handle template processing using jinja2 templates
class Handler(webapp2.RequestHandler):

    def write(self,*a,**kw):
        self.response.out.write(*a,**kw)
        
    def render_str(self,template,**params):
        t=jinja_env.get_template(template)
        return t.render(params)
    
    def render(self,template,**kw):
        self.write(self.render_str(template,**kw))

    def set_cookie(self,user):
        #get user id
        id = Accounts.user_id(user)
        #make a new cookie
        new_cookie_val = Hash.make_secure_val(id)
        #set cookie
        self.response.headers.add_header('Set-Cookie', 'user_id=%s;Path=/' % new_cookie_val) 

    def get_cookie(self):
        return self.request.cookies.get('user_id')

    def check_login(self):
        cookie = self.get_cookie()
        return Hash.check_secure_val(cookie)

    def get_by_id(self,uid,path):
        return wikiData.by_id(uid,path)

    def get_content(self,url):
            x = self.request.get("v")

            if x:
                return wikiData.by_id(int(x),url)

            return wikiData.by_path(url).get()                       


#class for signing up the new user
class Signup(Handler):
	
   #render html page
    def render_page(self,**values):
        self.render("registration.html",**values)
        
    #get method  - browser request    
    def get(self):
        self.render_page()
   

    #post method - server responce    
    def post(self):
        #assume that the information is valid
        valid = True
        values = dict({})        
        #get uset information
        #get username from the form
        username      = self.request.get("username")
        #get password from the form
        password      = self.request.get("password")
        #get password one more time from the form
        verify        = self.request.get("verify")
        #get email if user provides it from the form
        email         = self.request.get("email")
        
        #check if username is valid
        valid_user_name     = validation.valid_username(username)
        #check if password is valid
        valid_password      = validation.valid_password(password)
        #check if email is valid 
        valid_verify_email  = validation.valid_email(email)
        
        # if username is not valid init first error
        if not valid_user_name:
            values["error1"] = "That's not a valid username."
            valid = False
        #check if the user already registered    
        if Accounts.by_name(username):
            values["error1"] = "Username already exist!"
            valid = False
            
        # if password not valid
        #init second error    
        if not valid_password:
            values["error2"] = "Thats not a valid password"
            valid = False
        
        # if passwords don't match
        #init error 3    
        if password != verify:
            values["error3"] = "Password don't match."
            valid = False
        # if email isn't valid and email not empty
        # init error4    
        if not valid_verify_email and email != "":
            values["error4"] = "Thats not a valid email adress."
            valid = False
        #if input isn't valid write corresponding errors    
        if not valid:
            #add username and email to dict
            values["username"] = username
            values["email"]    = email
            #render our page
            self.render_page(**values)
        #else add data to the database
        else :
            #create an instance of a database
            user = Accounts(username = username,
                            password=Hash.make_pw_hash(username,password),
                            email=email)
            #put that data in the database
            user.put()
            #set cookie, supply the id of the entity
            self.set_cookie(user)            
            # redirect
            self.redirect("/")

#class for login

class Login(Handler):
	  # renders our page
    def render_page(self,render_page="login.html",**error):

        self.render(render_page,**error)
    
        # get method(getting data from the server)
    def get(self):
        self.render_page()
    # check if the entered info is valid
    def check_user(self,name,pw,user):
            # if value not none
        if user:
            #check the user return true if pw and name are correct false otherwise
            return Hash.valid_pw(name,pw,user.password)
        else:
            # if empty return False    
            return False
    
    def post(self):
            #request username       
        username = self.request.get("username")
            #request password        
        password = self.request.get("password")

            #get user info from the database
        user  = Accounts.by_name(username)
        #check if supplied information is valid     
        if self.check_user(username,password,user):
            self.set_cookie(user)

            self.redirect("/")
            # else rerender form with a error    
        else:
            self.render_page(login_error = "Invalid login")

#logout from the page
class Logout(Handler):
    def get(self):
        self.response.headers.add_header('Set-Cookie', 'user_id=; Path=/')
        self.redirect("/")

class EditPage(Handler):
        
    def get(self,url):

        valid_cookie = self.check_login()

        if valid_cookie:

            page = self.get_content(url)

            self.render("newpage.html",wikidata = page)
        else:
            self.redirect("/login")    

    def post(self,url):

        valid_cookie = self.check_login()

        if valid_cookie:
        
            #get content from the database
            old_page = wikiData.by_path(url).get()

            content = self.request.get("content")

            if not old_page or old_page.content != content:
                #make a new instance of object
                w = wikiData(parent = wikiData.parent_key(url), content = content)
                w.put()
            self.redirect(url)     
        else:
            self.redirect("/login")        


class WikiPage(Handler):
    
    def get(self,url):

        page  = self.get_content(url)        

        valid_cookie = self.check_login()

        if not valid_cookie and page:
            self.render("front.html",wikidata = page)
        elif page and valid_cookie:
            self.render("front_logedin.html",wikidata = page,link = url)
        elif valid_cookie:
            self.redirect("/_edit"+url)        
        else:
            self.redirect("/signup")    


class History(Handler):

    def get(self,url):
        #get entities associated with this parent
        cursor = wikiData.by_path(url)

        self.render("history.html",link = url,wikidata = cursor)





PAGE_RE = r'(/(?:[a-zA-Z0-9_-]+/?)*)'
app = webapp2.WSGIApplication([('/signup', Signup),
                               ('/login' , Login),
                               ('/logout', Logout),
                               ('/_history' + PAGE_RE,History),
                               ('/_edit' + PAGE_RE, EditPage),                               
                               (PAGE_RE, WikiPage),
                               ], debug=True)