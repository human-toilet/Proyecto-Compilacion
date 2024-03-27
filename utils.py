def is_number(string: str):
  try:
    parse = int(string)
    return (True, 'int' if not '.' in string else 'float')
  
  except:
    try:
      parse = float(string)
      return (True, 'int' if not '.' in string else 'float')
    
    except:
      return (False, None)

