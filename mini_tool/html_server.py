import http.server
import socketserver

DIRECTORY = "./"
PORT = 38121


class SimpleHTTPRequestHandlerWithDirectory(http.server.SimpleHTTPRequestHandler):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)


def run_server(port=PORT):
    # 创建并启动服务器
    with socketserver.TCPServer(("", port), SimpleHTTPRequestHandlerWithDirectory) as httpd:
        print("Serving at port", port)
        httpd.serve_forever()


if __name__ == '__main__':
    run_server()
