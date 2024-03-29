def is_number(string: str):
  try:
    parse = int(string)
    return (True, ('int', parse))
  
  except:
    try:
      parse = float(string)
      return (True, ('float', parse))
    
    except:
      return (False, None)
    


