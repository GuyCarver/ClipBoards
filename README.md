# Sublime Text Clipboards Package adding multiple clipboards.

## Install

    $ https://github.com/GuyCarver/Clipboards

## Instructions

This package stores the contents of the clipboard when you select another slot and restores that contents when you switch back to that slot.

In order to paste clipboard contents in another application you must make sure that slot is the active one before pasting.

### Settings:

* clipboards = 7

### Key Bindings:

* ctrl+[0-6] sets the currently active clipboard.
* ctrl+shit+[0-7] sets the active clipboard and pastes the contents.
    Slots 4,5 and 6 are special in that they switch back to the previous slot after pasting.

#### Some bindings you may wish to remove.
* keypad_minus = cut
* keypad_plus = copy
* insert = paste
* ctrl+instert = paste and indent
* ctrl+keypad_plus = Append to clipboad
* ctrl+keypad_minus = Append to clipboad and cut from buffer.
* ctrl+x = cut
* ctrl+c = copy
* alt+c = column select mode (changes how up/down work)
* alt+l = line select mode (changes how up/down work)
* alt+shift+c = disables column select mode.
