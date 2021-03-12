import json

def extract_route(request):
  req = request.split('\n')
  for line in req:
    if 'GET' in line or 'POST' in line:
      split = line.split(' ')
      string = split[1]
      return string[1:]

def read_file(file):
  cd = file.suffix
  if cd == ".js" or cd == ".txt" or cd == ".html" or cd == ".css":
    with open (file, 'r', encoding= 'utf-8') as f:
      read = bytes(f.read(), 'utf-8')
  else:
    with open (file, 'rb') as p:
      read = p.read()
  return read

def load_data(db):
  return db.get_all()
  

def load_template(file):
  caminho = "templates/" + file
  with open (caminho, 'r') as f:
    read = f.read()
  return read



