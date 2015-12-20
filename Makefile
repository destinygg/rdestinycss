all: compile

compile:
	compass compile --sass-dir ./ -s compressed

clip: all
	cat stylesheets/rdestiny.css | xclip -selection c

clean:
	rm -f style.css
	rm -rf stylesheets/