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


parser = BookmarksParser()
origin_bookmarks = ""

try:
    origin_bookmarks = argv[1]
except IndexError:
    print("Missed path to bookmarks.html")
    exit()

try:
    with open(origin_bookmarks, "r", encoding="utf-8") as f:
        parser.feed(f.read())
except FileNotFoundError:
    print(f"\nNo such file: '{origin_bookmarks}'"
          f"\nPlease input correct path to bookmarks.html.")
    exit()

bookmarks_lst = list(
    filter(
        lambda x: len(x) == 2 or x[0].startswith("http"), parser.get_datas()
    )
)

if (urls_list := list(filter(lambda x: len(x) == 1, bookmarks_lst))):

    urls_str = "\n".join([link for sublist in urls_list for link in sublist])

    with open("urls", "w", encoding="utf-8") as f:
        f.write(urls_str)

if (qk_list := list(filter(lambda x: len(x) == 2, bookmarks_lst))):

    qk_str = "\n".join([" ".join(item) for item in qk_list])

    with open("quickmarks", "w", encoding="utf-8") as f:
        f.write(qk_str)

