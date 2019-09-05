# Community Driven Creation of Educational Material with Bookmanager

* Gregor von Laszewski, laszewski@gmail.com
* G. C. Fox

## Abstract

We report here on the motivation and findings for Bookmanager

## Introduction

The pervasive importance of computing and cyberinfrastructure is broadly acknowledged in many areas of commercial, government, and academic endeavors. This is reflected in Indiana University's (IU) plan to build its new Intelligent Systems Engineering (ISE) program with a strong computational and information technology basis and situate it in the School of Informatics, Computing, and Engineering (SICE). As curriculum changes and integrates modern concepts and practices, students are changing as well, and we must support the learning modes of Generation Z.

This proposal takes what we have learned from a four-year undergraduate curriculum designed ab initio and taught so far to our first two undergraduate classes, and invests it into developing active modules that are customized for Cyberinfrastructure Contributors (CIC) communities nucleated, built, and sustained via the dynamic use of GitHub.

We rework carefully chosen subsets of our curriculum, including the following topics: Cloud Computing, Big Data Applications and Analytics, Networking, High Performance Computing, Artificial Intelligence/Machine Learning, and Information Visualization. The content will be offered online, in a modular format, and will reflect the needs of today’s tech-savvy students by incorporating successful community building tools. We will support Generation Z CyberTraining with all of the thriving approaches used by the Apache Software Foundation, including Meetups, Workshops or Hackathons and follow our current approach that all student projects are stored in open GitHub repositories and automatically made available for later learners and educators. While the project primarily focuses on developing content for training the CIC communities, we will offer a few modules for domain scientists and engineers, e.g. the cyberinfrastructure Users (CIU) that exploit advanced CI methods for research in nanoengineering and bioengineering. Appropriate modules will be made available on portals such as nanoHUB where appropriate to train a wider set of CIU communities. This project is leveraging the very significant IU investment in new faculty and new curricula to develop modules sourced from these curricula and customized for CIC via the GitHub based community model. All can contribute to the course improving the text, the software and providing an amazing set of examples and we hope in this project to show that we can build both learning and sustainability communities by using the proven techniques of the open source software community.


## Evaluation of Tools

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
