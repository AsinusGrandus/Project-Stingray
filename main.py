
# Local imports
import webserver
import config
import loggingformatter as lf

# Run the webserver
Webserver = webserver.Webserver(devmode=True, daemon=True)

Webserver.setPort(config.PORT)
paggeee = webserver.pages.Page
paggeee.name, paggeee.Protected, paggeee.html_ISFILE = "geit", False, False
paggeee.html = "<html><body><h1>testpageeeee</h1></body></html>"
Webserver.addPage(paggeee,r"/")
Webserver.addPage(webserver.pages.LoginHandler,r"/login")
#Webserver.addSSL(certPath=config.CERT_PATH, keyPath=config.KEY_PATH,)


def testfunc() -> None:
    print()

Webserver.addCallback(testfunc)


if __name__ == '__main__':
    Webserver.startWebServer()