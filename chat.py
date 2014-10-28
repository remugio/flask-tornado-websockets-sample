
# -*- coding: utf-8 -*-
"""
    Simple sockjs-tornado chat application. By default will listen on port 8080.
"""
import os
import tornado.ioloop
import tornado.web
from tornado.web import Application, FallbackHandler
from tornado.wsgi import WSGIContainer
import sockjs.tornado
import json
curvote = 0

class ChatConnection(sockjs.tornado.SockJSConnection):
    """Chat connection implementation"""
    # Class level variable
    participants = set()

    def on_open(self, info):
        # Send that someone joined
        self.broadcast(self.participants, "Someone joined.")
        self.send("{\"curvote\":%d}" % curvote)

        # Add client to the clients list
        self.participants.add(self)

    def on_message(self, message):
        # Broadcast message
        print json.dumps(json.loads(message), indent=2)
        self.broadcast(self.participants, json.dumps(json.loads(message)))

    def on_close(self):
        # Remove client from the clients list and broadcast leave message
        self.participants.remove(self)

        self.broadcast(self.participants, "Someone left.")

from flask import Flask

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.debug = True

from flask import render_template

@app.route('/')
def index():
    print 'flask hit'
    return render_template('index.html')

@app.errorhandler(404)
def page_not_found(e):
    return('''
  <h1>Page Not Found</h1>
  <p>What you were looking for is just not there.
  <p><a href="/">go somewhere nice</a>
'''), 404

if __name__ == "__main__":
    import logging
    logging.getLogger().setLevel(logging.DEBUG)

    # 1. Create chat router
    ChatRouter = sockjs.tornado.SockJSRouter(ChatConnection, '/chat')
    
    wsgi_app = WSGIContainer(app)

    # 2. Create Tornado application
    application = tornado.web.Application(
            ChatRouter.urls + [(r'.*', FallbackHandler, dict(fallback=wsgi_app))]
    )

    # 3. Make Tornado app listen on port 8080
    application.listen(8080)

    # 4. Start IOLoop
    tornado.ioloop.IOLoop.instance().start()
