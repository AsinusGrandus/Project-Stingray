# Standard libs
import multiprocessing

# Pip installs
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.websocket

# Local imports


# NOTES:
# https:// -> wss://
# http:// -> ws://

# class TestHandler(tornado.web.RequestHandler):
#     def get(self):
#         self.write("Test")
#         # # Render html file
#         # self.render("file.html")

#         # # Use variable
#         # variable = self.get_argument("variable")
#         # self.render("home.html", variable=variable)

class IndexHandler(tornado.web.RequestHandler):
    def get(self) -> None:
        self.render("html-pages/index.html")

class LoginHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('<html><body><form action="/test" method="post">'
                   'Name: <input type="text" name="name">'
                   '<input type="submit" value="Sign in">'
                   '</form></body></html>')

    def post(self):
        print(self.get_argument("name"))
        global webserver
        webserver.runCallback()
        self.redirect("/")

        #self.set_secure_cookie("user", self.get_argument("name"))
        #self.redirect("/")

class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        print("WebSocket opened")

    def on_message(self, message):
        print(f"received: {message}")
        self.write_message(u"You said: " + message)
        if message == "exit":
            exit()

    def on_close(self):
        print("WebSocket closed")


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

    # Function to customise the port 
    def setPort(self, port: int) -> None:
        self.port = port        

    # Add SSL to the webserver
    def addSSL(self, certPath : str = None, keyPath : str = None):
        self.certPath = certPath
        self.keyPath = keyPath

    # Test functions for callbacks
    def addCallback(self, functionszz):
        self.function = functionszz

    def runCallback(self):
        self.function()

    # Start the webserver
    def startWebServer(self) -> None:
        self.start()
        self.join()

    # Because Webserver is a child from multiprocessing.Process, run() is the function that gets ran (@FVHCreations explain better)
    def run(self) -> None:
        self.__startWebServer()
    
    # Create the web app
    def __create_app(self) -> tornado.web.Application:
        return tornado.web.Application([
            (r"/", IndexHandler),
            (r"/ws", WebSocketHandler),
            (r"/test", LoginHandler),
        ], 
        debug = self.debug,
        autoreload = self.autoreload)

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
            print("WARNING: SERVER RUNNING WITHOUT SSL")

        http_server.listen(self.port)
        print(f'Server is online on port {self.port}')

        # Start the server
        global webserver
        webserver = self
        tornado.ioloop.IOLoop.current().start()



webserver : Webserver