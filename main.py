import webserver
import config

# Run the webserver
Webserver = webserver.Webserver(devmode=True, daemon=True)

Webserver.setPort(8888)
# Webserver.addSSL(certPath=config.CERT_PATH, keyPath=config.KEY_PATH,)

def testfunc():
    print("loopback")
Webserver.addCallback(testfunc)
#Webserver.addSSL(certPath=config.CERT_PATH, keyPath=config.KEY_PATH,)
if __name__ == '__main__':
    Webserver.startWebServer()

    
