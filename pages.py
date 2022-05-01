# Standard libs

# Pip installs
import tornado.web

# Local imports
import loggingformatter as lf

class BaseHandler(tornado.web.RedirectHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")



class Page(BaseHandler):

    def initialize(self, ParentServer) -> None:
        self.ParentServer = ParentServer
        self.name : str
        self.Protected : bool
        self.callback : function
        self.html : str
        self.html_ISFILE : bool = False
    
    def get(self) -> None:
        if (not self.current_user) and self.Protected:
            url = self.get_login_url()
            self.redirect(url)
        else:
            if self.html != None:
                if self.html_ISFILE:
                    self.render(self.html)
                else:
                    self.write(self.html)
            else:
                lf.notify(f"NO HTML GIVEN FOR PAGE '{self.name}'",lf.Warninglevels.ERROR)


class LoginHandler(tornado.web.RequestHandler):
    def initialize(self, ParentServer) -> None:
        self.parent = ParentServer
        self.test : str
        print(self.test)

    def get(self) -> None:
        self.write('<html><body><form action="/test" method="post">'
                   'Name: <input type="text" name="name">'
                   '<input type="submit" value="Sign in">'
                   '</form></body></html>')

    def post(self) -> None:
        print(self.get_argument("name"))
        self.redirect("/")
        #self.set_secure_cookie("user", self.get_argument("name"))
        #self.redirect("/")

class TestHandler(tornado.web.RequestHandler):
    def initialize(self, ParentServer) -> None:
        self.parent = ParentServer

    def get(self) -> None:
        self.parent.runCallback()
        self.render("html-pages/index.html")