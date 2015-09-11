from collections import defaultdict
import os
import subprocess

''' this is the gitTA module. You do not do not modify this file, but instead modify main.py
to run the code you want
'''
def listen(event_name):
    ''' call this function for simplicity when registering
    to listen to a hook-call
    '''
    def wrapper(func):
        g = Hook()
        g._add_event_function(event_name, func)
        return func
    return wrapper

def trigger(*args, **kwargs):
    Hook.trigger_events_in_all_instances(*args, **kwargs)


class Hook:
    event_functions = defaultdict(list)
    _class_instances = []

    def __init__(self):
        self.event_functions = self.event_functions.copy()
        self._hold_self_reference_in_class(self)

    @classmethod
    def _hold_self_reference_in_class(cls, self):
        cls._class_instances.append(self)

    @classmethod
    def trigger_events_in_all_instances(cls, *args, **kwargs):
        repo = kwargs.get('repo_dir', None)
        for self in cls._class_instances:
            if repo:
                os.chdir(repo)  # verify each function triggers with cwd in repository
            self.trigger(*args, **kwargs)
    
    def _add_event_function(self, event_name, func):
        self.event_functions[event_name] = func

    def listen(self, event_name):
        ''' calling a decorator with an argument is significantly different than calling an argumentless decorator.
        so in this case, listen only gets the event_name, and the wrapper function is called immediately with the
        function to decorate
        : a wrapper to call each "registered/wrapped" event function when the event name matches 
        '''
        def wrapper(func):
            ''' wrapper gets called immediately with the function to register. What wrapper returns will be the
            replacement function
            '''
            self._add_event_function(event_name, func)
            return func  # return function unmodified
        return wrapper
        
    def trigger(self, *args, **kwargs):
        event = kwargs.get('event', None)
        if event not in self.event_functions:
            return  # it might also be good to log somewhere that no function was called
        f = self.event_functions[event]
        f(*args, **kwargs)  # trigger function


class Branch:

    def undo_checkout(self, *args, **kwargs):
        ''' for the evil :D. re-checkout the previous branch '''
        print('going to undo checkout')
        print(kwargs)
        head_previous = kwargs['head_previous']
        print(head_previous)
        # have to prevent undo_checkout from causing git checkout to trigger
        # post-checkout, which causes undo_checkout to recursively trigger...
        repo_dir, git_dir = kwargs['repo_dir'], kwargs['git_dir']
        os.chdir(git_dir)
        os.chdir('hooks')
        os.rename('post-checkout', 'post-checkout.disable')
        os.chdir(repo_dir)  # have to change back to repo_dir to run git
        subprocess.call(['git', 'checkout', head_previous])
        os.chdir(git_dir)
        os.chdir('hooks')
        os.rename('post-checkout.disable', 'post-checkout')
