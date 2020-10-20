def encrypt_vigenere(plaintext: str, keyword: str) -> str:
  """
  Encrypts plaintext using a Vigenere cipher.
  >>> encrypt_vigenere("PYTHON", "A")
  'PYTHON'
  >>> encrypt_vigenere("python", "a")
  'python'
  >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
  'LXFOPVEFRNHR'
  """
  ciphertext = []
  textlen = list(plaintext)
  keylen = list(keyword.lower())
  length = len(keylen)
  i = 0
  for letter in textlen:
    letter = ord(letter)
    if ord('a') <= letter <= ord('z') or ord('A') <= letter <= ord('Z'):
      if ord('A') <= letter <= ord('Z'):
        if ord('Z') - (ord(keylen[i]) - ord('a')) < letter <= ord('Z'):
          letter -= 26
        letter += ord(keylen[i]) - ord('a')
      elif ord('a') <= letter <= ord('z'):
        if ord('z') - (ord(keylen[i]) - ord('a')) < letter <= ord('z'):
          letter -= 26
        letter += ord(keylen[i]) - ord('a')
      letter = chr(letter)
      ciphertext += letter
    else:
      letter = chr(letter)
      ciphertext += letter
    i += 1
    if i == length:
      i = 0
  return ("".join(ciphertext)) 


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
  """
  Decrypts a ciphertext using a Vigenere cipher.
  >>> decrypt_vigenere("PYTHON", "A")
  'PYTHON'
  >>> decrypt_vigenere("python", "a")
  'python'
  >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
  'ATTACKATDAWN'
  """
  plaintext = []
  textlen = list(ciphertext)
  keylen = list(keyword.lower())
  length = len(keylen)
  i = 0
  for letter in textlen:
    letter = ord(letter)
    if ord('a') <= letter <= ord('z') or ord('A') <= letter <= ord('Z'):
      if ord('A') <= letter <= ord('Z'):
        if ord('A') <= letter < ord('A') + (ord(keylen[i]) - ord('a'):
          letter += 26
        letter -= ord(keylen[i]) - ord('a')
      elif ord('a') <= letter <= ord('z'):
        if ord('a') <= letter < ord('a') + (ord(keylen[i]) - ord('a')):
          letter += 26
        letter -= ord(keylen[i]) - ord('a')
      letter = chr(letter)
      plaintext += letter
    else:
      letter = chr(letter)
      plaintext += letter
    i += 1
    if i == length:
      i = 0
  return ("".join(plaintext))