import os,  binascii,  hashlib
from wordlist import wordList
from utils import chunks

def genMnemonic():
    # Generate a new mnemonic phrase
    # Generate a new random seed
    # Convert seed to integers
    # Assign each number to a word in the word list
    
    words = wordList()
    seed = genSeed()
    mnemonicInt = mnemonicList(seed)
    mnemonic = []
    
    for num in mnemonicInt:
        ind = num
        mnemonic.append(words[ind])
    
    mnemonic = " ".join(str(x) for x in mnemonic)
    
    return mnemonic
    
def mnemonicList(seed):
    # Convert each hexidecimal character (4 bits) of a given seed to a decimal integer
    # Return the integers as a list
    
    seed = chunks(seed,  1)
    mnemonicInt = []
    
    for character in seed:
        x = int(character, 16)
        mnemonicInt.append(x)
    
    return mnemonicInt
    
    
def genSeed():
    # Turn our entropy into a seed
    # We will first create a seed using PBKDF2 - using SHA512 as our pseudo random function
    # Two sets of entropy will be used, one as our main source, another will be hashed and used as a salt
    # For demo purposes the seed will be cut down to 3 bytes (24bits) for simplicity
    # A checksum is calculated from the seed (see: genChecksum) and appended to the seed
    
    entropy = genEntropy()
    saltEntropy = genEntropy()
    
    sha256 = hashlib.sha256()
    sha256.update(saltEntropy)
    salt = sha256.hexdigest() 
    
    pbkdf2 = hashlib.pbkdf2_hmac('sha512',  entropy,  salt,  2048)
    seed = binascii.hexlify(pbkdf2)
    seed = seed[:6]
    
    checksum = genChecksum(seed)
    
    seed = seed + checksum
    
    return seed
    
def genEntropy():
    # Generate 24bits (3 bytes) of entropy using the OS' cryptography function
    # Convert raw bytes to hex
    
    ent = os.urandom(3)
    ent = binascii.hexlify(ent)
    
    return ent
    
def genChecksum(data):
    # Generates a checksum from given seed
    # Seed is hashed using SHA256
    # The first character (4 bits) of the checksum is returned
    
    sha256 = hashlib.sha256()
    sha256.update(data)
    checksum = sha256.hexdigest()
    checksum = checksum[:1]
    
    return checksum
    
def checkValid(mnemonic):
    # Verify the validity of a given mnemonic
    # Decode the mnemonic to it's original seed using the wordlist
    # Remove the last character of the seed (the checksum) to find the initial seed
    # Hash the seed and take the first letter of the generated checksum
    # Compare to the last letter of the decoded mnemonic
    # If both match, mnemonic is valid
    
    mnemonic = mnemonic.split()
    words = wordList()
    rawSeed = []
    seed = []
    
    for word in mnemonic:
        x = words.index(word)
        rawSeed.append(x)
    
    for num in rawSeed:
        x = hex(num)[2:]
        seed.append(x)
    
    seed = "".join(str(x) for x in seed)
    
    rawSeed = seed[:6]
    
    rawCheck = seed[6:]

    checksum = genChecksum(rawSeed)
    
    if checksum == rawCheck:
        return True
    
    return False
