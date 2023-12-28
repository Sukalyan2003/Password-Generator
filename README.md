This is where I'll make my first CLI program as the final project to CS50.
Creating an entire project may seem daunting. Here are some questions that you should think about as you start:

- What will your software do? What features will it have? How will it be executed?
  It will be a password generator that works in two ways. Either it will ask the user a set of questions about the parameters or work directly with the flags provided in the terminal.
- What new skills will you need to acquire? What topics will you need to research?
  Complete CLI development is new to me. Along with that I have to learn about asynchronous code. Now I can work either with Javascript or Python and I haven't decided which one to use yet.
- In the world of software, most everything takes longer to implement than you expect. And so it’s not uncommon to accomplish less in a fixed amount of time than you hope. What might you consider to be a good outcome for your project? A better outcome? The best outcome?
  A good outcome would be a program that just works with the core functionality but doesn't have all the aesthetics or the flag options. 
  better outcome would be colours and aesthetics.
  Best outcome would be a complete sets of flags and pipeline support.

https://clig.dev/#the-basics

The program will be a CLI application built using [[Python]] using the [click](https://click.palletsprojects.com/en/8.1.x/),[rich](https://github.com/Textualize/rich)
and recorded for CS50 using [asciinema](https://asciinema.org/)

Things to do
1. Make the program such that it can take input from multiple file formats and give output in multiple formats.
2. Make the program such that there is a detailed documentation built into it, much like a help command.
   **Display help text when passed no options, the `-h` flag, or the `--help` flag.**
   The concise help text should only include:
   A description of what your program does.
   One or two example invocations.
   Descriptions of flags, unless there are lots of them.
   An instruction to pass the `--help` flag for more information.
3. Make the program standalone so that the user does not have to worry about dependencies.
4. Think about all the possible errors and how to effectively show the error logs without saying too much or too little.
5. **Send messaging to `stderr`.** Log messages, errors, and so on should all be sent to `stderr`. This means that when commands are piped together, these messages are displayed to the user and not fed into the next command.

## General features
The only thing left is to test everything out point by point. 

1. Questionnare or flagged?
   IF there are no flags mentioned while calling the program in the command line, then it launches into a questionnare, otherwise it leaves everything else the same and works based on the flags provided. 
2. Password length: 
   Question: "How long do you want the password to be?"
   Flag: `-l` and `--length`
3. Character Customization:
   Question: "Do you want to change which characters occur in the password?"
   IF they say yes then ask about each of Upper case, Lower case, Digits and Special characters.
   By default have all of them turned on. 
   Flag: `-noUp`,`-noLow`,`-noDig` and `-noSpe` to disable each of the four types of characters. 
4. Beginning with a particular character. 
   Question: "Do you want the password to start with a particular type of character?"
   IF they say yes then do exactly as you did for point 2. 
   Flag: `-begL`, `-begNum`,`-begSpe` for the password to begin with those respectively. 
5. No similar characters:
   Question: "Do you want there to be similar characters like i, l, 1, L, o, 0, O?"
   If yes then ok else apply the logic to exclude similar characters.
   Flag: `-noSim`.
6. No duplicate characters:
   Question: "Do you want there to be duplicate Characters?"
   If yes then leave as is, if no then implement the logic for this. 
   Flag: `-noDup`
7. No sequential Characters:
   Question: "Do you want to exclude sequential characters like abc or 789?"
   If no then leave it, if yes then apply the logic.
   Flag: `-noSeq`
8. Number of passwords to generate:
   Question: "How many passwords do you want to generate?"
   This value has to be a positive integer. 
   Flag: `-genNum number` 
9. Randomization algorithm. This one you should pick your own, it's not a user choice. Or should you put on here???
   Question: "Do you want to provide your own seed for the randomization algorithm?"
   If no then use defaults else Add the feature for the user to provide a secure seed and change the algorithm based on that.
10. Hashing Passwords:
    Question: "Do you want your password to be hashed?"
    If yes then do a SHA-256 hash. Add more later
    flag: `-hash`
11. 
## Python approach

First display a banner using figlet, "Password generator". using [this](https://towardsdatascience.com/prettify-your-terminal-text-with-termcolor-and-pyfiglet-880de83fda6b)
Then give the password if arguments are given else start the questionnare

We use the click module for parsing command line stuff and it works as follows:
We first need to add `@click.command()` above our function to make sure it's working with it.
Then we can add each flag using the `@click.option('flag', default='',help='Tis will be shown when the help command is run')`,where for example, `@click.option('--string', default='world')` is used to take a string input from user but has world as the default so we can just print hello world by default or hello name if we pass a name. 

use `click.echo("statement")` instead of print function when using click. One problem i have noticed is that if you have a print function and an echo function both in one code, the type that comes first will only be executed. That is if print is used even once first, that will work but all the echos won't work.
So the best practice would be to use echo or print consistently for everything.

We can also add subcommands by defining a function within a click command and then writing the other commands as FunctionName.command()

For example:
```python

@click.group()
def cli():
    pass 

@cli.command()
@click.option('--name', default='world', help='Name of the person to greet.')
def greet(name):
    click.echo(colored(f.renderText('Password Generator'),'red'))
    click.echo('Hello there %s' %name)
    # print('Hello there %s' %name)
if __name__ == '__main__':

    cli()
```


Now to add the graphics using Textual and rich.
Here I have to make a decision, whether to add simple colours using Rich or making a complete GUI like app within the terminal using textual.

Let's do the simpler one first then try out the complex one. Probably i'll use textual in a later more massive program. https://www.youtube.com/playlist?list=PLHhDR_Q5Me1MxO4LmfzMNNQyKfwa275Qe

Had to use UPX to compress the executable file size down from 64mb to 50mb but that's still not enough.
Now im gonna try to setup a virtual environment.

To run this venv, after ive initialized it, i have to run the following command for Powershell to allow me to enter the venv
`Set-ExecutionPolicy RemoteSigned`
then `.\venv\Scripts\Activate`

Then install all the packages you need *including* pyinstaller. Because if you don't the global pyinstaller will work and inflate your application size.

The following is the executable making command that finally worked for me when turning the python code into a funcitoning executable.
```cmd
  pyinstaller --onefile --upx-dir=C:\Users\Admin\Desktop\cli\upx-4.2.1-win64 -F --collect-all pyfiglet --strip .\password_generator.py
```
And everything Just works.
### Rich
I am using this to pretty print the tracebacks and add progress bars to my program.