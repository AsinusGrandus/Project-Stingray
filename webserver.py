import tornado.ioloop
import tornado.web

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
        self.render("html-pages/button.html")

class ButtonHandler(tornado.web.RequestHandler):
    # https://www.acmesystems.it/tornado_web_server_python_led
    def get(self) -> None:
        print("Button pressed")

class VariableHandler(tornado.web.RequestHandler):
    def get(self) -> None:
        variable = self.get_argument("variable")
        self.render("html-pages/variable.html", variable=variable)

def create_app() -> tornado.web.Application:
    return tornado.web.Application([
        (r"/", DefaultHandler),
        (r"/button", ButtonHandler),
        (r"/variable", VariableHandler),
    ], 
    debug = True,
    autoreload = True)

def startwebserver() -> None:
    app = create_app()
    port = 8888
    app.listen(port)
    print(f'Server is online on port {port}')

    # Start the server
    tornado.ioloop.IOLoop.current().start()
