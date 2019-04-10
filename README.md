
# Cloudmehs Installer 

This is an experimental installer that is most usefull during the development of
cloudmesh components form source. Once cloudmehs is released, you can use the
packages hosted at pypi.

This command can be installed with 

```bash
$ pip install cloudmesh-installer
```

## Usage
```
cloudmesh-installer -- a helper to install cloudmesh from source for developers.

Usage:
  cloudmesh-installer git key [LOCATION]
  cloudmesh-installer git [clone|pull|status] [BUNDLE]
  cloudmesh-installer install [BUNDLE] [-e]
  cloudmesh-installer list
  cloudmesh-installer info
  cloudmesh-installer local purge DIR [--force]
  cloudmesh-installer pyenv purge ENV [--force]

A convenient program called `cloudmesh-installer` to ownload and install cloudmesh
from sources published in github.

Arguments:
  BUNDLE      the bundle [default: cms]
  REPOS       list of git repos
  ENV         the name of the pyenv
  DIR         the directory form where to start the search

Options:
  -h --help
  --force   test

Description:

    cloudmesh-installer list

        Bundles

        Cloudmesh has a number of bundels. Bundels are simple a number of git
        repositories. You can list the bundels with the list command. and see
        their names in the top level.

    cloudmesh-installer info

        The info command gives some very basic information about the version
        numbers of cloudmesh on your system, github, and pypi. THis helps
        identifying if you may run an odlder version.

        In addition we try to check if you do use pyenv

    cloudmesh-installer git key [LOCATION]

        This command only works if you use ssh keys to authenticate with github.
        This command makes uploading the key easy as it checks for your key and
        provides via the web browser automatic pageloads to github for the
        keyupload. YOu do not have tou use this command. It is intenden for
        novice users.

    cloudmesh-installer git [clone|pull|status] [BUNDLE]

        This command executes the given git command on the bundle

    cloudmesh-installer install [BUNDLE]

        This command executes an install on the given bundle

    cloudmesh-installer info

        This command is very useful to list the version of the installed
        package, the version n git, and the version on pypi

    cloudmesh-installer local purge [DIR] [--force]

        THIS IS A DANGEROUS COMMAND AND YOU SHOULD PROBABLY NOT USE IT


        This command should not be used in general. It is for the most
        experienced user and allows to identify eggs in your directory
        recursively. The --force option allows to delete the egg, but it may be a
        better strategy to just list the egs without the --force and than delete the
        files you do not want.

        One test that you may want to do is to just call the command without the
        force option as to see possible eggs that you forgot and may need to be
        deleted.

    cloudmesh-installer pyenv purge ENV [--force]

        THIS IS A DANGEROUS COMMAND AND YOU SHOULD PROBABLY NOT USE IT

        THis command removes the specified virtual envireonment and reinstalls
        it with python 3.7.2. It will erase it entirely, thus make sure you know
        what this command does. YOu will have to reinstall all packages.

    Example:

        let us assume you like to work on storage, than you need to do the following

            mkdir cm
            cd cm
            cloudmesh-installer git clone storage
            cloudmesh-installer install storage -e
            cloudmesh-installer info
```
