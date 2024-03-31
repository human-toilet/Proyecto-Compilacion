#dependencias
from tokens import *
from utils import *

class Token():
  def __init__(self, value: str, token_type: str, line = None, col = None):
    self.__value = value
    self.__token_type = token_type
    self.__line = line
    self.__col = col
    
  def __repr__(self) -> str:
    return f'({self.__token_type}) {self.__value}'
  
  @property
  def value(self) -> str: return self.__value
  @property
  def token_type(self) -> str: return self.__token_type
  @property
  def line(self) -> int: return self.__line
  @property
  def col(self) -> int: return self.__col

class Lexer:
  def __init__(self, text: str):
    self.__text = text.strip() #cadena
    self.__open_cuote = False #saber si hay comillas abiertas
    self.__current_line = 1 #linea donde estoy
    self.__current_col = 0 #columna donde estoy
    self.__tokens = self.__tokenize() #tokens
      
  #tokenizar una cadena
  def __tokenize(self) -> list:
    result = []
    token = ''
  
    for char in f'{self.__text}$':
      #si llegue al final de la cadena
      if char == '$':
        result.append(self.__type_token(token))
        result.append(Token('$', 'end'))
        self.__current_line = 0
        self.__current_col = 0      
        
      #si hay una comilla sin cerrar
      elif self.__open_cuote:
        if char == '"':
          self.__current_col += 1
          token += char
          self.__open_cuote = False
        
        else:
          self.__current_col += 1
          token += char

      #llegue a un espacio o a un salto de linea
      elif char == ' ' or char == '\n':
        if token != '' and char == '\n':
          result.append(self.__type_token(token))
          self.__current_line = self.__current_line + 1
          self.__current_col = 0         
          token = ''
        
        elif token == '' and char == '\n':
          self.__current_line = self.__current_line + 1
          self.__current_col += 1   
               
        elif token != '':
          result.append(self.__type_token(token))
          self.__current_col += 1
          token = ''
          
        else:
          self.__current_col += 1
          
      #si el token no es vacio
      elif token != '':
        #si el token es un operador
        if token in OPERATORS:
          if len(token) == 1:
            #todo token de len = 1 mas '=' es un operador
            if char == '=' and not token in ['^', '|', '&']:
              self.__current_col += 1
              token += char
 
            #si no es el igual ya no es un operador y no puede seguir xq el operador no puede estar dentro de un id
            else:
              result.append(self.__type_token(token))
              self.__current_col += 1
              token = char

          #el maximo len de un operador es 2
          else:
            result.append(self.__type_token(token))
            self.__current_col += 1
            token = char

        #el token no es un operador
        else:
          #lo unico que no puede tener es un operador
          if char in OPERATORS:
            result.append(self.__type_token(token))
            self.__current_col += 1
            token = char

          #agregarle todo lo que vea 
          else:
            self.__current_col += 1
            token += char

      #el token esta vacio
      else:
        if char == '"':
          self.__current_col += 1         
          self.__open_cuote = True
          token += char
        
        else:
          self.__current_col += 1          
          token += char
       
    return result
  
  #determinar el tipo de token
  def __type_token(self, token: str):
    #si es un booleano
    if is_boolean(token):
      return Token(token, '<boolean>')
    
    temp = is_number(token)
    #si es un numero
    if temp[0]:
      return Token(temp[1][1], temp[1][0], self.__current_line, self.__current_col)

    #si es una keyword
    if token in KEYWORDS:
      return Token(token, '<keyword>', self.__current_line, self.__current_col)

    #si es un operador
    if token in OPERATORS:
      return Token(token, '<operator>', self.__current_line, self.__current_col)  

    #si es un string
    if token[0] == '"' and token[len(token) - 1] == '"':
      return Token(token, '<string>', self.__current_line, self.__current_col) 
    
    #es un id
    return Token(token, '<id>', self.__current_line, self.__current_col) 
  
  #control de errores
  def __valid_tokens(self):
    if self.__open_cuote:
      self.__open_cuote = False
      return (False, 'Missed "')
    
    for token in self.__tokens:
      if token.token_type == '<id>':
        #si empieza con un numero
        if is_number(token.value[0])[0]:
          return (False, Exception(f'Invalid syntax: "{token.value}" line {token.line}; col {token.col}'))
    
        #si contiene un token invalido
        for element in INVALID_ID:
          if element in token.value:
            return (False, Exception(f'Invalid syntax: "{token.value}" line {token.line}; col {token.col}'))
      
    return (True, 'ok')
        
  @property
  def tokens(self): return self.__tokens if self.__valid_tokens()[0] else self.__valid_tokens()[1]
  
  

