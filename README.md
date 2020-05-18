## Netscape-bookmark importer for qutebrowser

### If the bookmark has a name, then the bookmark will be written to quckmakrs (name link)
### Else the bookmark will be written to urls


## How to use
### $ python3 bookmarks_importer.py command arg
  
### commands:
###        -w        open for writing, truncating the file first
###        -a        open for writing, appending to the end of the file if it exists
###        --help    print help
###        default command '-w' if no command
###    arg:
###        /path/to/bookmarks.html
###        if no arg then script will looks for bookmarks.html in script dir
