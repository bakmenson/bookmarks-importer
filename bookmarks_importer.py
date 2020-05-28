from html.parser import HTMLParser
from sys import argv, exit
from os import getcwd
from pathlib import Path


class BookmarksParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.datas = []
        self.tag_data = []

    def get_datas(self):
        return list(filter(None, self.datas))

    def handle_starttag(self, tag, attrs):
        for attr in attrs:
            if tag == "a" and attr[0] == "href":
                self.tag_data.append(attr[1])

    def handle_data(self, data):
        self.tag_data.append(data.strip())
        self.tag_data.reverse()
        self.datas.append(list(filter(None, self.tag_data)))
        self.tag_data = []


def write_bookmarks(file_path, mode, string):
    with open(file_path, mode, encoding="utf-8") as f:
        if mode == "a":
            f.write("\n" + string)
        else:
            f.write(string)


def print_help():
    print(
        """
    Usage: python3 bookmarks_importer.py <command> [<arg>]

    commands:
        -w        open for writing, truncating the file first
        -a        open for writing, appending to the end of the file if it exists
        --help    print help

        default command '-w' if no command

    arg:
        /path/to/bookmarks.html

        if no arg then script will looks for bookmarks.html in script dir
    """
    )


parser = BookmarksParser()
argv_bookmarks = ""
argv_command = ""

if len(argv) > 1:
    for i in range(1, len(argv)):
        if argv[i].startswith("-"):
            argv_command = argv[i]

        if not argv[i].startswith("-"):
            argv_bookmarks = argv[i]

if argv_command == "--help":
    print_help()
    exit()

bookmarks = argv_bookmarks if argv_bookmarks else "bookmarks.html"

open_mode = "a" if argv_command == "-a" else "w"

destination_choice = None

while True:
    print("1) Save urls and quickmarks here.\n2) Overwrite urls and"
          " quickmarks in ~/.config/qutebrowser,\n   be careful if"
          " command == '-w' you can lost current urls and quickmarks values.")

    try:
        destination_choice = int(input("\n>>> "))
    except ValueError:
        continue

    if 0 < destination_choice < 3:
        break

    continue

home_dir = str(Path.home())

urls_path = getcwd() + "/urls" if destination_choice == 1 \
    else home_dir + "/.config/qutebrowser/bookmarks/urls"

quickmarks_path = getcwd() + "/quickmarks" if destination_choice == 1 \
    else home_dir + "/.config/qutebrowser/quickmarks"

try:
    with open(bookmarks, "r", encoding="utf-8") as f:
        parser.feed(f.read())
except FileNotFoundError:
    print(f"\nNo such file: '{bookmarks}'"
          f"\nPlease input correct path to bookmarks.html.")
    exit()

bookmarks_lst = list(
    filter(
        lambda x: len(x) == 2 or x[0].startswith("http"), parser.get_datas()
    )
)

if (urls_list := list(filter(lambda x: len(x) == 1, bookmarks_lst))):

    urls_str = "\n".join([url for sublist in urls_list for url in sublist])

    write_bookmarks(urls_path, open_mode, urls_str)

if (quickmarks_list := list(filter(lambda x: len(x) == 2, bookmarks_lst))):

    quickmarks_str = "\n".join([" ".join(item) for item in quickmarks_list])

    write_bookmarks(quickmarks_path, open_mode, quickmarks_str)
