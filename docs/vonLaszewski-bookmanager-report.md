# Community Driven Creation of Educational Material with Bookmanager

* Gregor von Laszewski, laszewski@gmail.com
* G. C. Fox

Digital Science Center, Indiana University, Bloomingtopn, IN 47401

## Abstract

We report here on the motivation and findings for Bookmanager

## Introduction

The pervasive importance of computing and cyberinfrastructure is broadly
acknowledged in many areas of commercial, government, and academic
endeavors. This is reflected in Indiana University's (IU) plan to build
its new Intelligent Systems Engineering (ISE) program with a strong
computational and information technology basis and situate it in the
School of Informatics, Computing, and Engineering (SICE). As curriculum
changes and integrates modern concepts and practices, students are
changing as well, and we must support the learning modes of Generation
Z.

This proposal takes what we have learned from a four-year undergraduate
curriculum designed ab initio and taught so far to our first two
undergraduate classes, and invests it into developing active modules
that are customized for Cyberinfrastructure Contributors (CIC)
communities nucleated, built, and sustained via the dynamic use of
GitHub.

We rework carefully chosen subsets of our curriculum, including the
following topics: Cloud Computing, Big Data Applications and Analytics,
Networking, High Performance Computing, Artificial Intelligence/Machine
Learning, and Information Visualization. The content will be offered
online, in a modular format, and will reflect the needs of today’s
tech-savvy students by incorporating successful community building
tools. We will support Generation Z CyberTraining with all of the
thriving approaches used by the Apache Software Foundation, including
Meetups, Workshops or Hackathons and follow our current approach that
all student projects are stored in open GitHub repositories and
automatically made available for later learners and educators. While the
project primarily focuses on developing content for training the CIC
communities, we will offer a few modules for domain scientists and
engineers, e.g. the cyberinfrastructure Users (CIU) that exploit
advanced CI methods for research in nanoengineering and bioengineering.
Appropriate modules will be made available on portals such as nanoHUB
where appropriate to train a wider set of CIU communities. This project
is leveraging the very significant IU investment in new faculty and new
curricula to develop modules sourced from these curricula and customized
for CIC via the GitHub based community model. All can contribute to the
course improving the text, the software and providing an amazing set of
examples and we hope in this project to show that we can build both
learning and sustainability communities by using the proven techniques
of the open source software community.


## Objectives

We had the following specific objectives:
 
Develop concrete course material that we can distribute on GitHub.

1. Verify if our plan to host course material on GitHub is possible and
   allows for contributions by the students and AI’s.

2. Identify if material could be easily uploaded to existing course
   management systems used at IU

3. Identify educational Gaps the students have to improve our proposed
   suggested courses.


## Activities

Our main activities were spread across the areas of Educational
Component Development, enabling technologies, and 	Outreach
Activities. In particular we conducted the following activities in each
of the areas:

* **Educational Component Development:**  We packaged course material
  for the classes Engineering Cloud Computing, Big Data Applications
  Intelligent Systems Engineering for Undergraduates (which is a mix of
  Machine Learning and Cloud Computing)
* **Enabling technologies:** We developed a tool called bookmanager that
  can create individualized course material into a book format allowing
  individualized content to be included from distributed educational
  content located in distributed repositories on GitHub. We evaluated
  online tools used at Indiana University to distribute our content
  including CANVAS and EdX for the automated upload of course content
* **Outreach Activities:** We hosted and reused material from our
  curriculum to educate minority serving students as part of an REU at
  Indiana University. This included topical lessons form Python, Linux,
  AI and Data Processing We supported the “Science Gateway Coding
  Institute” at Elizabeth City State University, a minority serving
  institution with course material and teaching support. Our next major
  event is Fall 2019 jointly with the nanoBIO project and we will offer
  this cyberinfrastructure material with nanoengineering and
  bioengineering to a visiting group of about 20 undergraduates from
  Minority Serving Institutions.


## Evaluation of Tools

