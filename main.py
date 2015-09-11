# this is the main file that get called
import os
import sys
import gitTA as git
import colorama
from colorama import Fore, Back  # add color output to terminal: we want anything printed to be VERY visible to user
colorama.init()  # called so that windows colors work
'''
modify this file! When git runs certain commands, it will run THIS main.py
which will trigger the functions you've decorated here with gitta.listen('event-name')
your methods can listen for the following events:
pre-push, pre-commit,  # pre-x methods can be aborted by raising an exception
post-commit, post-checkout, post-merge
'''

# pre-* events can be aborted by raising an exception ???
@git.listen('pre-push')
def prepush(*args, **kwargs):
    print(Fore.GREEN)  # set so that ALL next prints will be green
    print(args, kwargs)

@git.listen('pre-commit')
def precommit(*args, **kwargs):
    print(Fore.GREEN)
    print(args, kwargs)

@git.listen('post-commit')
def postcommit(*args, **kwargs):
    print(Fore.GREEN)
    print(args, kwargs)

@git.listen('post-checkout')
def postcheckout(*args, **kwargs):
    print(Fore.GREEN)  # set so that ALL next prints will be green
    print(args, kwargs)
    branches = git.Branch()
    branches.undo_checkout(*args, **kwargs)

@git.listen('post-merge')
def postmerge(*args, **kwargs):
    print(args, kwargs)

if __name__ == '__main__':
    git.trigger(45, event='post-checkout')  # example of what might get passed to postcheckout
    # the garbled message that appears before (45, ) is the Fore.GREEN. On normal terminals this garbled output will NOT appear
    

# ['.gitta/py/main.py', 'pre-push', 'origin', 'https://github.com/lancekindle/test.git']
# ['.gitta/py/main.py', 'pre-commit']
# ['.gitta/py/main.py', 'post-commit']
