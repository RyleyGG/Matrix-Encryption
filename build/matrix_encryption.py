import pymatrix #used throughout the program - have to use this instead of numpy because of Brython (browser implementation) support
import math  #used throughout the program
import random #Used in multiple places, most prominently when generating a random key matrix
from random import randint #Used in multiple places, most prominently when generating a random key matrix
import base64
from browser import alert, document
        
def initialInput(self):
    document['initialSect'].style.display = 'block'
    document['encodedResultSect'].style.display = 'none'
    document['decodedResultSect'].style.display = 'none'

def encryptInput(self):
    global userInput
    document['initialSect'].style.display = 'none'
    document['encryptSect'].style.display = 'block'

    def encryptInputFinal(self):
        global userInput
        userInput = list(document['encryptInput'].value)
        encryptMessage()
    document['encryptSubmit'].bind('click',encryptInputFinal)

def encryptMessage(): #handles the encryption process of a message from the user
    global userInput


    for i in range(len(userInput)): #For all the characters entered in the input
        userInput[i] = ord(userInput[i]) #Convert the value of the current character into the unicode representation of that character.


    for i in range(len(userInput)+3): #this for loop formats the input list such that it will create a proper matrix, filling in the leftover spaces with -1.
        if i >= len(userInput):
            if len(userInput) % 3 == 0:
                break
            else:
                userInput.append(-1)

    #As opposed to numpy, pymatrix doesn't have a built-in method of properly shaping a matrix given a list, so its done manaully here by dividing the given input list into 3 smaller ones
    originalMessage = [],[],[]
    userInputSplitVal = (len(userInput)-1)/3
    for i in range(len(userInput)):
        if i <= userInputSplitVal:
            originalMessage[0].append(userInput[i])
        elif i >= userInputSplitVal and i <= userInputSplitVal*2:
            originalMessage[1].append(userInput[i])
        else:
            originalMessage[2].append(userInput[i])

    originalMessage = pymatrix.Matrix.from_list(originalMessage)

    #The key matrix is what's used in this case to encode the message; the inverse of the key matrix is used to decode the message
    keyMatrixSize = len(originalMessage[0]) #Sets the size of the key matrix, again based on the size of the original matrix

    #pymatrix doesn't have a built in method of properly filling with random values, so its done manually here after creating the keymatrix itself
    keyMatrix = pymatrix.Matrix(keyMatrixSize, keyMatrixSize)
    for i in range(keyMatrixSize): #For each row in the keymatrix...
        for x in range(keyMatrixSize): #for each column in the keymatrix
            keyMatrix[i][x] = random.randint(1,9)

    encodedMatrixTemp = originalMessage * keyMatrix #Holds the pymatrix object matrix representation of the dot product between the two matrices
    encodedMatrix = []

    #pymatrix doesn't allow .tolist() functionality, so its converted to a list manually here
    for i in range(3):
        for x in range(keyMatrixSize):
            encodedMatrix.append(encodedMatrixTemp[i][x])

    keyMatrixTemp = []
    for i in range(keyMatrixSize):
        for x in range(keyMatrixSize):
            keyMatrixTemp.append(keyMatrix[i][x])

    keyMatrix = keyMatrixTemp
    arrayCount = 0

    for x in range(len(keyMatrix)): #For however many values are in the keyMatrix, randomly insert values into the encoded matrix. 
        encodedMatrix.insert(randint(0, len(encodedMatrix)), -2) #The -2 here is replaced in the following for loop. It basically represents a placeholder value that will eventually get replaced with the values from the key matrix

    for x in range(len(encodedMatrix)): #Cleans up and prints the encrypted string with the hidden key
        if encodedMatrix[x] == -2: #If the value at a certain index was randomly placed there by the above for loop...
            encodedMatrix[x] = keyMatrix[arrayCount] #Then replace that value with a value from the keymatrix.
            arrayCount+=1
    encodedMatrix = str(encodedMatrix).strip("[").strip("]")
    finalCode = encodedMatrix.encode('utf-8')
    finalCode = str(base64.b64encode(finalCode)).strip('b').strip('\'')

    document['encryptSect'].style.display = 'none'
    document['messageSeedResult'].value = finalCode
    document['encodedResultSect'].style.display = 'block'

    document['useAgainButtonOne'].bind('click',initialInput)


def decryptInput(self):
    global messageSeed

    document['initialSect'].style.display = 'none'
    document['decryptSect'].style.display = 'block'

    def decryptInputFinal(self):
        global messageSeed
        messageSeed = document['decryptInput'].value
        decryptMessage()
    document['decryptSubmit'].bind('click',decryptInputFinal)

def decryptMessage(): #Handles the decryption process
    global messageSeed

    encryptedList = str(base64.b64decode(messageSeed.encode('utf-8'))).strip('b').strip('\'').split(", ") #Decoding the message, converting it to a string, and turning it into a list
    encodedMatrixTemp = []
    keyMatrixTemp = []

    for x in range(len(encryptedList)):
        encryptedList[x] = int(encryptedList[x]) #Convert every value to an integer
        if (encryptedList[x] > 0) and (encryptedList[x] < 10): #If the selected value is between 0 and 10, it means that it was part of the keymatrix
            keyMatrixTemp.append(encryptedList[x])
        else:
            encodedMatrixTemp.append(encryptedList[x])
    
    #As opposed to numpy, pymatrix doesn't have a built-in method of properly shaping a matrix given a list, so its done manaully here by dividing the given input list into 3 smaller ones
    encodedMatrix = [],[],[]
    encodedMatrixTempSplitVal = (len(encodedMatrixTemp)-1)/3
    for i in range(len(encodedMatrixTemp)):
        if i <= encodedMatrixTempSplitVal:
            encodedMatrix[0].append(encodedMatrixTemp[i])
        elif i >= encodedMatrixTempSplitVal and i <= encodedMatrixTempSplitVal*2:
            encodedMatrix[1].append(encodedMatrixTemp[i])
        else:
            encodedMatrix[2].append(encodedMatrixTemp[i])

    encodedMatrix = pymatrix.Matrix.from_list(encodedMatrix)

    #Create the keymatrix
    keyMatrixSize = len(encodedMatrix[0])
    keyMatrix = pymatrix.Matrix(keyMatrixSize, keyMatrixSize)
    
    y = 0
    for i in range(keyMatrixSize): #For each row in the keymatrix...
        for x in range(keyMatrixSize): #for each column in the keymatrix
            keyMatrix[i][x] = keyMatrixTemp[y]
            y+=1

    keyMatrixInverse = keyMatrix.inv()
    
    decodedMatrix = encodedMatrix * keyMatrixInverse
    decodedList = []
    for i in range(3):
        for x in range(len(decodedMatrix[0])):
            decodedList.append(decodedMatrix[i][x])
    
    throwawayArray=[]
    
    for x in range(len(decodedList)):
        floattoint = decodedList[x]
        floattoint = int(round(float(floattoint)))
        try:
            chr(floattoint) #Convert the current character from its unicode representation back into a character
        except:
            break
        else:
            throwawayArray.append(chr(floattoint))
            finalstr = ''.join(throwawayArray)
    
    #print("Decoded message:", finalstr)
    #useagain()

    document['decryptSect'].style.display = 'none'
    document['decodedMessageResult'].value = finalstr
    document['decodedResultSect'].style.display = 'block'
    document['useAgainButtonTwo'].bind('click',initialInput)

document['encryptChoice'].bind('click',encryptInput)
document['decryptChoice'].bind('click',decryptInput)