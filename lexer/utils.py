#si es un numero devuelve el tipo
def is_number(string: str):
  try:
    parse = int(string)
    return (True, ('<number>', parse))
  
  except:
    try:
      parse = float(string)
      return (True, ('<number>', parse))
    
    except:
      return (False, None)
 
#saber si es un boolean
def is_boolean(string: str):
  return string == 'true' or string == 'false'   


