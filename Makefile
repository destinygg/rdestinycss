PIP=scripts/venv/bin/pip

all: compile

env:
	python3 -m venv scripts/venv
	$(PIP) install praw

update-emoticons:
	cp ../website/scripts/emotes/emoticons/* emoticons/

compile-dev:
	compass compile -s expanded

compile:
	compass compile -s compressed

clip: compile
	cat stylesheets/rdestiny.css | xclip -selection c

release: clean update-emoticons clip

clean:
	rm -f style.css
	rm -rf stylesheets/
	rm -f emoticons-*.png