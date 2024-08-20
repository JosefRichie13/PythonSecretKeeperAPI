import shortuuid 
import time 
import html
import re
import cryptocode 
import string
import random



# Generates a UUID, which is used as an ID
def generateID():
    return shortuuid.uuid()



# Sanitizes the string to avoid XSS vulnerabilities
# Also removes any double spaces in between the strings
def sanitizeString(inputString):
    santizedString = html.escape(inputString, quote=False)
    santizedString = re.sub(' +', ' ', santizedString)
    return santizedString



# Generates the current time in Epoch
def currentEpochTime():
    return int(time.time())



# Encrypts a Secret and returns it
def encryptASecret(ID, secret, timestamp):
    keyToEncrypt = ID + str(timestamp)
    return cryptocode.encrypt(secret, keyToEncrypt)



# Decrypts a Secret and returns it
def decryptASecret(ID, secret, timestamp):
    keyToDecrypt = ID + str(timestamp)
    return cryptocode.decrypt(secret, keyToDecrypt)



# Generates a random 10 digit string
def genRandoStr(): 
    N = 10
    return ''.join(random.choices(string.ascii_letters, k=N))



# Scrambles the key
def keyScrambler(secretKey):
    secretKey = secretKey[:-10]
    return secretKey[20:]