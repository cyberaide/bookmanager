package=cyberaide-bookmanager
VERSION=$(shell head -1 ../../VERSION)
CM=$(shell dirname `pwd`)

.PHONY: readme

#source:
#	cd ../cloudmesh.common; make source
#	$(call banner, "Install cloudmesh-cmd5")
#	pip install -e . -U
#	cms help

validate:
	gem install travis
	travis lint .travis.yml

clean:
	@echo "############################################################"
	@echo "# CLEAN "
	@echo "############################################################"
	rm -rf dist
	rm -rf *.zip
	rm -rf *.egg-info
	rm -rf *.eggs
	rm -rf docs/build
	rm -rf build
	find . | grep -E "(__pycache__|\.pyc|\.pyo$)" | xargs rm -rf
	rm -rf .tox
	rm -f *.whl

readme:
	bookmanager --help > README-helper/manual.md
	cat README-prefix.md \
	    README-helper/verbatim-start.md \
	    README-helper/manual.md \
	    README-helper/verbatim-stop.md \
	    README-postfix.md \
	    README-helper/verbatim-start.md \
	    tests/python.yml \
	    README-helper/verbatim-stop.md \
	    README-install-other.md > README.md
	git commit -am "Generating the README"
	git push

requirements_dev:
	pip install -r  requirements-dev.txt

######################################################################
# DOCKER
######################################################################

#--no-cache=true

image:
	docker build  -t cloudmesh/bookmanager:${VERSION} -t cloudmesh/bookmanager:latest .

#
# cm munts all parent directories into the container
#
cm:
	docker run -v $(CM):/cm -w /cm --rm -it cloudmesh/bookmanager:${VERSION}  /bin/bash

wincm:
	winpty docker run -v $(CM):/cm -w /cm --rm -it cloudmesh/bookmanager:${VERSION}  /bin/bash

shell:
	docker run --rm -it cloudmesh/bookmanager:${VERSION}  /bin/bash

cms:
	docker run --rm -it cloudmesh/bookmanager:${VERSION}

dockerclean:
	-docker kill $$(docker ps -q) --force
	-docker rm $$(docker ps -a -q) --force
	-docker rmi $$(docker images -q) --force

push:
	docker push cloudmesh/bookmanager:0.2.36
	docker push cloudmesh/bookmanager:latest

run:
	docker run cloudmesh/bookmanager:${VERSION} /bin/sh -c "cd books/book/cloud; git pull; make"
