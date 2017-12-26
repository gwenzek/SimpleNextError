# Totally experimental Sublime Text plugin

This is a POC for parsing build errors using a `.sublime-syntax`
instead of using `.sublime-build`.

Writing complex regexes in the `.sublime-build` quicly becomes a nightmare.
The `.sublime-syntax` allows for better commenting, splitting of regexes, more
complex logic...

Goal: provide a possible alternative to the `next_result` command for navigating build error messages.
