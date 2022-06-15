# Standard libs

# Pip installs
import tornado.web

# Local imports
import loggingformatter as lf

class BaseHandler(tornado.web.RedirectHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")

    def unauthorise_current_user(self):
        self.clear_cookie("user")



class Page(BaseHandler):

    def initialize(self, ParentServer, Name, Protected, Callback, HTML) -> None:
        self.ParentServer = ParentServer
        self.name = Name
        self.Protected = Protected
        self.callback = Callback
        self.html = HTML
    
    def get(self) -> None:
        if (not self.current_user) and self.Protected:
            url = self.get_login_url()
            self.redirect(url)
        else:
            if self.html != None:
                if self.html[-5:] == ".html":
                    self.render(self.html)
                else:
                    self.write(self.html)
            else:
                lf.notify(f"NO HTML GIVEN FOR PAGE '{self.name}'",lf.Warninglevels.ERROR)
        if self.callback != "": self.callback()


class LoginPage(Page):

    def initialize(self, ParentServer, HTML, Credcheck) -> None:
        self.ParentServer = ParentServer
        self.html = HTML
        self.Credcheck = Credcheck

    def get(self) -> None:
        self.write('<html><body><form action="/login" method="post">'
                   'Name: <input type="text" name="name">'
                   'Password: <input type="password" name="password">'
                   '<input type="submit" value="Sign in">'
                   '</form></body></html>')

        if (not self.current_user) and self.Protected:
            if self.html != None:
                if self.html[-5:] == ".html":
                    self.render(self.html)
                else:
                    self.write(self.html)
            else:
                lf.notify(f"NO HTML GIVEN FOR PAGE '{self.name}'",lf.Warninglevels.ERROR)
        else:
            # redirect to protected page
            print()

    def post(self) -> None:
        print(self.get_argument("name"))
        if self.Credcheck() == True:
            self.set_secure_cookie("user", self.get_argument("name"))
        self.redirect("/protected")

class AuthPage(Page):
    def initialize() -> None:
        return
    
    def get(self) -> None:
        if (not self.current_user):
            # Authorise user
            pass
        else:
            # Unauthorise user
            self.unauthorise_current_user()

class TestHandler(tornado.web.RequestHandler):
    def initialize(self, ParentServer) -> None:
        self.parent = ParentServer

    def get(self) -> None:
        self.parent.runCallback()
        self.render("html-pages/index.html")