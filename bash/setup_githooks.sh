#!/bin/sh
# symlink the files in gitTA/hooks/* to .git/hooks/*
# notice that I have to use relative imports. So if the depth to a common parent directory changes
# then the ../../ may change to a ../ or a ../../../
# it all depends on where the actual hooks are stored relative to common parent directory
# vs .git/hooks stored relative to actual hooks
cd ../hooks
for f in ./*
do
   echo $f
   ln -sf ../../gitTA/hooks/$f ../../.git/hooks/$f
done
