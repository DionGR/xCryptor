import string
import random
from pyperclip import *

#==========================================
# Program initialization & Looks
#==========================================
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
    print('4) Your decryption token HAS to be in a file named token.txt.\n')
    print('5) You can enter a message manually by creating a file named message.txt WARNING: Your message will be replaced if you choose to export the encrypted one.\n')
    print('6) You can read unencrypted or encrypted messages from the messages.txt file and encrypt/decrypt them in the process.\n')
    print('===========================\n')
logo()
token = alpha_cleaner(alphabet).copy() # A copy list of the alphabet that will be manipulated later on.
#==========================================
# General X-Crypting functions
#==========================================
def token_file_reader(): # Reads the token from a file.
    try:
        token_file = open("token.txt", "r")
        token = list(token_file.read())
        token_file.close()
        return token
    except:
        print("There is no existent token file. Please try again.\n")
        main(token)

def message_reader(): # Decides how the message is going to be read.
    while True:
        choice = input('\nIs your message:\nMANUAL INPUT[1]\nFILE[2]\n')
        if choice == '1':
            xinput = list(input('\nPlease type your message:\n'))
            break
        elif choice == '2':
            try:
                message_file = open("message.txt", "r")
                xinput = list(message_file.read())
                message_file.close()
            except:
                print("There is no existent message file. Please try again.\n")
                continue
            break
        else:
            print('No valid answer was given. Please try again.\n')
            continue
    return xinput

def token_translate(token): # Transform the token into a proper encrypted alphabet. Split the token in half and reverse it.
    token = token[:(int)(len(token)//2)]
    token.reverse()
    return token

def xcrypt_loop(xinput, alphabet, token): # Encrypts or decrypts the message and swaps the corresponding alphanumerical letters with the encrypted ones.
    for i in range(len(xinput)): 
        for j in range(len(alphabet)): 
            if xinput[i] == alphabet[j]:
                try:
                    xinput[i] = token[j]
                    break
                except:
                    print('You have entered a wrong token. Restarting the sequence.\n')
                    main(token)
    return xinput
#==========================================
# [SUB] Decryptying
#==========================================
def decrypt(): # Function responsible for handling the decrypt input.
    deinput = message_reader()
    detoken = token_file_reader()
    deinput = deinput[(int)(len(deinput)//2):]
    deinput.reverse()
    token = token_translate(detoken) 
    deinput = xcrypt_loop(deinput, token, alphabet) # Decrypt the message by doing the reverse encryption.
    message_export(deinput)
#==========================================
# [SUB] Encrypting
#==========================================
def shuffler(tobeshuffled): # Shuffles and reverses a message/token a ranom amount of times.
    for i in range(random.randint(0, 150)): 
        random.shuffle(tobeshuffled)
        tobeshuffled.reverse()
    return tobeshuffled

def existing_token(eninput, token): # Encrypts a message using an existing token.
    try:
        token = token_file_reader()
    except:
        print('No valid answer was given. Please try again.\n')
        existing_token(eninput, token=None)
    token = token_translate(token) # Token restoration.
    eninput = xcrypt_loop(eninput, alphabet, token)
    return eninput, token

def new_token(eninput, token, final): # Generates a new token and encrypts a message.
    shuffler(token)
    decoy = token.copy() # Create a shuffled decoy to mix up with the token, so the decryption is harder.
    shuffler(decoy)
    eninput = xcrypt_loop(eninput, alphabet, token) # Run the input encryption function.
    token.reverse() # Reverse the VALID token.
    final = token + decoy # Merge the two tokens, create a large, hard-to-decrypt token.
    print('\nYour encryption token is:\n' + ''.join(map(str, final)) + '\n\nEncryption token extracted in a local file!\n')
    token_file = open("token.txt", "w")
    token_file.write(''.join(map(str, final)) + '\n')
    token_file.close()
    return None, token, final

def message_encrypt(eninput): # Further encrypt the message.
    msg_decoy = eninput.copy() 
    msg_decoy = shuffler(msg_decoy)
    eninput.reverse()
    eninput = msg_decoy + eninput
    message_export(eninput)
    return eninput

def message_export(eninput): # Export the message to a file or the clipboard.
    choice = input('\nDo you want your message to be:\nCOPIED & PRINTED[1]\nEXPORTED TO FILE[2]\n')
    while True:
        if choice == '1':
            copy(''.join(eninput)) # Copy it to the users clipboard.
            print('\n\nMessage copied to the clipboard!\n')
            break
        elif choice == '2':
            message_file = open("message.txt", "w")
            message_file.write(''.join(map(str, eninput)) + '\n')
            message_file.close()
            print('\n\nMessage has been exported into a file!\n')
            break
        else:
            print('No valid answer was given. Please try again.\n')

def encrypt(token): # Function responsible for handling the encrypt input.
    eninput = message_reader()
    while True:
        enchoice = input('\nDo you want to use a token that is:\nEXISTING[1]\nNEW[2]\n')
        if enchoice == '1': # Encrypt a message using an existing token.
            existing_token(eninput, token=None)
            break
        elif enchoice == '2': # Encrypt a message an generate a new token.
            new_token(eninput, token, final=None)
            break
        else:
            print('No valid answer was given. Please try again.\n')
    eninput = message_encrypt(eninput)
    print('Your encrypted message is:\n ' + ''.join(map(str, eninput)) + ' \n')
#==========================================
# Input validation.
#==========================================
def main(token):
    while True: 
        answer = input('\nDo you want to:\nENCRYPT[1]\nDECRYPT[2]\nINSTRUCTIONS[3]\n')
        if answer == '1':
            encrypt(token)
        elif answer == '2':
            decrypt()
        elif answer == '3':
            instructions()
        else:
            print('No valid answer was given. Please try again.')
            continue
        choice = input('\nDo you want to:\n[Μ]ain Menu\n[E]xit\n')
        if choice.lower() == 'm':
            continue
        else:
            exit()
#==========================================

main(token)
