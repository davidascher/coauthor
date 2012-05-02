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

	./run.sh &
	cp APIKEY.txt ../../coauthor_site

Start Django:

	python manage.py runserver &

Install, configure and run the front-end proxy (in dev, I use node-http-proxy -- in production, configure your favorite solution (see [instructions](https://github.com/Pita/etherpad-lite/wiki/How-to-put-Etherpad-Lite-behind-a-reverse-Proxy)):

	npm install -g http-proxy
	# edit http_proxy.config to point to the right ports for etherpad and django
	http-proxy --config http_proxy.config --port 8081 # or whatever port you want

Should work!
