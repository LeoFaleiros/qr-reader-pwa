import http.server
import socketserver
import os

class NoCacheHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Adiciona headers para prevenir cache
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()

    def do_GET(self):
        # Adiciona headers CORS se necessário
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

# Muda o diretório de trabalho para a pasta src
os.chdir(os.path.join(os.path.dirname(__file__), 'src'))

PORT = 8000

Handler = NoCacheHandler
Handler.extensions_map.update({
    ".js": "application/javascript",
    ".manifest": "text/cache-manifest",
})

print(f"Serving at http://localhost:{PORT}")
print("Para acessar no celular, use o IP da sua máquina na rede local")
print("Ctrl+C para parar o servidor")

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("Servindo arquivos da pasta 'src' (com cache desabilitado)")
    httpd.serve_forever()