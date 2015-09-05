build:
	virtualenv .virtualenv --system-site-packages;\
	source .virtualenv/bin/activate;\
	pip install -r requirements.txt;
