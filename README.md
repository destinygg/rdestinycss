# r/Destiny CSS

This repository hosts the source scss files to generate the CSS used on the [r/Destiny](https://www.reddit.com/r/destiny) subreddit.

# Requirements

You need the following tools to compile / generate CSS from this repository:
```
Compass
  (depends on) Sass
```

You will also need a copy of the latest [website](https://github.com/destinygg/website) repo adjacent to this repository, such that your directory tree resembles the following:

```
  |-website/
  |-rdestinycss/
```

# Building

There are several make commands available, however you're probably only interested in `make compile`, `make clip` and `make release`.

`make compile` simply compiles the source files and outputs a compressed CSS stylesheet named `stylesheets/rdestiny.css`.

`make clip` performs a `make compile` and copies the contents of the resulting CSS stylesheet into your clipboard (uses xclip).

`make release` performs a `make clip` but also updates the emoticons before compiling the source files.