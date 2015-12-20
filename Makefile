all: compile

update-emoticons:
	cp ../website/scripts/emotes/emoticons/* emoticons/

compile:
	compass compile --sass-dir ./ -s compressed

clip: compile
	cat stylesheets/rdestiny.css | xclip -selection c

release: update-emoticons clip

clean:
	rm -f style.css
	rm -rf stylesheets/