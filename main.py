import webserver
import config

# Run the webserver
Webserver = webserver.Webserver(port=config.PORT, devmode=True, daemon=True)

def testfunc():
    print("loopback")
Webserver.addCallback(testfunc)
#Webserver.addSSL(certPath=config.CERT_PATH, keyPath=config.KEY_PATH,)
if __name__ == '__main__':
    Webserver.startWebServer()

    