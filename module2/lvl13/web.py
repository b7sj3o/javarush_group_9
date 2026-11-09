from http.server import BaseHTTPRequestHandler, HTTPServer

from storage import load_users

PORT = 8000


class Handler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        rows = "".join(
            f"<li>{user['name']}: {user['visits']} візитів</li>" for user in load_users().values()
        )
        html = f"<meta charset='utf-8'><h1>Користувачі бота</h1><ul>{rows or 'поки нікого'}</ul>"
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(html.encode("utf-8"))


if __name__ == "__main__":
    print(f"Сторінка працює всередині контейнера на порту {PORT}", flush=True)
    HTTPServer(("0.0.0.0", PORT), Handler).serve_forever()
