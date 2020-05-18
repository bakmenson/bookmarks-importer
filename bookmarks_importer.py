from html.parser import HTMLParser
from sys import argv, exit


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
argv_bookmarks = None
argv_command = None
open_mode = str()

len_argv = len(argv)

if len_argv >= 2:
    try:
        argv_command = argv[1] if argv[1].startswith("-") else None
        if argv_command and argv_command not in {"-w", "-a", "--help"}:
            raise ValueError

        argv_bookmarks = argv[1] if not argv[1].startswith("-") else None
    except IndexError:
        pass
    except ValueError:
        print("Wrong command.")
        print_help()
        exit()

if len_argv == 3:
    try:
        argv_bookmarks = argv[2] if not argv[2].startswith("-") else None
    except IndexError:
        pass

bookmarks = argv_bookmarks if argv_bookmarks else "bookmarks.html"

urls_path = "urls" if not argv_command else "urls"
quickmarks_path = "quickmarks" if not argv_command else "quickmarks"

try:
    open_mode = "a" if "a" == argv_command.replace("-", "") else "w"
except AttributeError:
    open_mode = "w"

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

    urls_str = "\n".join([link for sublist in urls_list for link in sublist])

    write_bookmarks(urls_path, open_mode, urls_str)

if (qk_list := list(filter(lambda x: len(x) == 2, bookmarks_lst))):

    qk_str = "\n".join([" ".join(item) for item in qk_list])

    write_bookmarks(quickmarks_path, open_mode, qk_str)
