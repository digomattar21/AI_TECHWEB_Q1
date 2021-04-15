import socket
from pathlib import Path
from utils import extract_route, read_file
from views import index, edit, notfound
from database import Database, Note

CUR_DIR = Path(__file__).parent
print(CUR_DIR)
SERVER_HOST = '0.0.0.0'
SERVER_PORT = 8080
db = Database('banco')

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen()

print(
    f'Servidor escutando em (ctrl+click): http://{SERVER_HOST}:{SERVER_PORT}')

while True:
  client_connection, client_address = server_socket.accept()

  request = client_connection.recv(1024).decode()

  route = extract_route(request)
  filepath = CUR_DIR / route
  print('route', route)
  if filepath.is_file():
    response = read_file(filepath)
  elif route == '':
    response = index(request, db)
  elif route == 'edit':
    response = edit(request, db)
  elif route:
    response = notfound(request,db)
  

  client_connection.sendall('HTTP/1.1 200 OK\n\n'.encode() + response)


  client_connection.close()

server_socket.close()
