import os
import sys

def trigger(*args, **kwargs):
    repo_dir = os.getcwd()  # current directory is where repository resides
    hook_path = args[0]  # relative path to hook:  e.g. '.git/hooks/post-checkout'
    git_hooks_dir, event = os.path.split(hook_path)  # e.g. '.git/hooks',   'post-checkout'
    git_dir_relative, _ = os.path.split(git_hooks_dir)  # e.g. '.git'
    git_dir = os.path.join(repo_dir, git_dir_relative)
    path_to_gitta_pyfiles = os.path.join(repo_dir)  # EVENTUALLY I want to run only code within .git
    # so EVENTUALLY all gitTA files will be in .git/gitTA  (including hooks and py folders)
    sys.path.append(path_to_gitta_pyfiles)    # add path so that importing main and gitta works
    import main
    import gitTA  # order is important. MUST import main before GitTA
    gitTA.gitta.trigger_all_instances(*args[1:], event=event, git_dir=git_dir, repo_dir=repo_dir, **kwargs)
