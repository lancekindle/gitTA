
''' copy hooks to .git/hooks so that gitta can run each time user commits, pushes, or merges '''
import os
import shutil
os.chdir('.gitta/hooks') # cd .githooks
for f in os.listdir():  #list all files
   print(f)
   if os.path.isdir(f):  # skip operations on folders
      continue
   shutil.copy2(f, '../../.git/hooks/' + f, follow_symlinks=True) # copy file over to .git/hooks/
   
#
#  ==== bash version ==== #
##cd .githooks
##for f in ./*
##do
##   echo $f
##   ln -sf ../../.githooks/$f ../.git/hooks/$f
##done
