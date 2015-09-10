# this is the main file that get called
import os
import sys
import gitTA
import colorama
from colorama import Fore, Back  # add color output to terminal: we want anything printed to be VERY visible to user
colorama.init()  # called so that windows colors work
'''
MODIFY THIS FILE! When git is run with certain commands, it also triggers hooks
called git hooks. These hooks are tied in to directly run THIS main.py
which will trigger the functions you've decorated here with gitta.listen('event-name')
your methods can listen for the following events:
CHECKOUT: post-checkout
COMMIT:  pre-commit*, prepare-commit-msg*, commit-msg*, post-commit
PUSH: pre-push*
MERGE: post-merge
... and even more: pre-applypatch*, applypatch-msg*, post-applypatch,
post-rebase, pre-auto-gc*
You can abort git actions marked with * by raising an error in your listening method. e.g. you can abort a commit by raising an error in any of the three commit hooks.
I strongly suggest you search 'git hook tutorial' online to determine which hook you most want. https://www.atlassian.com/git/tutorials/git-hooks/local-hooks
'''
git = gitTA.gitta()

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
    print(Fore.GREEN)
    print(args, kwargs)

@git.listen('post-merge')
def postmerge(*args, **kwargs):
    print(Fore.GREEN)
    print(args, kwargs)

if __name__ == '__main__':
    gitTA.gitta.trigger_all_instances(45, event='post-checkout') 
    # example of what might get passed to postcheckout
    # the garbled message that appears before (45, ) is the Fore.GREEN. On normal terminals this garbled output will NOT appear
    

# ['.gitta/py/main.py', 'pre-push', 'origin', 'https://github.com/lancekindle/test.git']
# ['.gitta/py/main.py', 'pre-commit']
# ['.gitta/py/main.py', 'post-commit']
