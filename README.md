Installation
------------

First, get the repo and the submodules:

	git clone git@github.com:davidascher/coauthor.git
	cd coauthor
	git submodule init
	git submodule update

Then, configure etherpad:

	cd vendor/etherpad-lite
	cp settings.json.template settings.json
	edit that file!

Start etherpad, and copy the APIKEY from etherpad to the django dir:

	bin/run.sh &
	cp APIKEY.txt ../../coauthor_site

Start Django:
	# make sure you have 1.3.1:
	sudo pip install --upgrade django==1.3.1
	cd ../../coauthor_site
	python manage.py syncdb
	python manage.py runserver &

Install, configure and run the front-end proxy (in dev, I use
node-http-proxy -- in production, configure your favorite solution
(see [instructions](https://github.com/Pita/etherpad-lite/wiki/How-to-put-Etherpad-Lite-behind-a-reverse-Proxy)):

	cd ..
	npm install http-proxy
	# edit frontend.js to point to the right ports for etherpad and django
	node frontend.js

Should work!  Go to http://localhost:8081 and see.

If you don't use 8081 as your front-end port, then you'll want to
update coauthor_site/setting.py, or the BrowserID verification will fail.

