from termcolor import colored
from pyfiglet import Figlet
import click
import string
import time
import random
import hashlib
from rich.progress import track
from rich.traceback import install
install() # These two lines give us a pretty looking traceback

f = Figlet(font='standard')

@click.command()
@click.option('--name', default='user', help='Name of the person to greet.')
@click.option('-l', '--length', type=int,default = 5, help='Password length')
@click.option('-noUp', '--no_upper', is_flag=True, help='Exclude uppercase characters')
@click.option('-noLow', '--no_lower', is_flag=True, help='Exclude lowercase characters')
@click.option('-noDig', '--no_digits', is_flag=True, help='Exclude digits')
@click.option('-noSpe', '--no_special', is_flag=True, help='Exclude special characters')
@click.option('-begL', '--begin_letter', is_flag = True, help='Start with a specific letter')
@click.option('-begNum', '--begin_number',is_flag = True , help='Start with a specific number')
@click.option('-begSpe', '--begin_special',is_flag = True , help='Start with a specific special character')
@click.option('-noSim', '--no_similar', is_flag=True, help='Exclude similar characters (i, l, 1, L, o, 0, O)')
@click.option('-noDup', '--no_duplicates', is_flag=True, help='Exclude duplicate characters')
@click.option('-noSeq', '--no_sequential', is_flag=True, help='Exclude sequential characters')
@click.option('-genNum', '--num_passwords', type=int, default = 1, help='Number of passwords to generate')
@click.option('-hash', '--hash_password', is_flag=True, help='Hash the generated password using SHA-256')
@click.option('-seed', '--random_seed', type=int, default = 69420, help='Seed for the randomization algorithm')
@click.option('-f', '--file', type=click.File('w'), help='File to write the passwords to')
def start(name, length, no_upper, no_lower, no_digits, no_special, begin_letter,
          begin_number, begin_special, no_similar, no_duplicates, no_sequential,
          num_passwords, hash_password, random_seed,file):
       """
       This function greets the user and generates passwords.
       
       To use with flags, example:
       
       password.exe --name Suka --length 10 --begin_letter --no_similar --no_duplicates --no_sequential --num_passwords 2 --hash_password
       
       Will give the following output:
       
       the banner
       
       Hello there Suka
       
       Generated Password 1: }f'T*8;?pN (Hash: 7195d36954170f1d2bb23d3b77a2d9fc74ba18a9eb9643a6f8b57bac0cdab848)
       
       Generated Password 2: Jxn%(6H>W (Hash: 3dcc569eb36c1766b23e0a01775c40fcf31f1ea4185e20b0b08b1e8c99c0af29)
       
       """
       click.echo(colored(f.renderText('Password Generator'),'red'))
       click.echo(colored('Hello there %s' %name,'green'))
    # print('Hello there %s' %name)
       if not any([no_upper, no_lower, no_digits, no_special, begin_letter, begin_number,
                begin_special, no_similar, no_duplicates, no_sequential, hash_password,file]):
                    for i in track(range(100), description='Loading...'):
                        time.sleep(0.01) # This gives us a nice loading bar
                        
                    click.echo(colored('Welcome to the Password Generator', 'blue'))
                    click.echo(colored('Please answer the following questions to generate your password', 'blue'))
                    length = click.prompt("How long do you want the password to be?", type=int)
                    no_upper = not click.confirm("Include uppercase characters?")
                    no_lower = not click.confirm("Include lowercase characters?")
                    no_digits = not click.confirm("Include digits?")
                    no_special = not click.confirm("Include special characters?")
                    no_similar = not click.confirm("Exclude similar characters (i, l, 1, L, o, 0, O)?")
                    no_duplicates = not click.confirm("Exclude duplicate characters?")
                    no_sequential = not click.confirm("Exclude sequential characters?")
                    if click.confirm("Do you want to start the password with a particular type of character?"):
                        # Ask for eac   h type individually
                        begin_letter = False
                        begin_number = False
                        begin_special = False
                        if click.confirm("Do you want to start with a letter?"):
                            begin_letter = True
                        elif click.confirm("Do you want to start with a number?"):
                            begin_number = True
                        else:
                            begin_special = True
                    num_passwords = click.prompt("How many passwords do you want to generate?", type=int, default=1, show_default=True)
                    if click.confirm("Do you want your password to be hashed?"):
                        hash_password = True
                        if click.confirm("Do you want to provide your own numeric seed for the randomization algorithm?", default = False):
                                random_seed = click.prompt("Enter your seed", type=int)

                        if random_seed:
                            random.seed(random_seed)
    
       passwords = [] # This will be an array of passwords

       for _ in range(num_passwords):
           password = generate_single_password(length, no_upper, no_lower, no_digits, no_special,
                                        begin_letter, begin_number, begin_special,
                                        no_similar, no_duplicates, no_sequential)
           passwords.append(password)

       for i, password in enumerate(passwords, start=1):
            if hash_password:
                hashed_password = hashlib.sha256(password.encode()).hexdigest()
                if file:
                    file.write(f'Generated Password {i}: {password} (Hash: {hashed_password})\n')
                click.echo(colored(f'Generated Password {i}: {password} (Hash: {hashed_password})', 'yellow'))
            else:
                if file:
                    file.write(f'Generated Password {i}: {password}\n')
                click.echo(colored(f'Generated Password {i}: {password}', 'blue'))
       if file:
           click.echo(colored('Your passwords have been saved to the file', 'green'))
           file.close()
def generate_single_password(length, no_upper, no_lower, no_digits, no_special,
                            begin_letter, begin_number, begin_special,
                            no_similar, no_duplicates, no_sequential):
    """This function generates a single password"""
    characters = ''
    if not no_upper:
        characters += string.ascii_uppercase
    if not no_lower:
        characters += string.ascii_lowercase
    if not no_digits:
        characters += string.digits
    if not no_special:
        characters += string.punctuation

    if no_similar:
        characters = characters.translate(str.maketrans('', '', 'il1Lo0O'))  # Exclude similar characters

    passwor = ''
    if begin_letter:
        passwor += random.choice(string.ascii_letters)
    elif begin_number:
        passwor += random.choice(string.digits)
    elif begin_special:
        passwor += random.choice(string.punctuation)

    passwor += ''.join(random.sample(characters, length - len(passwor)))



    if no_duplicates:
        passwor = ''.join(set(passwor))  # Remove duplicates
    if no_sequential:
        passwor = remove_sequential_characters(passwor)  # Remove sequential characters

    return ''.join(passwor)

def remove_sequential_characters(characters):
    # Remove sequential characters like abc or 789
    new_characters = ''
    for i, char in enumerate(characters):
        if i == 0 or characters[i - 1] != chr(ord(char) - 1):
            new_characters += char
    return new_characters

if __name__ == '__main__':
    start()
