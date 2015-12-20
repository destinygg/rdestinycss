all: compile

update-emoticons:
	cp ../website/scripts/emotes/emoticons/* emoticons/

compile-dev:
	compass compile -s expanded

compile:
	compass compile -s compressed

clip: compile
	cat stylesheets/rdestiny.css | xclip -selection c

release: update-emoticons clip

clean:
	rm -f style.css
	rm -rf stylesheets/