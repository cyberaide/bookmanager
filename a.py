import ebooklib
from ebooklib import epub
from glob import glob
from pprint import pprint

directory = "/Users/grey/Library/Containers/com.apple.BKAgentService/Data/Documents/iBooks/Books"

books = glob(f"{directory}/*.epub")

pprint (books)

for filename in books:
    print ("SSS")
    print (filename)
    try:
        book = epub.read_epub(filename)
        # print (book.get_metadata())
        print (filename)
        print (book.get_metadata('DC', 'title'))
    except:
        pass
