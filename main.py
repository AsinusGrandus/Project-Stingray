import webserver
import config

# Run the webserver
Webserver = webserver.Webserver(devmode=True, daemon=True)

Webserver.setPort(config.PORT)
# Webserver.addSSL(certPath=config.CERT_PATH, keyPath=config.KEY_PATH,)


def testfunc() -> None:
    print()

Webserver.addCallback(testfunc)


if __name__ == '__main__':
    Webserver.startWebServer()