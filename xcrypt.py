import string
import random
from colorama import *
from pyperclip import *

# Program initialization
alphabet = list(string.printable) # Alphabet for reference.
def logo(): # Shows the logo of the program
    logo = """

    ██╗░░██╗░░░░░░░█████╗░██████╗░██╗░░░██╗██████╗░████████╗░█████╗░██████╗░
    ╚██╗██╔╝░░░░░░██╔══██╗██╔══██╗╚██╗░██╔╝██╔══██╗╚══██╔══╝██╔══██╗██╔══██╗
    ░╚███╔╝░█████╗██║░░╚═╝██████╔╝░╚████╔╝░██████╔╝░░░██║░░░██║░░██║██████╔╝
    ░██╔██╗░╚════╝██║░░██╗██╔══██╗░░╚██╔╝░░██╔═══╝░░░░██║░░░██║░░██║██╔══██╗
    ██╔╝╚██╗░░░░░░╚█████╔╝██║░░██║░░░██║░░░██║░░░░░░░░██║░░░╚█████╔╝██║░░██║    █▄▄ ▀▄▀ █▀▄ ▀█▀ █▀█ █▄ █ 
    ╚═╝░░╚═╝░░░░░░░╚════╝░╚═╝░░╚═╝░░░╚═╝░░░╚═╝░░░░░░░░╚═╝░░░░╚════╝░╚═╝░░╚═╝    █▄█  █  █▄▀ ▄█▄ █▄█ █ ▀█
    """
    print(logo + '\n')
def alpha_cleaner(alphabet): # Cleans the alphabet list from characters that might cause issue.
    alphabet.remove('\r')
    alphabet.remove('\t')
    alphabet.remove('\n')
    alphabet.remove('\x0b')
    alphabet.remove('\x0c')
    return alphabet
def instructions():
    print('\n===========================\n')
    print('1) Give your encryption token or read it from a file. Then, give the message you want (de/en)crypted and let the x-cryptor do its magic.\n')
    print('2) You can only encrypt letters, symbols and numbers that are in the English alphabet.\n')
    print('3) You can use "SPACE" between your words, but no new lines.\n')
    print('===========================\n')
logo()
token = alpha_cleaner(alphabet).copy() # A copy list of the alphabet that will be manipulated later on.

# X-Crypting functions
def shuffler(token): # Generates a random token. Shuffles and reverses it a random amount of times.
    for i in range(random.randint(0, 100)): 
        random.shuffle(token)
        token.reverse()
    return token

def xcrypt_loop(input, alphabet, token): # Encrypts or decrypts the message and swaps the corresponding alphanumerical letters with the encrypted ones.
    for i in range(len(input)): 
        for j in range(len(alphabet)): 
            if input[i] == alphabet[j]:
                try:
                    input[i] = token[j]
                    break
                except:
                    print('You have entered a wrong token. Restarting the sequence.\n')
                    main()
    return input

def token_decrypt(token): # Transform the token into a proper encrypted alphabet. Split the token in half and reverse it.
    newtoken = token[:(int)(len(token)/2)]
    newtoken.reverse()
    return newtoken

def file_taker(token=None): # Reads the token from a file.
    try:
        token_file = open("token.txt", "r")
        token = list(token_file.read())
        token_file.close()
        return token
    except:
        print("There is no existent token file. Please try again.")
        main()

def decrypt(): # Function responsible for handling the decrypt input.
    deinput = list(input('Please type your encrypted message: '))
    dechoice = input('Is your token:\nCLIPBOARD[1]\nFILE[2]\n')
    if dechoice == '1':
        detoken = list(input('Please type your encryption token: '))
    elif dechoice == '2':
        detoken = file_taker()
    else:
        decrypt()
    deinput = deinput[(int)(len(deinput)/2):]
    deinput.reverse()
    token = token_decrypt(detoken) 
    deinput = xcrypt_loop(deinput, token, alphabet) # Decrypt the message by doing the reverse encryption
    print('Your decrypted message is:\n' + ''.join(map(str, deinput)))

def encrypt(): # Function responsible for handling the encrypt input.
    eninput = list(input('Please type the sentence you want to encrypt: '))
    while True:
        enchoice = input('Do you want to use a token that is:\nEXISTING[1]\nNEW[2]\n')
        if enchoice == '1': # Encrypt a message using an existing token.
            filechoice = input('Is your token:\nCLIPBOARD[1]\nFILE[2]\n')
            if filechoice == '1': # Take token as input.
                extoken = list(input('Insert your existing token: '))
            elif filechoice == '2': # Read token from file.
                extoken = file_taker()
            else:
                continue
            extoken = token_decrypt(extoken) # Token restoration.
            eninput = xcrypt_loop(eninput, alphabet, extoken)
            break
        elif enchoice == '2': # Encrypt a message an generate a new token.
            shuffler(token)
            decoy = token.copy() # Create a shuffled decoy to mix up with the token, so the decryption is harder.
            shuffler(decoy)
            eninput = xcrypt_loop(eninput, alphabet, token) # Run the input encryption function.
            token.reverse() # Reverse the VALID token.
            final = token + decoy # Merge the two tokens, create a large, hard-to-decrypt token.
            print('Your encryption token is:\n' + ''.join(map(str, final)) + '\n\nEncryption token extracted in a local file!\n')
            token_file = open("token.txt", "w")
            token_file.write(''.join(map(str, final)) + '\n')
            token_file.close()
            break
        else:
            print('No valid answer was given. Please try again.\n')
    decoy = token[:len(eninput)] # Further encrypt the message.
    shuffler(decoy)
    eninput.reverse()
    finalinput = decoy + eninput
    copy(''.join(finalinput)) # Copy it to the users clipboard.
    print('Your encrypted message is:\n' + ''.join(map(str, finalinput)) + '\n\nMessage copied to the clipboard!\n')

# Input validation.
def main():
    while True: 
        answer = input('Do you want to:\nENCRYPT[1]\nDECRYPT[2]\nINSTRUCTIONS[3]\n')
        if answer == '1':
            encrypt()
        elif answer == '2':
            decrypt()
        elif answer == '3':
            instructions()
        else:
            print('No valid answer was given. Please try again.')
        choice = input('Do you want to:\n[Μ]ain Menu\n[E]xit\n')
        if choice == 'M' or choice == 'm':
            continue
        else:
            exit()

main()