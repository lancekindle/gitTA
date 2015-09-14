from collections import defaultdict
import os
import subprocess
from contextlib import contextmanager

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

@contextmanager
def ignored(event_name):
    ''' call this contextmanager function with an event_name to ignore while
    in scope (before the with-statement exits. As an example:
    with ignored('pre-push'):
        do_some_pushing()
    # outside scope, pre-push event will be caught once again
    if an event is ignored multiple times in nested functions like:
    with ignored('pre-push'):
        with ignored('pre-push'):
            do_some_pushing()
        do_more_pushes()
    do_caught_pushes()

    then only do_caught_pushes() will trigger pre-push listeners, as it lies
    outside the scope of the first ignored event. Neither do_more_pushes nor
    do_some_pushing will trigger pre-push listeners.
    '''
    # disable event here...
    kwargs = Hook.get_kwargs()  #  Hook will always have the kwargs since 
            # it is responsible for triggering all the functions
    repo_dir, git_dir = kwargs['repo_dir'], kwargs['git_dir']
    os.chdir(git_dir)
    os.chdir('hooks')  # cd into .git/hooks directory
    is_first_context = False
    if os.path.exists(event_name):
        os.rename(event_name, event_name + '.ignore')  # "ignore" file by renaming so it won't trigger again during this context
        is_first_context = True
    os.chdir(repo_dir)  # reset directory back to reference (where we expect)
    try:  # http://preshing.com/20110920/the-python-with-statement-by-example/
        yield None  # this try-finally block is essential to make sure that
    finally:        # we re-enable event, even if horrible errors happen
        if is_first_context:  # we only re-enable event listening if this was from the first context to ignore this event
            os.chdir(git_dir)
            os.chdir('hooks')  # enable event here -- this part will be done no matter what.
            os.rename(event_name + '.ignore', event_name)


class Hook:
    event_functions = defaultdict(list)
    _class_instances = []
    _kwargs = {}

    def __init__(self):
        self.event_functions = self.event_functions.copy()
        self._hold_self_reference_in_class(self)

    @classmethod
    def _hold_self_reference_in_class(cls, self):
        cls._class_instances.append(self)

    @classmethod
    def _set_kwargs(cls, kwargs):
        cls._kwargs.clear()
        cls._kwargs.update(kwargs)

    @classmethod
    def get_kwargs(cls):
        ''' get keyword arguments that have been passed to every listening
        function. Can be used as a way to clean up function calls
        '''
        return cls._kwargs.copy()
    
    @classmethod
    def trigger_events_in_all_instances(cls, *args, **kwargs):
        repo = kwargs.get('repo_dir', None)
        cls._set_kwargs(kwargs)  # verify kwargs is the same for each function
        event = kwargs['event']
        with ignored(event):  # automatically ignore just-triggered event. Helps prevent recursion if user does the same action through python
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
        ''' for the evil :D. re-checkout the previous branch / commit 
        must be called from a post-checkout function
        '''
        print('going to undo checkout')
        print(kwargs)
        if kwargs.get('branch_previous', None) is not None:
            previous = kwargs['branch_previous']
        else:
            previous = kwargs['head_previous']
        print(previous)
        with ignored('post-checkout'):  # prevent accidental recursion
            subprocess.call(['git', 'checkout', previous])
        
