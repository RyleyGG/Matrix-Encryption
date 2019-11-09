# Matrix-Encryption
Using matrices to encrypt a message; also capable of decoding these messages.

The program is a proof-of-concept of how matrices can be used to encrypt data, particularly string-like messages.

## Program Process

### Setting up the message matrix
1. Gather a string from the user.
2. After converting the string to a list of its individual characters, the characters will be converted to the unicode representations of themselves.
3. In order to create a proper matrix down the road, -1 values will be appended to this list of characters to ensure that there are enough values to fill a 3 row matrix.
4. The set of characters (and filler values) will be converted to an array of size (3,-1), where the -1 means that it will be inferred from the other value.

### Setting up the key matrix
1. Create a new matrix with the same size as the length of a row in the original message matrix (this is so the dot product of the two later on is valid)
2. Fill the matrix with random values between 1 and 9. The randomness is what allows the encryption to change everytime the process is run, so the same string can have different results.

### Creating the coded matrix
1. Find the dot product between the original message matrix and the key matrix. Round the data and convert it all to integers.
2. Flatten this matrix and convert to a list, and do the same with the key matrix.
3. For however long the key matrix is, insert placeholder values of '-2' into the coded matrix at random indices. The placeholder values will be eventually replaced with the key matrix values in the final code. This is done so that the key matrix will always be in the proper order in the final code string, but will appear in random indices.
4. After properly replacing the placeholder values with the key matrix values, encode the final string into base64 and give to the user as a seed. This seed can then be decoded.

### Decoding messages
The decoding process is essentially the inverse of the encoding process:
1. Given a base64 value, the program will decode it into a list and convert that list into a matrix.
2. The key matrix will be gathered from the original message matrix. This is possible for two reasons:

a) When the key matrix values are placed in the final encoded string, they are always kept in the correct order. For example, say you had a final code matrix that looked like this: [a,55,23,b,35,1954,c,9923] where a, b, and c are the key matrix values. They can appear at random indices, but they will always be in the order of a and then b and then c.

b) With the current system, the after the original message values are encoded, they will always be large numbers in the 1000-range. Key matrix values on the other hand are always between 1 and 10, meaning its very easily to programatically sort the two out.

3. After the key matrix is gathered, the inverse will be created. This is because, in order to gather the original message values from the coded matrix, you have to perform the dot product between the coded matrix and the inverse of the key matrix in order to undo the initial dot product that created the encryption in the first place.
4. After the dot product, the resultant matrix will be flattened and iterated through in order to recreate the original string, which is then given to the user.

There are a number of issues with the current setup that prevent it from being something akin to an actually usable cryptographic solution; it is more a proof-of-concept of how data can be reliably stored in matrix representations.
