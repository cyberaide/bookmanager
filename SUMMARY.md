Bookmanager

The problem:

	We have a number of distributed documentation written by
	different groups and organizations and users. Although we can
	put an html link up with the collection Students, researchers,
	tutorial participants can benefit from a tool that integrates
	all of them into a single Document and not just a collection
	of links. This allows for a “book” like distribution of the
	content written by various people and hosted on various and
	GitHub repositories.

	In our case it also serves as a mechanism for generating class
	proceedings of reports developed by students so they can take
	them “home” after they did the class.

The solution

	We have a simple tool called bokmanager that creates an epub
	of documents specified in a yaml table of contents. The
	documents will be fetched from the url, the images downloaded
	and an epub generated. This epub (if not to big) can than be
	browes not only on your computer, but also on your iPads and
	cell phones, so you can add them to your book collection

Source

	https://pypi.org/project/cyberaide-bookmanager/
	https://github.com/cyberaide/bookmanager

Sample yaml file

    https://github.com/cyberaide/bookmanager/blob/master/tests/python.yml

Summary of Benefit

	* Simple to use
	* leverages pandoc, so more formats in future will be
	* supported
	* pulls together information from several sources
	* auto generated title page
	* epub
