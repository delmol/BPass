import hashlib, binascii

def passManager(mnemonic):
    seed = genSeed(mnemonic)
    site = raw_input("Enter website/service name: ")
    password = genPass(seed,  site)
    print(password)
    
def genSeed(mnemonic):
    pbkdf2 = hashlib.pbkdf2_hmac('sha512',  mnemonic,  mnemonic + '',  2048)
    seed = binascii.hexlify(pbkdf2)
    return seed
    
def genPass(seed,  salt):
    passSeed = seed + salt
    sha256 = hashlib.sha256()
    sha256.update(passSeed)
    password = sha256.hexdigest()
    password = password[:32]
    return password
