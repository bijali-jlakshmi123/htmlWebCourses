import random
import string
def generate_password(length,uppercase,lowercase,numbers,symbols):
    characters=''
    if uppercase:
        characters += string.ascii_uppercase
    if lowercase:
        characters += string.ascii_lowercase
    if numbers:
        characters += string.digits
    if symbols:
        characters += string.punctuation
    if not characters:
        print("Error, no characters found: ")  
    password = ''.join(random.choice(characters) for ln in range(length))
    return password 
    

length = int(input("Enter the length of the password : "))
uppercase= input('Include Uppercase yes/no:').lower() == 'yes'
lowercase= input('Include Lowercase yes/no:').lower() == 'yes'
numbers= input('Include Digits yes/no:').lower() == 'yes'
symbols= input('Include Symbols yes/no:').lower() == 'yes'

password = generate_password(length,uppercase,lowercase,numbers,symbols)
print("Generated password: ",password)