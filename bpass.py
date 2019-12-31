import sys
from mnemonic import genMnemonic, checkValid
from password import passManager

def main(argv):
    print("BPass: Ben's Basic Deterministic Password Generator")
    print("~~~~~~~~~~~~")
    
    if not argv:
        generate()
    elif argv:
        if checkValid(argv[0]):
            passManager(argv[0])
        else:
            print("Invalid mnemonic")
    
def generate():
    print("No mnemonic specified. Generating a new one...")
    print("Mnemonic: ")
    mnemonic = genMnemonic()
    print(mnemonic)

if __name__ == "__main__":
    main(sys.argv[1:])
