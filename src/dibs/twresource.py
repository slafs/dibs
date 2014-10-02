import crochet
crochet.setup()

from twisted.web import server, resource  # , client
# from twisted.internet import defer


class Root(resource.Resource):

    def __init__(self, wsgi_resource):
        resource.Resource.__init__(self)
        self.wsgi_resource = wsgi_resource

    def getChild(self, path, request):
        path0 = request.prepath.pop(0)
        request.postpath.insert(0, path0)
        return self.wsgi_resource


def _format_sse(msg, event=None):
    data = []
    if event is not None:
        data.append("event: {}\n".format(event))
    for line in msg.splitlines():
        data.append("data: {}\n".format(line))
    data.append("\n")
    return "".join(data)


class SSEResource(resource.Resource):

    def __init__(self):
        resource.Resource.__init__(self)
        self._listeners = []

    def add_listener(self, request):
        print "listener connected", request
        self._listeners.append(request)
        request.notifyFinish().addBoth(self.remove_listener, request)

    def remove_listener(self, reason, listener):
        print "listener disconnected", listener, "reason", reason
        self._listeners.remove(listener)

    @crochet.run_in_reactor
    def broadcast_message(self, msg, event=None):
        self.broadcast_message_async(msg, event)

    def broadcast_message_async(self, msg, event=None):
        print 'broadcasting'
        sse = _format_sse(msg, event)
        for listener in self._listeners:
            listener.write(sse)

    def render_GET(self, request):
        request.setHeader("Content-Type", "text/event-stream")
        self.add_listener(request)
        return server.NOT_DONE_YET


sse_resource = SSEResource()
