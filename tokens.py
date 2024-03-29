#palabras claves y operadores del lenguaje
KEYWORDS: set = set()
OPERATORS: set = set()
INVALID_ID: set = set()

with open('assets/keywords.txt', 'r') as f:
  for line in f.readlines():
    KEYWORDS.add(line.replace('\n', ''))

with open('assets/operators.txt', 'r') as f:
  for line in f.readlines():
    OPERATORS.add(line.replace('\n', ''))
    
with open('assets/invalid_id.txt', 'r') as f:
  for line in f.readlines():
    INVALID_ID.add(line.replace('\n', ''))
    

  