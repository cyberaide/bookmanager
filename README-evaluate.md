# Evaluation of Tools

We evaluated prior to developping bookmanager a number of tools. However
none of them could deliver a tool that

* is easy to use by the users while setting it up and developping content
* allows the integration of distributed documents managed in github


We evaluated Sphinx, LaTeX, and Markdown.

* **Sphinx:** We also developed a sphinx-based system that creates an
  online Web page from the material. We wrote initially all content in
  restructured Text. The content was easy to write while we leveraged
  advanced editors that allowed semi-automated rendering of the
  contents.  We contributed about 1000 pages of class
  material. However, we found that while developing the content with a
  group, that circular dependencies were introduced in the Web pagse
  that resulted in students iterating through the same pages over and
  over, after which they got lost. Even though we provided a table of
  content student did get lost as they did not consult the
  table. After consulting with the students we got the feedback to
  distribute the content as a book and not as Web page. Although
  Sphinx provided the feature to create a book, it did not easily
  provide us with the mechanism for integrating distributed content
  easily hosted in multiple repositories. Creation of the book while
  using sphinx took less than 5 minutes upon change.

* **LaTeX:** Latex is a very powerful tool and was used to create class
  content. It is has superior features to create books in beautiful
  output format. The creation of custom content can be achieved with
  the LaTeX include feature while making sure that the distributed
  github repositories are first cloned into the local environment in a
  consistent fashion and then the content is included. Although LaTeX
  provided mechanisms to organize the content, in practice we found
  that entry level students that have not been exposed to LaTeX had a
  difficult time to contribute content in LaTeX. Furthermore, we also
  found that a number of advanced students had never used LaTeX
  before. Instead of using our simple templates, student’s also
  started developing their own macros, and plugins that were
  incompatible with some more advanced LaTeX packages. Thus, LaTeX to
  develop course content was not suitable.  Creation of the book while
  using LaTeX took about 5- 10 minutes upon change.

* **Markdown via Bookamanger:** Taking the lessons from Sphinx and
  LaTeX we converted all content to to markdown. This was a
  significant effort despite the use of conversion tools such as
  pandoc as we originally used some very advanced features in LaTeX
  and Sphinx. The conversion was conducted over a period of 3
  month. One of the advantages of this approach was that we could use
  GitHub GUI as an editor and leverage (other than references, and
  bibliographies) the build in rendering capabilities of markdown in
  github. While now being able to leverage Github and markdown, the
  number of student support to contribute and develop content in a
  particular format was significantly reduced. We tested out the
  approach of students contributing to new and existing course content
  and found that contributions can be solicited easily. Most
  importantly, we improved the build creation of the book
  drastically. While the first version of bookmanager was driven by
  very sophisticated makefiles, we replaced them in the second version
  with a python program distributed in PyPi.  This had the following
  consequences (1) students could easily create the book on their
  local computes (2) the creation of the book is possible on Windows
  as it does not come with makefiles (3) students are able to create
  their customized books based on lessons they like to integrate in
  their educational experience The creation of the book incontarste to
  the other systems has been drastically reduced and is now less than
  30 seconds.


Note: all benchmarks have been conducted on a MacPro from 2017 with 16 GB RAM.
