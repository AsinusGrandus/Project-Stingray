
# Local imports
from webserver import Webserver as ws
from pages import Page, LoginPage
import config
import loggingformatter as lf

# Run the webserver

#Webserver.addSSL(certPath=config.CERT_PATH, keyPath=config.KEY_PATH,)


def testfunc() -> None:
    print("Test")

#Webserver.addCallback(testfunc)

if __name__ == "__main__":
    Webserver = ws(devmode=True, daemon=True)
    Webserver.setPort(config.PORT)
    testpage = Page
    loginpage = LoginPage
    protectedPage = Page
    testhtml = "<html><body><h1>testpage</h1></body></html>"
    test2html = "<html><body><h1>Protected access</h1></body></html>"
    Webserver.addPage(testpage, r"/", testhtml, "geit", callback=testfunc)
    Webserver.addPage(loginpage, r"/login", testhtml)
    Webserver.addPage(protectedPage, r"/protected", test2html, protected=True)
    Webserver.startWebServer()