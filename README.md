# gitTA
Listen to git hooks, and trigger your functions simply with gitTA.
```
import gitTA as git

@git.listen('pre-push')
def run_tests(*args, **kwargs):
	import test
    test.all_your_things()
    if test.failed:
    	raise BaseException('abort the push' + test.feedback)
```
With the above code in main.py, the function **run_tests** will trigger each time **git push** is called, with the option to abort the push by raising an error.
In fact, you can listen to **all** local git hooks, including:

1. **pre-commit**
2. **commit-msg**
3. **post-commit**
4. **post-checkout**
5. .... and many more!

With these hooks, its possible to:

1. Encrypt a commit message after user input
2. Abort pushes if the branch is master
3. Correct file-permissions after branch changes
4. Undo branch changes to always stay on master
5. Change files after committing
6. Most anything good or evil... use your powers responsibly

To install gitTA, copy gitTA into a local git repo of your choice. Edit main.py to your liking, then run the install script (located in ./bash/install_githooks.sh), which will move gitTA into your .git directory, overwriting any current hooks with its own.
gitTA is local only -- the install script MUST be run each time another user clones your repository.  In short, it's a local tool that must be installed by the user; there is no way to have gitTA pre-installed in a repository, short of passing it around in a zipfile or setting it up as a git template. You can, however, include gitTA in your repository as a visible folder and ask that the user run the install script prior to using it.