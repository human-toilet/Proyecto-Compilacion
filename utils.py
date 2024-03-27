def is_number(string: str):
  try:
    parse = int(string)
    return (True, 'int')
  
  except:
    try:
      parse = float(string)
      return (True, 'float')
    
    except:
      return (False, None)
    


