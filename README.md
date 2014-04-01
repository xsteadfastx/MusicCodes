MusicCodes
==========

A webapp for generating and managing download codes and serving the files.

![screenshot](screenshot.jpg)

## Usage ##

```
Usage:
    MusicCodes.py run
    MusicCodes.py create <number>
    MusicCodes.py add <number>
    MusicCodes.py show
    MusicCodes.py voucher --all
    MusicCodes.py voucher <from> <to>
    MusicCodes.py reset <code>
    MusicCodes.py -h | --help

Options:
    -h --help                   Show this screen.
    run                         Starts MusicCodes Web.
    create <number>             Creates DB with number of codes.
    add <number>                Adds number of codes to existing DB.
    show                        Show all DB entries.
    voucher --all               Creates a voucher PDF with all codes.
    voucher <from> <to>         Creates a voucher PDF with a range of codes.
    reset <code>                Resets the USED counter for a specific code.
```

### voucher ###
For using the voucher option you need to have latex installed. Needs `latexpdf`.

## Todo ##
- `add` to create new download codes
