# Standard libs
import multiprocessing

# Pip installs
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

class DefaultHandler(tornado.web.RequestHandler):
    def get(self) -> None:
        self.render("html-pages/index.html")

class ButtonHandler(tornado.web.RequestHandler):
    # https://www.acmesystems.it/tornado_web_server_python_led
    def get(self) -> None:
        print("Button pressed")

class VariableHandler(tornado.web.RequestHandler):
    def get(self) -> None:
        variable = self.get_argument("variable")
        self.render("html-pages/variable.html", variable=variable)

class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        print("WebSocket opened")

    def on_message(self, message):
        print(f"received: {message}")
        self.write_message(u"You said: " + message)

    def on_close(self):
        print("WebSocket closed")



class Webserver(multiprocessing.Process):

    def __init__(self, port : int, devmode : bool = False, daemon : bool = True) -> None:

        multiprocessing.Process.__init__(self, daemon=daemon)

        self.port = port
        self.devmode = devmode
        self.debug = self.devmode
        self.autoreload = self.devmode

    def startWebServer(self) -> None:
        self.start()
        self.join()

    def run(self) -> None:
        self.__startWebServer()
    
    def __create_app(self) -> tornado.web.Application:
        return tornado.web.Application([
            (r"/", DefaultHandler),
            (r"/ws", WebSocketHandler),
        ], 
        debug = self.debug,
        autoreload = self.autoreload)

    def __startWebServer(self) -> None:
        app = self.__create_app()
        app.listen(self.port)
        print(f'Server is online on port {self.port}')

        # Start the server

        tornado.ioloop.IOLoop.current().start()