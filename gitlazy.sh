#!/bin/bash
git config --global credential.helper 'cache --timeout=3600'
echo Git configuration modified. Global credential.helper set to chache with 3600ms timeout.
while [ "1" = "1" ]
do
	echo "Git posted!"
	git add *
	git commit -m "5 minutes passed (gitlazy.sh)"
	git push origin master
	sleep 300
done 
