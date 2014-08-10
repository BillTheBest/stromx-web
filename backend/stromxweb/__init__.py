# -*- coding: utf-8 -*-

import httplib
import os
import re
import tornado.escape
import tornado.ioloop
import tornado.web
import tornado.websocket

import model

class ItemsHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "http://localhost:9000")
    
    def options(self, *args, **kwargs):
        self.set_header('Access-Control-Allow-Headers', 
                        ('Content-Type, Depth, User-Agent, X-File-Size, '
                         'X-Requested-With, X-Requested-By, If-Modified-Since, '
                         'X-File-Name, Cache-Control'))
        self.set_header('Access-Control-Allow-Methods', 
                        'GET,PUT,POST,DELETE,OPTIONS')
        self.set_status(204)
        self.finish()
    
    def initialize(self, items):
        self.items = items
        
    def get(self, index = None):
        try:
            if index == None:
                query = tornado.escape.url_unescape(self.request.query)
                data = self.items.data
                if query != "":
                    ids = [str(index) for index in
                           re.findall('ids\[\]=(\d+)', query)]
                    resourceName = data.keys()[0]
                    items = data.values()[0]
                    filteredItems = [item for item in items
                                     if item['id'] in ids]
                    data = {resourceName: filteredItems}
                json = tornado.escape.json_encode(data)
            else:
                json = tornado.escape.json_encode(self.items[index].data)
            self.write(json) 
        except KeyError:
            self.set_status(httplib.NOT_FOUND)
    
    def put(self, index):
        try:
            data = tornado.escape.json_decode(self.request.body)
            item = self.items.set(index, data)
            json = tornado.escape.json_encode(item)
            self.write(json)  
        except KeyError:
            self.set_status(httplib.NOT_FOUND)
        
    def post(self):
        data = tornado.escape.json_decode(self.request.body)
        item = self.items.addData(data)
        json = tornado.escape.json_encode(item)
        self.write(json)  
    
    def delete(self, index):
        try:
            self.items.delete(index)
            self.write("null")
        except KeyError:
            self.set_status(httplib.NOT_FOUND)
    
class ErrorSocket(tornado.websocket.WebSocketHandler):
    def initialize(self, errors):
        self.errors = errors
        
    def open(self):
        self.errors.errorHandlers.append(self.sendError)
    
    def on_close(self):
        self.errors.errorHandlers.remove(self.sendError)
        
    def doSend(self, error):
        json = tornado.escape.json_encode(error.data)
        self.write_message(json)
        
    def sendError(self, error):
        loop = tornado.ioloop.IOLoop.instance()
        loop.add_callback(lambda: self.doSend(error))

def start(files):
    appModel = model.Model(files)
    serverDir = os.path.dirname(os.path.abspath(__file__))
    staticDir = os.path.join(serverDir, "static")
    application = tornado.web.Application(
        [
            (r"/", tornado.web.RedirectHandler,
             {"url": "/static/index.html"}),
            (r"/files", ItemsHandler, dict(items = appModel.files)),
            (r"/files/([0-9]+)", ItemsHandler, dict(items = appModel.files)),
            (r"/streams", ItemsHandler, dict(items = appModel.streams)),
            (r"/streams/([0-9]+)", ItemsHandler, dict(items = appModel.streams)),
            (r"/operators", ItemsHandler, dict(items = appModel.operators)),
            (r"/operators/([0-9]+)", ItemsHandler,
             dict(items = appModel.operators)),
            (r"/parameters", ItemsHandler, dict(items = appModel.parameters)),
            (r"/parameters/([0-9]+)", ItemsHandler,
             dict(items = appModel.parameters)),
            (r"/enumDescriptions", ItemsHandler, 
             dict(items = appModel.enumDescriptions)),
            (r"/enumDescriptions/([0-9]+)", ItemsHandler,
             dict(items = appModel.enumDescriptions)),
            (r"/connections", ItemsHandler, 
             dict(items = appModel.connections)),
            (r"/connections/([0-9]+)", ItemsHandler,
             dict(items = appModel.connections)),
            (r"/connectors", ItemsHandler, 
             dict(items = appModel.connectors)),
            (r"/connectors/([0-9]+)", ItemsHandler,
             dict(items = appModel.connectors)),
            (r"/threads", ItemsHandler, 
             dict(items = appModel.threads)),
            (r"/threads/([0-9]+)", ItemsHandler,
             dict(items = appModel.threads)),
            (r"/error_socket", ErrorSocket, dict(errors = appModel.errors)),
            (r"/download/(.*)", tornado.web.StaticFileHandler,
             {"path": files}),
        ],
        static_path = staticDir
    )
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
    
def stop():
    ioLoop = tornado.ioloop.IOLoop.instance()
    ioLoop.add_callback(ioLoop.stop)