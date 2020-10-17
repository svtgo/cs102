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
    for i in range(len(plaintext)): 
        x=(ord(plaintext[i])+ord(keyword[i]))%26
        x+=ord('A') 
        ciphertext.append(chr(x))
    return("".join(ciphertext))


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
    for i in range(len(ciphertext)): 
        x=(ord(ciphertext[i])-ord(keyword[i])+26)%26
        x+= ord('A') 
        plaintext.append(chr(x)) 
    return("".join(plaintext))
