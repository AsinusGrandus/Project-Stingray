import webserver
import config

# Run the webserver
Webserver = webserver.Webserver(port=config.PORT, devmode=True, daemon=True)
if __name__ == '__main__':
    Webserver.startWebServer()