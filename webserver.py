# Standard libs
import multiprocessing
import os

# Pip installs
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.websocket
import cryptography.fernet as C

# Local imports
import loggingformatter as lf
import pages


# NOTES:
# https:// -> wss://
# http:// -> ws://



# Create the Webserver class
class Webserver(multiprocessing.Process):

    def __init__(self,
                devmode : bool = False, daemon : bool = True) -> None:

        multiprocessing.Process.__init__(self, daemon=daemon)

        # Process init variables
        self.devmode = devmode
        self.debug = self.devmode
        self.autoreload = self.devmode

        # Prepare other variables
        self.port = 5000
        self.certPath = None
        self.keyPath = None
        self.pages = []
        self.settings = {
        "cookie_secret": C.Fernet.generate_key() + C.Fernet.generate_key() + C.Fernet.generate_key() + C.Fernet.generate_key(),
        "login_url": "/login",
        }

    # Function to customise the port 
    def setPort(self, port: int) -> None:
        self.port = port  

    # Add SSL to the webserver
    def addSSL(self, certPath : str = None, keyPath : str = None):
        self.certPath = certPath
        self.keyPath = keyPath

    def addPage(self, page : pages.Page, url):
        page = (url, page, dict(ParentServer=self))
        self.pages.append(page)

    def setCustomLoginURL(self, url : str):
        self.settings["login_url"] = url


    ##################################################### WIP ################################################
    def addCallback(self, functions) -> None:
        self.function = functions

    def runCallback(self) -> None:
        self.function()
    ##################################################### ENDWIP #############################################

    # Start the webserver
    def startWebServer(self) -> None:
        self.start()
        self.join()

    # Define run statement (needed for multiprocessing.Process subclassing)
    def run(self) -> None:
        self.__startWebServer()
    
    # Create the web app
    def __create_app(self) -> tornado.web.Application:
        return tornado.web.Application(
        self.pages, 
        debug = self.debug,
        autoreload = self.autoreload,
        **self.settings
        )

    # Private function to start the webserver
    def __startWebServer(self) -> None:
        application = self.__create_app()

        if self.certPath and self.keyPath != None:
            http_server = tornado.httpserver.HTTPServer(application, ssl_options={
            "certfile": self.certPath,
            "keyfile": self.keyPath,
            })
        else:
            http_server = tornado.httpserver.HTTPServer(application)
            lf.notify("SERVER RUNNING WITHOUT SSL", lf.Warninglevels.WARNING)

        http_server.listen(self.port)
        lf.notify(f'Server is online on port {self.port}', lf.Warninglevels.INFO)

        # Start the server
        tornado.ioloop.IOLoop.current().start()

    ##################################################### WIP ################################################
    class WebSocketHandler(tornado.websocket.WebSocketHandler):
        def initialize(self, Parent) -> None:
            self.parent = Parent

        def open(self) -> None:
            lf.notify("WebSocket opened", lf.Warninglevels.DEBUG)

        def on_message(self, message) -> None:
            lf.notify(f"ws received: {message}", lf.Warninglevels.DEBUG)

            # self.write_message(u"You said: " + message)
            # if message == "exit":
            #     exit()

        def on_close(self) -> None:
            lf.notify("WebSocket closed", lf.Warninglevels.DEBUG)

    ##################################################### ENDWIP #############################################