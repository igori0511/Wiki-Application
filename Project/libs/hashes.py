import random
import string
import hashlib
import hmac

class Hash():
    #password hashing
    #make a hashed password
    @classmethod
    def make_pw_hash(self,name, pw, salt = None):
        if not salt:
            salt = self.make_salt()
        h = hashlib.sha512(name + pw + salt).hexdigest()
	
        return '%s,%s' % (h, salt)

    #make a salt for a given user
    @classmethod    
    def make_salt(self):
        return ''.join(random.choice(string.ascii_lowercase) for x in xrange(5))
	
     #check if user is valid   
    @classmethod		
    def valid_pw(self,name, pw, h):
        salt = h.split(",")[1]
        return self.make_pw_hash(name,pw,salt) == h

    ##### cookie hashing    
    #init secret word
    SECRET = "bwtnwgbtosaifcvyjyqiivhrtmklukeigahosdgahoixoxgogx"
    #make a hash from a secret and an input
    @classmethod 
    def hash_str(self,s):
        return hmac.new(self.SECRET, s).hexdigest()

    #make a security value
    @classmethod
    def make_secure_val(self,s):
        return "%s|%s" % (s, self.hash_str(s))

    #check if it is valid
    @classmethod
    def check_secure_val(self,h):
        if h:
            val = h.split('|')[0]            
            if h == self.make_secure_val(val):
                return val
