#import databasemodel
from google.appengine.ext import db

#create user_acount database
class Accounts(db.Model):
        #create column username in database
        username = db.StringProperty(required = True)
        #create column with hashed password
        password = db.StringProperty(required = True)
        #create column for an email
        email    = db.StringProperty()
        
        @classmethod
        def by_id(self,uid):
            u = Accounts.get_by_id(uid)
            return u

        @classmethod
        def wipe_data(self):
            q = db.GqlQuery("SELECT * FROM Accounts")
            results = q.fetch(1000)
            db.delete(results) 

        @classmethod
        def get_data(self):
            query = db.GqlQuery("SELECT * FROM Accounts")
            return query
        
        @classmethod
        def by_name(cls,name):
            u = Accounts.all().filter('username =', name).get()
            return u  

        @classmethod
        def user_id(cls,user):     
            return str(user.key().id())

        @classmethod
        def get_user_by_cookie(cls,cookie):

            if cookie:    
                id = cookie.split("|")[0]

                return cls.by_id(int(id)).username  


                  
                
class wikiData(db.Model):
    #store wikis data
    content = db.TextProperty()
    #store created date
    created = db.DateTimeProperty(auto_now_add = True)

    #every path will have its own parent key
    #this will ensure strong consistency
    #and the retrieval of entities will be easy
    @staticmethod
    def parent_key(path):
        #create a parrent key
        return db.Key.from_path("/root " + path, 'pages')

    @classmethod
    def by_path(self,path):
        q = self.all()
        q.ancestor(self.parent_key(path))
        q.order("-created")
        return q     

    @classmethod
    def by_id(self,uid,path):
        u = wikiData.get_by_id(uid,parent = self.parent_key(path))
        return u   

    @classmethod
    def wipe_data(self):
        q = db.GqlQuery("SELECT * FROM wikiData")
        results = q.fetch(1000)
        db.delete(results) 

    @classmethod
    def get_data(self):
        query = db.GqlQuery("SELECT * FROM wikiData LIMIT 10")
        return query

    #get link associated with that post
    @classmethod
    def by_link(cls,link):
        u = wikiData.all().filter('link =', link).get()
        return u