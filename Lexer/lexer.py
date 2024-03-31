#dependencias
from tokens import *
from utils import is_number, is_boolean

class Token():
  def __init__(self, value: str, token_type: str):
    self._value = value
    self._token_type = token_type
    
  def __repr__(self) -> str:
    return f'({self._token_type}) {self._value}'
  
  @property
  def value(self) -> str: return self._value
  @property
  def token_type(self) -> str: return self._token_type

class Lexer:
  def __init__(self, text: str):
    self._text = text.strip() #cadena
    self._open_cuote = False #saber si hay comillas abiertas
    self._tokens = self.tokenize() #tokens
  
  #tokenizar una cadena
  def tokenize(self) -> list:
    result = []
    token = ''
  
    for char in f'{self._text}$':
      #si llegue al final de la cadena
      if char == '$':
        result.append(self._type_token(token))
        result.append(Token('$', 'end'))
      
      #si hay una comilla sin cerrar
      elif self._open_cuote:
        if char == '"':
          token += char
          self._open_cuote = False
        
        else:
          token += char

      #llegue a un espacio o a un salto de linea
      elif char == ' ' or char == '\n':
        if token != '':
          result.append(self._type_token(token))
          token = ''

      #si el token no es vacio
      elif token != '':
        #si el token es un operador
        if token in OPERATORS:
          if len(token) == 1:
            #todo token de len = 1 mas '=' es un operador
            if char == '=' and not token in ['^', '|', '&']:
              token += char
 
            #si no es el igual ya no es un operador y no puede seguir xq el operador no puede estar dentro de un id
            else:
              result.append(self._type_token(token))
              token = char

          #el maximo len de un operador es 2
          else:
            result.append(self._type_token(token))
            token = char

        #el token no es un operador
        else:
          #lo unico que no puede tener es un operador
          if char in OPERATORS:
            result.append(self._type_token(token))
            token = char

          #agregarle todo lo que vea 
          else:
            token += char

      #el token esta vacio
      else:
        if char == '"':
          self._open_cuote = True
          token += char
        
        else:
          token += char
       
    return result
  
  #determinar el tipo de token
  def _type_token(self, token) -> Token:
    if token == '':
      return Token('', 'epsilon')
    
    elif is_boolean(token):
      return Token(token, 'boolean')
    
    temp = is_number(token)

    if temp[0]:
      return Token(temp[1][1], temp[1][0])

    if token in KEYWORDS:
      return Token(token, 'keyword')

    if token in OPERATORS:
      return Token(token, 'operator')
    
    if token[0] == '"' and token[len(token) - 1] == '"':
      return Token(token, 'string')

    return Token(token, 'id')

  #saber si los tokens son validos
  def _valid_tokens(self):
    if self._open_cuote:
      self._open_cuote = False
      return (False, 'Missed "')
    
    for token in self._tokens:
      if token.token_type == 'id':
        #si empieza con un numero
        if is_number(token.value[0])[0]:
          return (False, f'Invalid syntax: "{token.value}"')
    
        #si contiene un token invalido
        for element in INVALID_ID:
          if element in token.value:
            return (False, f'Invalid syntax: "{token.value}"')
      
    return (True, 'ok')
        
  @property
  def tokens(self) -> list: return self._tokens if self._valid_tokens()[0] else self._valid_tokens()[1]
  
  

