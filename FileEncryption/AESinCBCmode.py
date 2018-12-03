#@author: Jasmin Agustin & Nikki Nguyen
#CECS 378 File Encryption Assignment

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
    iv = os.urandom(nBytes) #generate IV (size of ciphertext)
    #pad message: fill in extra space so it is the same
    #PKCS7: Public Key Cryptography Standards #7: used to sign and/or encrypt messages under a public key infrastructure
    padder = padding.PKCS7(nBits).padder() #nBits = 128, size of ciphertext
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
    key = os.urandom(keyLength) #generate secret key

    #get file extension
    filebase,extension = os.path.splitext(filepath)

    #open, read, close file
    file = open(filepath)
    message = file.read()
    file.close()
    #call Myencrypt
    ct, iv = Myencrypt(message,key)

    #create new text file containing encryption in folder
    savepathC = '/Users/NikkiNguyen/Desktop/usedFiles/encrypt'+ filebase + extension
    #create new file and write in binary mode
    newFileC = open(savepathC, 'wb')
    #write ciphertext to new file
    newFileC.write(ct)
    #close file
    newFileC.close()

    #return ciphertext message, key, iv, and extension to call in MyfileDecrypt
    return ct, key, iv, extension

#inverse of MyfileEncrypt
def MyfileDecrypt(ct,key,iv,extension):

    #get plaintext
    p = Mydecrypt(ct,key,iv)

    # convert message from 64 bytes to string
    p = p.decode()

    #create new text file containing decryption in folder
    savepathD = '/Users/NikkiNguyen/Desktop/usedFiles/decrypt' + extension
    #create variable for full file path
    #create new file and write in binary mode
    newFileD = open(savepathD, 'wb')
    #write plaintext to new file
    newFileD.write(p)
    #close file
    newFileD.close()
    #return the plaintext message
    return p

def main():
    newTxtFile = open(filepathTxt, "w")
    fileMess = raw_input("enter a message: ")
    newTxtFile.write(fileMess)
    newTxtFile.close()
    #Encrypt text file, print in console
    C, IV, tag, EncKey, HMACkey, ext = MyfileEncryptMAC(filepathTxt)
    print("ct: " + C)
    print("Encrypted text file ready ")

    #Decrypt file, print in console
    p = MyfileDecryptMAC(C, IV, EncKey, HMACkey, ext, tag)
    print("Decrypted text file ready ")


'''
NOTES:
Padding is a way to take data that may or may not be a multiple
the block size for a cipher and extend it out so that it is. This is
required for many block cipher modes as they require the data to be
encrypted to be an exact multiple of the block size

'''
