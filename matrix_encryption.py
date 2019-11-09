import os
import numpy #used throughout the program
import math  #used throughout the program
import random #Used in multiple places, most prominently when generating a random key matrix
from random import randint #Used in multiple places, most prominently when generating a random key matrix
import time
import base64

def userChoice():
    userAction = input(f"1. Encrypting\n2. Decrypting\nAre you encrypting or decrypting?\n")
    
    while True:
        if userAction not in ["1", "encrypting", "encryption", "2", "decrypting", "decryption"]:
            userAction = input(f'I don\'t understand what you mean by {userAction}. Please resubmit.')
        else:
            break

    if userAction.lower() in ["1", "encrypting", "encryption"]: encryptMessage()

    elif userAction.lower() in ["2", "decrypting", "decryption"]: decryptMessage()

        
def encryptMessage(): #handles the encryption process of a message from the user
    originalMessage = list(input("Please input a message to be encoded: ")) #Splitting the input into a list so that each individual character can be encrypted
    
    for i in range(len(originalMessage)): #For all the characters entered in the input
        originalMessage[i] = ord(originalMessage[i]) #Convert the value of the current character into the unicode representation of that character.


    for i in range(len(originalMessage)+3): #this for loop formats the input list such that it will create a proper matrix, filling in the leftover spaces with -1.
        if i >= len(originalMessage):
            if len(originalMessage) % 3 == 0:
                break
            else:
                originalMessage.append(-1)
        
    originalMessage = numpy.array(originalMessage).reshape(3,-1) #Converting the input list into an array and then reshaping it. By setting the width to be -1, the value will be inferred from the length value

    #The key matrix is what's used in this case to encode the message; the inverse of the key matrix is used to decode the message
    keyMatrixSize = len(originalMessage[0]) #Sets the size of the key matrix, again based on the size of the original matrix
    keyMatrix = numpy.random.randint(1, high = 9, size = (keyMatrixSize, keyMatrixSize)) #Creates a matrix filled with random integers between 1 and 9 based on the size of a row in the original input matrix representation

    encodedMatrix = numpy.dot(originalMessage, keyMatrix) #Creating the coded matrix itself, which is the dot product between the original input matrix and the key matrix
    encodedMatrix = numpy.round(encodedMatrix) #Round the array
    encodedMatrix = encodedMatrix.astype(int) #Convert the array to a set of integers

    encodedMatrix = encodedMatrix.flatten().tolist() #Flattens the coded matrix and converts it to a list

    keyMatrix = keyMatrix.flatten().tolist()
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
    print("Message seed:", finalCode)
    time.sleep(1)
    useagain()

def decryptMessage(): #Handles the decryption process
    
    messageSeed = input('Place seed to be decoded: ') #Grabbing the base64 seed from the user
    encryptedList = str(base64.b64decode(messageSeed.encode('utf-8'))).strip('b').strip('\'').split(", ") #Decoding the message, converting it to a string, and turning it into a list
    encodedMatrix = []
    keyMatrix = []

    for x in range(len(encryptedList)):
        encryptedList[x] = int(encryptedList[x]) #Convert every value to an integer
        if (encryptedList[x] > 0) and (encryptedList[x] < 10): #If the selected value is between 0 and 10, it means that it was part of the keymatrix
            keyMatrix.append(encryptedList[x])
        else:
            encodedMatrix.append(encryptedList[x])

    encodedMatrix = numpy.array(encodedMatrix) #Convert the list into a numpy array
    encodedMatrix = encodedMatrix.reshape(3,-1) #Reshape the array
    
    #Create the keymatrix
    keyMatrixSize = len(encodedMatrix[0])
    keyMatrix = numpy.array(keyMatrix)
    keyMatrix = keyMatrix.reshape(keyMatrixSize, keyMatrixSize)
    
    keyMatrixInverse = numpy.linalg.inv(keyMatrix) #Find the inverse of the key matrix
    
    decodedMatrix = numpy.dot(encodedMatrix, keyMatrixInverse) #By multiplying the encoded matrix with the inverse of the key, 
    decodedStr = decodedMatrix.flatten()
    
    throwawayArray=[]
    
    for x in range(len(decodedStr)):
        floattoint = decodedStr[x]
        floattoint = int(round(floattoint))
        try:
            chr(floattoint) #Convert the current character from its unicode representation back into a character
        except:
            break
        else:
            throwawayArray.append(chr(floattoint))
            finalstr = ''.join(throwawayArray)
    
    print(f"Decoded message: {finalstr}")
    time.sleep(1)
    useagain()


#This function handles repeated user usage after they encrypt/decrypt at least once
def useagain():
    useagain = input(f"\nWould you like to do encrypt/decrypt another message? Y/N\n\n")
    if useagain.lower() in ["y","yes"]: userChoice()
    elif useagain.lower() in ["n","no"]:
        print("Thanks for using!")
        time.sleep(1.5)
        sys.exit()


userChoice()