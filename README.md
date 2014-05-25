###This is a basic wiki application on Google App Engine
####Basic functionality is:
1. Adding new posts
2. Registration
3. Loggin
4. History

###History is implemented for every new post


###List of handlers:
1. ('/signup', Signup),
2. ('/login' , Login),
3. ('/logout', Logout),
4. ('/_history' + PAGE_RE,History),
5. ('/_edit' + PAGE_RE, EditPage),                           
6. (PAGE_RE, WikiPage)



###Download google app engine for Python 2.7 from:
https://developers.google.com/appengine/downloads

###To start the app locally:
1. Add the app to your project list in GAE launcher and click the run button
2. Go to your browser of choice and type: **localhost:*port***

###Other links:
1. **localhost:*port/signup***
2. **localhost:*port/login***
3. **localhost:*port/logout***
4. **localhost:*port/_history + THE NAME OF THE PAGE***
5. **localhost:*port/PAGENAME***


###To Deploy the application to Google do the following:
1. Add the app to your project list in GAE launcher
2. Login to your google email
3. Go to https://appengine.google.com/start and create an application
4. Modify the *app.yaml* file as follows:
	change the the top most line ***application: cs253class1992***
	to ***application: Application Identifier***
5. Finaly In GAE launcher select the project and click *Deploy*


###Working project:
[Working wiki application](http://cs253class1992.appspot.com)
