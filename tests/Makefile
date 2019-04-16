EPUB=`fgrep "filename:" proceedings.yml | sed "s/\"//g" | sed 's/filename: //'`


all: clean
	bookmanager python.yml get --force
	bookmanager python.yml get list


clean:
	rm -rf dest