One of the impoprtant precurser to our effort was to
evaluate some existing tools to see if they could be reused without any
new development.  However none of the tools could deliver a tool that

* is easy to use by the users while setting it up and developping content
* allows the integration of distributed documents managed in github

One of our stated goals for this activity is to not only develop
educational material by a single faculty member, but to allow multiple
faculty members and more importantly the students from the class to
contribute content to leverage their potential technology experiences
into the courses. Thus we decided to use GitHub as it allows student to
openly contribute and as it is a tool with wide community acceptance.
However GitHub does not provide a tool that allows the easy integration
of content developed not only in one repository, but multiple. In order
to coordinate the creation of content from GitHub we have evaluated and
practically used multiple technologies to identify a suitable tool for
creating customized curricula including Sphinx, LaTeX as well as CANVAS
and OpenEdX. 

We evaluated Sphinx, LaTeX, and Markdown (in addition to Course
management tools such as CANVAS and OpenEdX).

We summarize our findings:

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


Selected features of the bookmanager include:

1. Bookmanager allows easily to combine course material from different
   authors distributed in GitHuB
2. We developed a special YAML format that allows the table of
   contents to be easily formatted and includes a mechanism to replace
   variable values defined in the yaml file, within the yaml file.
   This feature is now also used in some of our cloud research
   projects that we conducted as part of the class deliverables.
3. Easy formulation of a table of content in easy to read YAML format
4. Automated bibliography download from remote content repositories
5. Integration of bibliographies formulated for example in BibTex or
   other formats that can be converted to BibTex
6. Automated image download from remote content repositories
7. Ability to create PDF documents
8. Ability to create ePub documents. As GenerationZ students almost
   all had a tablet on which they could download books in ePub format
   this is our preferred format of distribution.
9. Allow bookmanager to be installed on various platforms such as
   Linux, macOS, Windows while assuming a python interpreter is
   present (all of our GenerationZ students are educated in the
   installation of python on their computers) a program that is easy
   to install on the major operating systems to be able to create
   custom books in our future activities planned for next year.



# Results

We have the following significant results
 
We have developed course material with over ~52K lines of teaching
material, with ~275K words and ~1.9M characters which are freely
available. Major educational course platform are not suitable to support
individual adapted course content: Neither CANVAS, nor OpenEdX allow the
pragmatic offline development of course material with easy to use
standard tools and then importing the content. We verified this with
booth platforms. In case of  OpenEdX we verified that an open source
tool to import LaTeX is not supported by OpenEdX and while experimenting
with it major limitations making it not suitable for use. In OpenEdX and
Canvas content must be developed in the platform itself through GUI’s
that are slow and are best suited for those developing traditional
course material that does not allow the adaptation of individual course
adaptation for students. The lack of an import feature for external
developed material requires a “vendor” lock in which is undesirable as
we strive to make the content of the modules available to everyone
regardless if they are OpenEdX, Canvas, or are part of another Learning
content management system. Existing tools such as LaTeX and sphinx have
disadvantages that make them not easily usable due to the complexity of
the tools or their setup. Due to these limitations, we are developing a
tool called  cyberaide bookmanager, that easily can generate custom
educational material for students based on their educational
requirements which are distributed in github We have released a version
to the public on github and pypi.

Based on community feedback we not only allow content to be distributed
in github, but also the local file system The tool will be an integral
part in two upcoming classes at Indiana University while targeting
residential and online students. We have showcased that the tool can be
integrating course material written in different formats including
LaTeX, restructured text, and org mode. The tool is using pandoc which
supports a great number of other formats. This was one of our year 3
goals, but was accomplished already in year 1.

 
We have developed the following components for the course content:

1. Introduction to Cloud Computing (700+ pages)
2. Introduction to Python programming (300+ pages),
3. Introduction to Linux (50 pages)
4. Introduction to Git (30 pages)
 
Courses taught
 
