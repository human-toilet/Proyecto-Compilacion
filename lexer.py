#dependencias
from tokens import *
from utils import is_number

#token
class Token():
  def __init__(self, value: str, token_type: str):
    self.__value = value
    self.__token_type = token_type
    
  def __repr__(self) -> str:
    return f'{self.__token_type}({self.__value})'
  
  @property
  def value(self) -> str: return self.__value
  @property
  def token_type(self) -> str: return self.__token_type

#tokenizar una cadena
def tokenize(string: str) -> list:
  string = string.strip()
  result = []
  token = ''
  
  for char in f'{string}$':
    #si llegue al final de la cadena
    if char == '$':
      if token.strip() != '':
        result.append(type_token(token))
    
    #llegue a un espacio o a un salto de linea
    elif char == ' ' or char == '\n':
      if token != '':
        result.append(type_token(token))
        token = ''
    
    #si el token no es vacio
    elif token != '':
      #si el token es un operador
      if token in OPERATORS:
        if len(token) == 1:
          #todo token de len = 1 mas '=' es un operador
          if char == '=':
            token += char

          #si no es el igual ya no es un operador y no puede seguir xq el operador no puede estar dentro de un id
          else:
            result.append(type_token(token))
            token = char
        
        #el maximo len de un operador es 2
        else:
          result.append(type_token(token))
          token = char
      
      #si el token es un numero 
      elif is_number(token)[0]:
        #un numero concatenado con un numero sigue sindo un numero
        if is_number(char)[0]:
          token += char
          
        #si tiene una vez solamente '.'
        elif len(list(filter(lambda x: x == '.', token))) == 1:
          #si se le concatena un numero seria un float
          if is_number(char)[0]:
            token += char
          
          #ya no es un numero y no puede ser un id xq un id no puede empezar con un numero
          else:
            result.append(type_token(token))
            token = char

        #si no tiene '.' al agregarselo al final es un float
        elif char == '.':
          token += char
        
        #ya no es un numero
        else:
          result.append(type_token(token))
          token = char
      
      #el token no es un numero
      else:
        #lo unico que no puede tener es un operador
        if char in OPERATORS:
          result.append(type_token(token))
          token = char
        
        #agregarle todo lo que vea 
        else:
          token += char
    
    #el token esta vacio
    else:
      token += char
  
  return result
       
#determinar el tipo de token           
def type_token(token) -> Token:
  temp = is_number(token)
  
  if temp[0]:
    return Token(temp[1][1], temp[1][0])
  
  if token in KEYWORDS:
    return Token(token, 'keyword')
  
  if token in OPERATORS:
    return Token(token, 'operator')
  
  return Token(token, 'id')
