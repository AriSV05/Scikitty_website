from http.server import BaseHTTPRequestHandler, HTTPServer
import scikitty_funtions as sk

class MiHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Escribir la respuesta del servidor
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        #df = sk.read_csv('playTennis.csv')
        #X,y = sk.getX_Y(df)
        #X_train, X_test, y_train, y_test = sk.splitX_Y(X,y)

        #model = sk.decide_and_train_tree(X_train,y_train)

        accuracy, recall, precision, f_score = sk.cal_metrics(X_test,y_test, model)

        #sk.image_tree_model(X,y,model)

        contenido = "<html><body><h1>Hola, mundo!</h1></body></html>"

        # TODO Contenido de la respuesta
        
        
        # Enviar la respuesta al cliente
        self.wfile.write(contenido.encode('utf-8'))

# Configurar y ejecutar el servidor
def iniciar_servidor(port=8000):
    server_address = ('', port)
    httpd = HTTPServer(server_address, MiHandler)
    print(f'Servidor iniciado en el puerto {port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    iniciar_servidor()
    