1. As part of the “Science Gateway Coding Institute” at Elizabeth City
   State University (http://nia.ecsu.edu/sgci/sgci_ci/ci2019/) a 4
   week workshop was held to which we contributed a number of lessons
   taught to the students by Jerome Mitchel a former PhD student of
   Dr. Fox. The material we presented focused on introduced the
   students to concepts such as
   
   1. Introduction to Python programming
   2. Introduction to Shell Scripting
   3. Introduction to Jupyter notebooks
   4. Introduction to Linux
   5. Introduction to Git
 
The workshop participants were prepared through a number of educational
activities That includes a significant number of lessons that we have
made available in our online course material lessons. This included not
only lessons related to programming, but also to introduce students to
data analytics, of which clustering with k-means is just one example.
 
# Future Activities

We will conduct the following activities:

Course Material:

* We will be developing new and updating existing course material

Course Material Distribution and Integration Framework:

* We will be interfacing with other faculty members for the
  development of new course material.  Provide workflows on how to
  integrate material that was originally developed in CANVAS and
  provides vendor lock in.  This will include the evaluation of how to
  deal with content that is vendor specific such as CANVAS forcing the
  course developer to predominantly using CANVAS.
* We will improve bookmanager and identify add ons to deal with
  formats other than markdown including org mode and LaTeX.
* We will explore OpenEdX more carefully and identify possibilities of
  using bookmanager as a generator for content that than can be
  referred to or integrated into OpenEdX Integration of DOI’s via zenodo
  or the use of arxiv.org for the distribution of our material

Outreach:

* Integration of other faculty members as content contributors
* Organization of Hackathons as part of seperate or class Lab
  activities in ongoing and future teaching material gatherings.

## Conclusion

The development of Bookmanager was a great success as we have now a tool
than not only can be used by experts but also novice and student
participants in educational activities at Indiana University. Content
can now be customized on individual students needs and students can even
perform this activity themselfs. A significant amount of information has
been made available for the creation of courses.

## References

1. G. von Laszewski, G. C. Fox, Community Driven Creation of
   Educational Material with Bookmanager,
   <https://github.com/cyberaide/bookmanager/blob/master/README-evaluate.md>
2. G. C. Fox, G. von Laszewski (Editors), Intelligent Systems
   Engineering, <https://laszewski.github.io/book/222/>
3. G. C. Fox, G. von Laszewski (Editors), Big Data Applications and
   Analytics, <https://laszewski.github.io/book/big-data/>
4. G. von Laszewski (Editor), Cloud computing, Fall 2019. Bloomington,
   Indiana: Indiana University, Spring 2019 [Online]. Available:
   <https://laszewski.github.io/book/cloud/>
5. G. von Laszewski (Editor), Cloud technologies,
   Fall 2019. Bloomington, Indiana: Indiana University, Spring 2019
   [Online]. Available:
   <https://cloudmesh-community.github.io/book/vonLaszewski-cloud-technologies.epub?raw=true>,
   Please note a new version is under development.
6. G. von Laszewski (Editor), Python for cloud computing,
   Spring 2019. Bloomington, Indiana: Indiana University, 2019
   [Online]. Available: <https://laszewski.github.io/book/python/>,
   Please note a new version is under development.
7. G. von Laszewski (Editor), Linux for cloud computing,
   Spring 2019. Bloomington, Indiana: Indiana University, 2019
   [Online]. Available: <https://laszewski.github.io/book/linux/>,
   Please note a new version is under development.
8. G. von Laszewski (Editor), Scientific writing with markdown,
   Spring 2019. Bloomington, Indiana: Indiana University, 2019
   [Online]. Available: <https://laszewski.github.io/book/writing/>,
   Please note a new version is under development.
9. G. von Laszewski, Bookmanager,
   <https://pypi.org/project/cyberaide-bookmanager/>
10. G. von Laszewski, <https://github.com/cloudmesh-community>
11. G. von Laszewski, <https://github.com/cloudmesh>
