#!/usr/bin/env python3
import http.server
import socketserver
import os
import sys

PORT = 8000
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def end_headers(self):
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        self.send_header('Access-Control-Allow-Origin', '*')
        return super().end_headers()

if __name__ == '__main__':
    handler = MyHTTPRequestHandler
    with socketserver.TCPServer(("", PORT), handler) as httpd:
        print(f"")
        print(f"╔════════════════════════════════════╗")
        print(f"║    KAPITAL - Servidor Local       ║")
        print(f"╚════════════════════════════════════╝")
        print(f"")
        print(f"✅ Servidor corriendo en http://localhost:{PORT}")
        print(f"📁 Directorio: {DIRECTORY}")
        print(f"")
        print(f"Abre en tu navegador:")
        print(f"  → http://localhost:{PORT}/kapital.html")
        print(f"")
        print(f"Presiona Ctrl+C para detener")
        print(f"")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print(f"")
            print(f"Servidor detenido ✓")
            sys.exit(0)
