import pymatrix #used throughout the program - have to use this instead of numpy because of Brython (browser implementation) support
import math  #used throughout the program
import random #Used in multiple places, most prominently when generating a random key matrix
from random import randint #Used in multiple places, most prominently when generating a random key matrix
import base64
from browser import alert, document


def updateTable(tableObj, matrix, matrixLabel, matrixlabelid):
    tableHtml = []
    for x in range(len(matrix)): #for each row in the matrix
        rowHtml = '<tr>'
        for y in range(len(matrix[0])): #for each column
            if x == 0 and y == 0:
                rowHtml += "<td class = 'topval leftval'>" + str(matrix[x][y]) + "</td>"
            elif x == len(matrix)-1 and y == 0:
                rowHtml += "<td class = 'bottomval leftval'>" + str(matrix[x][y]) + "</td>"
            elif x == 0 and y == len(matrix[0])-1:
                rowHtml += "<td class = 'topval rightval'>" + str(matrix[x][y]) + "</td>"
            elif x == len(matrix)-1 and y == len(matrix[0])-1:
                rowHtml += "<td class = 'bottomval rightval'>" + str(matrix[x][y]) + "</td>"
            elif y == 0:
                rowHtml += "<td class = 'leftval'>" + str(matrix[x][y]) + "</td>"
            elif y == len(matrix[0])-1:
                rowHtml += "<td class = 'rightval'>" + str(matrix[x][y]) + "</td>"
            else:
                rowHtml += "<td>" + str(matrix[x][y]) + "</td>"
        rowHtml += "</tr>"
        tableHtml.append(rowHtml)
    tableObj.html = ''.join(tableHtml)
    document[matrixlabelid].html = matrixLabel

#resets input form back to initial encrypt/decrypt options
def initialInput(ev):
    document['initialSect'].style.display = 'block'
    document['encodedResultSect'].style.display = 'none'
    document['decodedResultSect'].style.display = 'none'
    document['firstMatrixDisplay'].style.display = 'none'
    document['secondMatrixDisplay'].style.display = 'none'
    document['thirdMatrixDisplay'].style.display = 'none'

#executes when user chooses encryption option
def encryptInput(ev):
    document['initialSect'].style.display = 'none'
    document['encryptSect'].style.display = 'block'

    def encryptInputFinal(ev):
        userInput = list(document['encryptInput'].value)
        encryptMessage(userInput)
    document['encryptSubmit'].bind('click',encryptInputFinal)

def encryptMessage(userInput): #handles the encryption process of a message from the user

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
        if i <= userInputSplitVal: #Adding to first row of the matrix
            originalMessage[0].append(userInput[i])
        elif i >= userInputSplitVal and i <= userInputSplitVal*2: #Adding to second row of the matrix
            originalMessage[1].append(userInput[i])
        else:
            originalMessage[2].append(userInput[i]) #Adding to third row of the matrix

    updateTable(document['firstMatrix'], originalMessage, 'Original Message', 'firstmatrixtext')
    originalMessage = pymatrix.Matrix.from_list(originalMessage) #Generates a matrix object from the list of lists just generated

    #The key matrix is what's used in this case to encode the message; the inverse of the key matrix is used to decode the message
    keyMatrixSize = len(originalMessage[0]) #Sets the size of the key matrix, again based on the size of the original matrix

    #pymatrix doesn't have a built in method of properly filling with random values, so its done manually here after creating the keymatrix itself
    keyMatrix = pymatrix.Matrix(keyMatrixSize, keyMatrixSize)
    for i in range(keyMatrixSize): #For each row in the keymatrix...
        for x in range(keyMatrixSize): #for each column in the keymatrix
            keyMatrix[i][x] = random.randint(1,9)

    encodedMatrixTemp = originalMessage * keyMatrix #Holds the pymatrix object matrix representation of the dot product between the two matrices
    encodedMatrix = []
    encodedMatrixForDisplay = []
    #pymatrix doesn't allow .tolist() functionality, so its converted to a list manually here
    for i in range(3):
        encodedMatrixForDisplay.append([])
        for x in range(keyMatrixSize):
            encodedMatrixForDisplay[i].append(encodedMatrixTemp[i][x])
            encodedMatrix.append(encodedMatrixTemp[i][x])

    updateTable(document['thirdMatrix'], encodedMatrixForDisplay, 'Encoded', 'thirdmatrixtext')

    keyMatrixTemp = []
    keyMatrixForDisplay = []
    for i in range(keyMatrixSize):
        keyMatrixForDisplay.append([])
        for x in range(keyMatrixSize):
            keyMatrixForDisplay[i].append(keyMatrix[i][x])
            keyMatrixTemp.append(keyMatrix[i][x])

    updateTable(document['secondMatrix'], keyMatrixForDisplay, 'Key', 'secondmatrixtext')
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

    #once everything has been calculated, set up display
    document['encryptSect'].style.display = 'none'
    document['messageSeedResult'].value = finalCode
    document['encodedResultSect'].style.display = 'block'
    document['firstMatrixDisplay'].style.display = 'inline-block'
    document['secondMatrixDisplay'].style.display = 'inline-block'
    document['thirdMatrixDisplay'].style.display = 'inline-block'

    document['useAgainButtonOne'].bind('click',initialInput)

#executes when user chooses decryption option
def decryptInput(ev):
    document['initialSect'].style.display = 'none'
    document['decryptSect'].style.display = 'block'

    def decryptInputFinal(ev):
        messageSeed = document['decryptInput'].value
        decryptMessage(messageSeed)
    document['decryptSubmit'].bind('click',decryptInputFinal)

def decryptMessage(messageSeed): #Handles the decryption process

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

    updateTable(document['firstMatrix'], encodedMatrix, 'Encoded', 'firstmatrixtext')
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

    keyMatrixInverseForDisplay = []
    for i in range(keyMatrixSize):
        keyMatrixInverseForDisplay.append([])
        for x in range(keyMatrixSize):
            keyMatrixInverseForDisplay[i].append(keyMatrix[i][x])
    updateTable(document['secondMatrix'], keyMatrixInverseForDisplay, 'Inverse Key', 'secondmatrixtext')

    decodedMatrix = encodedMatrix * keyMatrixInverse
    decodedList = []
    decodedMatrixForDisplay = []
    for i in range(3):
        decodedMatrixForDisplay.append([])
        for x in range(len(decodedMatrix[0])):
            decodedMatrixForDisplay[i].append(round(decodedMatrix[i][x]))
            decodedList.append(decodedMatrix[i][x])

    updateTable(document['thirdMatrix'], decodedMatrixForDisplay, 'Decoded', 'thirdmatrixtext')

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

    document['decryptSect'].style.display = 'none'
    document['decodedMessageResult'].value = finalstr
    document['decodedResultSect'].style.display = 'block'
    document['firstMatrixDisplay'].style.display = 'inline-block'
    document['secondMatrixDisplay'].style.display = 'inline-block'
    document['thirdMatrixDisplay'].style.display = 'inline-block'

    document['useAgainButtonTwo'].bind('click',initialInput)

document['encryptChoice'].bind('click',encryptInput)
document['decryptChoice'].bind('click',decryptInput)