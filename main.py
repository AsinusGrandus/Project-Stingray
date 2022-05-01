
# Local imports
import webserver
import config
import loggingformatter as lf

# Run the webserver

#Webserver.addSSL(certPath=config.CERT_PATH, keyPath=config.KEY_PATH,)


def testfunc() -> None:
    print("Test")

#Webserver.addCallback(testfunc)

if __name__ == "__main__":
    Webserver = webserver.Webserver(devmode=False, daemon=True)
    print("hollo")
    Webserver.setPort(config.PORT)
    testpage = webserver.pages.Page
    Webserver.addPage(testpage, r"/", "<html><body><h1>testpageeeee</h1></body></html>", "geit", callback=testfunc)
    #Webserver.addPage(webserver.pages.LoginHandler,r"/login")
    Webserver.startWebServer()