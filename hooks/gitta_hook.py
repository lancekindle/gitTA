import os
import sys
from subprocess import check_output, PIPE

def trigger(*args, **kwargs):
    repo_dir = os.getcwd()  # current directory is where repository resides
    hook_path = args[0]  # relative path to hook:  
                        # e.g. '.git/hooks/post-checkout'
    git_hooks_dir, event = os.path.split(hook_path)  # e.g. '.git/hooks',
                                                          # 'post-checkout'
    git_dir_relative, _ = os.path.split(git_hooks_dir)  # e.g. '.git'
    git_dir = os.path.join(repo_dir, git_dir_relative)
    path_to_gitta_pyfiles = os.path.join(repo_dir)  # EVENTUALLY I want to run
            # only code within .git so EVENTUALLY all gitTA files will be in 
            # .git/gitTA (including hooks and py folders) 
    kwargs.update({'git_dir': git_dir, 'repo_dir': repo_dir, 'event': event})
    # now collect important git info that developer may use in kwargs
#    try:
#        cmd = ['git', 'symbolic-ref', '--short', 'HEAD']
#        branch_current = check_output(cmd).strip()
#    except CalledProcessError:  # will print "fatal: ref..." but won't abort
#        branch_current = None  # for when the HEAD is detached
    cmd = ['git', 'rev-parse', '--abbrev-ref', 'HEAD']
    branch_current = check_output(cmd, universal_newlines=True, 
            stdin=PIPE).strip()  # return HEAD if detached
    if branch_current == 'HEAD':
        branch_current = None  # indicate that we are not on a branch
    head_current = check_output(['git', 'rev-parse', 'HEAD'], stdin=PIPE,
            universal_newlines=True).strip()  # get sha1
    kwargs['branch_current'] = branch_current
    kwargs['head_current'] = head_current
    sys.path.append(path_to_gitta_pyfiles)    # add path so that importing main
                                              # and gitta works
    import main
    import gitTA as git # order is important. MUST import main before GitTA
    git.trigger(*args[1:], **kwargs)
