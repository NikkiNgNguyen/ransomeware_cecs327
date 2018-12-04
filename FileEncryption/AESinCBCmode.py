#@author: Jasmin Agustin & Nikki Nguyen
#CECS 378 File Encryption Assignment

import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding

BYTES = 16
BITS = 128
KEY_LENGTH = 32

def Myencrypt(message,key):
    #check key length for 32 bytes
    if len(key) < KEY_LENGTH:
        raise ValueError("ERROR. The key has to be 32 bytes = 256 bits.")
        return
    # convert message from string to 64 bytes / base 64 represents exactly 6 bits of data
    message = message.encode() # default argument results not in the string "utf-8" but NULL which is faster
    iv = os.urandom(BYTES) #generate IV (size of ciphertext)
    #pad message: fill in extra space so it is the same
    #PKCS7: Public Key Cryptography Standards #7: used to sign and/or encrypt messages under a public key infrastructure
    padder = padding.PKCS7(BITS).padder() #nBits = 128, size of ciphertext
    padded_data = padder.update(message) #update(message) adds everything into the context
    #finalize() finishes the operation and obtains the remainder of the data
    padded_data += padder.finalize()

    #encrypt with AES in CBC mode
    #creates cipher instance, takes in algorithm, mode, and backend from Cipher library
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend = default_backend())
    #creates Cipher(encrypt) object
    encryptor = cipher.encryptor()
    #encrypts the plaintext and generates associated ciphertext
    ct = encryptor.update(padded_data)

    #return ciphertext and iv
    return ct, iv

def Mydecrypt(ct,key,iv):

    #decrypt with AES in CBC mode
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    #create decryptor object
    decryptor = cipher.decryptor()
    #generate plaintext
    p = decryptor.update(ct)

    #return plaintext
    return p

def MyfileEncrypt(filepath):
    key = os.urandom(KEY_LENGTH) #generate secret key

    #get file extension
    filename,extension = os.path.splitext(filepath)

    #open, read, close file
    file = open(filepath)
    message = file.read()
    file.close()
    #call Myencrypt
    ct, iv = Myencrypt(message,key)

    #create new text file containing encryption in folder
    userFilepath = raw_input("please enter a save path for the encrypted file (Do not provide file name or extension): ")
    savepathC = userFilepath + "/encrypted_" + extension
    try:
        #create new file and write in binary mode
        newFileC = open(savepathC, 'wb')
        #write ciphertext to new file
        newFileC.write(ct)
        #close file
        newFileC.close()
    except Exception:
        print("invalid file path \n")
        userFilepath = raw_input("please enter a save path for the encrypted file (Do not provide file name or extension): ")


    #return ciphertext message, key, iv, and extension to call in MyfileDecrypt
    return ct, key, iv, extension

#inverse of MyfileEncrypt
def MyfileDecrypt(ct,key,iv,extension):

    #get plaintext
    p = Mydecrypt(ct,key,iv)

    # convert message from 64 bytes to string
    p = p.decode()

    #create new text file containing decryption in folder
    userFilepath = raw_input("please enter a save path for the decrypted file (Do not provide file name or extension): ")
    savepathD = userFilepath + "/decrypted_" + extension

    try:
        #create new file and write in binary mode
        newFileD = open(savepathD, 'wb')
        #write plaintext to new file
        newFileD.write(p)
        #close file
        newFileD.close()
    except Exception:
        print("invalid file path \n")
        userFilepath = raw_input("please enter a save path for the encrypted file (Do not provide file name or extension): ")

    #return the plaintext message
    return p

def menu():
    userInput = int(input("File Encryption \n"
                          "1. Encrypt & Decrypt a ready file \n"
                          "2. Encrypt & Decrypt your own message \n"
                          "3. Exit \n"))
    return userInput

def main():
    key = os.urandom(KEY_LENGTH)
    while True:
        userInput = menu()
        if userInput == 1:
            thisFilepath = raw_input("enter an absolute file path: ")
            try:
                ct, iv, key, extension = MyfileEncrypt(thisFilepath)
                print("encryption ready")
                p = MyfileDecrypt(ct, iv, key, extension)
                print("decryption ready \n")
            except Exception:
                print("invalid file path \n")
        elif userInput == 2:
            thisFilepath = raw_input("enter an .txt file path: ")
            try:
                textfile = open(thisFilepath, 'w')
                fileMessage = raw_input("enter a message you want to encrypt: ")
                textfile.write(fileMessage)
                textfile.close()
                ct, iv, key, ext = MyfileEncrypt(thisFilepath)
                print("encryption ready")
                p = MyfileDecrypt(ct, iv, key, ext)
                print("decryption ready \n")
            except Exception:
                print("invalid file path \n")
        elif userInput == 3:
            raise SystemExit

main()

'''
NOTES:
Padding is a way to take data that may or may not be a multiple
the block size for a cipher and extend it out so that it is. This is
required for many block cipher modes as they require the data to be
encrypted to be an exact multiple of the block size

'''
