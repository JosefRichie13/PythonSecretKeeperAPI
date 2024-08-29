import sqlite3
from fastapi import FastAPI, Response, status
from pydantic import BaseModel
from helpers import *
from fastapi.responses import FileResponse


app = FastAPI()

@app.get("/")
def landingPage():
    return FileResponse("SecretKeeper.html")



# Body for POST
class addASecretData(BaseModel):
    secret : str
    time : int


# Adds a secret, requires a POST body with 2 params, The secret and the time to expire in seconds.
@app.post("/keepASecret")
def storeASecret(addASecretBody: addASecretData):

    # Checks if the time supplied is a whole number
    if addASecretBody.time < 0:
        return {"status" : "The provided time is a negative number, please provide a whole number"}

    # Connects to the DB
    postConnection = sqlite3.connect("SECRETKEEPER.db")
    cur = postConnection.cursor()

    # Stores a UUID, Timestamp and a Key
    # Secret is encrypted and Key is scrambled
    generatedID = generateID()
    generatedTimestamp = currentEpochTime()
    generatedSecretKey = generateID() + generateID()
    encryptedSecret = encryptASecret(generatedID, sanitizeString(addASecretBody.secret), generatedTimestamp)
    scrambledKey =  genRandoStr()+ genRandoStr() + generatedSecretKey + genRandoStr()

    # Values are added to the DB
    queryToAddASecret = "INSERT INTO SECRETKEEPER (ID, SECRET, TTL, SECRETKEY, TIMESTAMP) Values (?, ?, ?, ?, ?)"
    valuesToAddASecret = (generatedID, encryptedSecret, addASecretBody.time, generatedSecretKey, generatedTimestamp)
    cur.execute(queryToAddASecret, valuesToAddASecret)
    postConnection.commit()

    # Scrambled key is returned
    return {"status" : "Your secret is added", "secretKey": scrambledKey}



# Gets the secret
@app.get("/knowASecret")
def getASecret(secretKey: str, response: Response):

    # Connects to the DB
    getConnection = sqlite3.connect("SECRETKEEPER.db")
    cur = getConnection.cursor()

    # Key is retreived
    secretKey = keyScrambler(secretKey)

    # Checks if the Key exists in the DB
    queryToCheckASecret = "SELECT * FROM SECRETKEEPER WHERE SECRETKEY = ?"
    valueToCheckASecret = [secretKey]
    storedSecret = cur.execute(queryToCheckASecret, valueToCheckASecret).fetchone()

    # If no, returns a 404
    if storedSecret is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"status" : "The secret key is invalid or the secret has been viewed before. Please recheck."}
    
    # If yes
    if storedSecret is not None:

        # Adds the Timestamp and the time to expire 
        secretValidTime = storedSecret[4] + storedSecret[2]

        # If the time to expire is 0 (no expiry) or the added time is greater than the current time (not expired)
        # Decrypt the secret, delete the record and return the secret 
        if storedSecret[2] == 0 or secretValidTime > currentEpochTime():
            secretInPlain = decryptASecret(storedSecret[0], storedSecret[1], storedSecret[4])
            queryToDeleteASecret = "DELETE FROM SECRETKEEPER WHERE SECRETKEY = ?"
            cur.execute(queryToDeleteASecret, valueToCheckASecret).fetchone()
            getConnection.commit()
            return {"secret" : secretInPlain, "status" : "You have viewed this secret, it is now deleted."}
        
        # If the added time is less than the current time (expired)
        # Return 403 and delete the record
        elif secretValidTime < currentEpochTime():
            response.status_code = status.HTTP_403_FORBIDDEN
            queryToDeleteASecret = "DELETE FROM SECRETKEEPER WHERE SECRETKEY = ?"
            cur.execute(queryToDeleteASecret, valueToCheckASecret).fetchone()
            getConnection.commit()
            return {"status" : "The time is passed to view the secret. It cannot be viewed."}