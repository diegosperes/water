from tornado.ioloop import IOLoop
from tornado.web import Application
from wormhole.api_handler import ApiHandler


def make_app():
    return Application([
        (r'/(\w+)/(\w+)[/]?(\w+)?', ApiHandler)
    ])


if __name__ == "__main__":
    app = make_app()
    app.listen(8000)
    IOLoop.current().start()
