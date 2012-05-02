Motivation
------------

This is an experiment in making a derivative of etherpad which is better suited to coauthoring of
documents for publication to a broader community.  I've found that etherpad's UI, which is awesome 
for small teams of 2-3, ends up 

* chaotic when dealing with a dozen or more authors.
* hard for _readers_ to process, primarily because the editing UI and the inevitable markup gets in the way of reading.

Also, I've found that it's hard to keep track of what etherpads I've authored or read. 
Team etherpads help, but not enough, especially because I have a different password for each team.

To address these issues, I'm trying the following:

* every user auths using Persona (there are no anonymous users)
* every user gets a personal 'team-of-one', and (someday) will be able to manage groups as in 'old' etherpad
* pads can be authored using the etherpad editing tools (bold, etc.), or using markdown
* pads can be published -- those URLs are what you send to people you just want to read a pad, not coauthor it.


Status
-------

* Persona login works
* Currently all publishing assumes markdown markup
* No real team management features yet
* Lots more work to do, but the general framework of using Persona + etherpad-lite seems to work ok.

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

