# Totally experimental Sublime Text plugin

This is a POC for parsing build errors using a `.sublime-syntax` instead of
using `.sublime-build`.

Writing complex regexes in the `.sublime-build` quickly becomes a nightmare.
The `.sublime-syntax` allows for better commenting, splitting of regexes, more
complex logic...

## Goal

Provide a possible alternative to the `next_result` command for navigating
build error messages.

## Testing the plugin

* Copy the content of the repo into your Packages folder.
* Add the following keybinding to your key bindings settings:

```json
    { "keys": ["ctrl+f4"], "command": "simple_next_error" },
```

* Open `sample.py` and build it using the `sample` build system.
* Navigate errors using either `f4` for the builtin navigation, `ctrl+f4` for
the syntax based navigation.

## Actually using the plugin

You only need the `simple_errors.py` file to use this plugin, other files can be safely deleted.

## Adding support for a given language / build tool

You'll need to create a `.sublime-syntax` to parse the ouput of your build tool.
The important part is to put the following scopes on the correct elements:

  * entity.name.filename.error
  * constant.numeric.linenumber.error

Once your syntax is ready, just add it under the "syntax" field in the
`.sublime-build` of your build tool.

## Under the hood

The implementation relies on the `view.find_by_selector` API and then is linear
on the number of errors.

So every time you press `ctrl+f4` the API `view.find_by_selector` is called on
the build ouput. The `linenumber` closest to the current position in the build
output is then selected. A `filename` is looked inside the same line, otherwise
the first `filename` found above it, is selected.

## Features

* Syntax based
* Doesn't try to open files that don't exists.

## Caveats

* Doesn't display phantoms
* Doesn't handle column number.
