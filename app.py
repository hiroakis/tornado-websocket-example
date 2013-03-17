from tornado import websocket, web, ioloop
import tornado
import json

cl = []

class IndexHandler(tornado.web.RequestHandler):

    def get(self):
        self.render("index.html")

class SocketHandler(tornado.websocket.WebSocketHandler):

    def open(self):
        if self not in cl:
            cl.append(self)

    def on_close(self):
        if self in cl:
            cl.remove(self)

class ApiHandler(tornado.web.RequestHandler):

    @tornado.web.asynchronous
    def get(self, *args):
        self.finish()
        id = self.get_argument("id")
        value = self.get_argument("value")
        data = {"id": id, "value" : value}
        data = json.dumps(data)
        for c in cl:
            c.write_message(data)

    @tornado.web.asynchronous
    def post(self):
        pass

app = tornado.web.Application([
    (r'/', IndexHandler),
    (r'/ws', SocketHandler),
    (r'/api', ApiHandler),
    (r'/(favicon.ico)', tornado.web.StaticFileHandler, {'path': '../'}),
    (r'/(rest_api_example.png)', tornado.web.StaticFileHandler, {'path': './'}),
])

if __name__ == '__main__':
    app.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
