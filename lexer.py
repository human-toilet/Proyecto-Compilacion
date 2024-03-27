from load import *
from utils import is_number

def tokenize(string: str) -> list:
  result = []
  token = ''
  
  for char in f'{string}$':
    if char == '$':
      if token != '':
        result.append(type_token(token))
    
    elif char == ' ' or char == '\n':
      result.append(type_token(token))
      token = ''
    
    elif token != '':
      if token in OPERATORS:
        if len(token) == 1:
          if char == '=':
            token += char

          else:
            result.append(type_token(token))
            token = char
        
        else:
          result.append(type_token(token))
          token = char
      
      else:
        if char in OPERATORS:
          result.append(type_token(token))
          token = char
        
        else:
          token += char
        
    else:
      token += char
  
  return result
           
def type_token(token) -> str:
  if is_number(token)[0]:
    return is_number(token[1])
  
  if token in KEYWORDS or token in OPERATORS:
    return token
  
  return 'id'

