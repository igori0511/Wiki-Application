import re
class validation:
    #initialize regular expressions
    
    USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
    USER_PS = re.compile(r"^.{3,20}$")
    USER_EM = re.compile(r"^[\S]+@[\S]+\.[\S]+$")
    #validate user input
    #validate user name
    @classmethod
    def valid_username(self,username):
        return self.USER_RE.match(username)
    #validate user password
    @classmethod
    def valid_password(self,password):
        return self.USER_PS.match(password)
    #validate user email
    @classmethod
    def valid_email(self,email):
        return self.USER_EM.match(email)
    #escape unnecesary characters
    @classmethod
    def escape_html(self, s):
        return escape(s, quote = True)
