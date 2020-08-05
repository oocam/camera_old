from .server import app


def start_server(host="0.0.0.0", port=8000):
    app.run(host, port)
