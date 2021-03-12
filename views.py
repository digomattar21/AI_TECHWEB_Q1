from utils import load_data, load_template
from database import Note
import urllib.parse

def index(request,db):
# A string de request sempre começa com o tipo da requisição (ex: GET, POST)
  if request.startswith('POST'):
    request = request.replace('\r', '') # Remove caracteres indesejados
# Cabeçalho e corpo estão sempre separados por duas quebras de linha
    partes = request.split('\n\n')
    corpo = partes[1]
    params = {}
    p1 = partes[1]
# Preencha o dicionário params com as informações do corpo da requisição
# O dicionário conterá dois valores, o título e a descrição.
# Posteriormente pode ser interessante criar uma função que recebe a
# requisição e devolve os parâmetros para desacoplar esta lógica.
# Dica: use o método split da string e a função unquote_plus
    print('p1', p1)
    if (p1.startswith('id')):
      idd = p1[3:]
      db.delete(idd)
    elif (p1.startswith('update')):
      newNote = {}
      for chave_valor in p1.split('&'):
        if 'titulo' in chave_valor:
          titulo = chave_valor[7:]
          titulo = urllib.parse.unquote_plus(titulo)
          newNote['title'] = titulo
        elif 'id' in chave_valor:
          aiD = chave_valor[3:]
          newNote['id'] = aiD
        elif 'detalhes' in chave_valor:
          detalhes = chave_valor[9:]
          detalhes = urllib.parse.unquote_plus(detalhes)
          newNote['content'] = detalhes
      db.update(titulo, detalhes, aiD)

    else:
      for chave_valor in corpo.split('&'):
        if 'titulo' in chave_valor:
          titulo = chave_valor[7:]
          titulo = urllib.parse.unquote_plus(titulo)
          params['titulo'] = titulo
        

        elif 'detalhes' in chave_valor:
          detalhes = chave_valor[9:]
          detalhes = urllib.parse.unquote_plus(detalhes)
          params['detalhes'] = detalhes

      note = Note(title=params['titulo'], content=params['detalhes'])
      db.add(note)

# O RESTO DO CÓDIGO DA FUNÇÃO index CONTINUA DAQUI PARA BAIXO..
  note_template = load_template('components/note.html')
  notes_li = [
  note_template.format(id=dados.id, title=dados.title, details=dados.content)
  for dados in load_data(db)
  ]
  notes = '\n'.join(notes_li)

  return load_template('index.html').format(notes=notes).encode()

def edit (request,db):
  if request.startswith('POST'):
    request = request.replace('\r', '') 
    partes = request.split('\n\n')
    corpo = partes[1]
    params = {}
    print('corpo', corpo)
    idRaw = corpo.split('&')[1]
    id= idRaw[3:]

    noteEditTemplate = load_template('components/noteEdit.html')
    note = db.get_one(id)
    for n in note:
      [iddd, tituloo, contentt] = n

    notes=noteEditTemplate.format(id=iddd, title=tituloo, detalhes=contentt)

  return load_template('edit.html').format(noteEdit=notes).encode()

    