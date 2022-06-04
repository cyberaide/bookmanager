package=cyberaide-bookmanager
VERSION=$(shell head -1 VERSION)
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

######################################################################
# PYPI
######################################################################


twine:
	pip install -U twine

dist:
	python setup.py sdist bdist_wheel
	twine check dist/*

requirements_dev:
	pip install -r  requirements-dev.txt

patch: clean requirements_dev
	@echo "############################################################"
	@echo "# BUILD "
	@echo "############################################################"
	bump2version --no-tag patch
	python setup.py sdist
	python setup.py bdist_wheel
	git push
	# git push origin master --tags
	twine check dist/*
	twine upload --repository testpypi  dist/*
	# $(call banner, "install")
	# sleep 10
	# pip install --index-url https://test.pypi.org/simple/ cloudmesh-$(package) -U

minor: clean
	@echo "############################################################"
	@echo "# MINOR "
	@echo "############################################################"
	bump2version minor --allow-dirty
	@cat VERSION
	@echo

release: clean
	@echo "############################################################"
	@echo "# CLEAN "
	@echo "############################################################"
	git tag "v$(VERSION)"
	git push origin master --tags
	python setup.py sdist bdist_wheel
	twine check dist/*
	twine upload --repository pypi dist/*
	$(call banner, "install")
	@cat VERSION
	@echo
	# sleep 10
	# pip install -U cyberaide-common
	make -f Makefile image
	make -f Makefile push

dev:
	bump2version --new-version "$(VERSION)-dev0" part --allow-dirty
	bump2version patch --allow-dirty
	@cat VERSION
	@echo

reset:
	bump2version --new-version "4.0.0-dev0" part --allow-dirty

upload:
	twine check dist/*
	twine upload dist/*

pip:
	pip install --index-url https://test.pypi.org/simple/ cyberaide-$(package) -U

#	    --extra-index-url https://test.pypi.org/simple

log:
	@echo "############################################################"
	@echo "# LOG "
	@echo "############################################################"
	gitchangelog | fgrep -v ":dev:" | fgrep -v ":new:" > ChangeLog
	git commit -m "chg: dev: Update ChangeLog" ChangeLog
	git push

######################################################################
# DOCKER
######################################################################

#--no-cache=true

image:
	docker build  -t cloudmesh/bookmanager:${VERSION} -t cloudmesh/bookmanager:latest .

#
# cm mounts all ./* directories into the container
#
shell:
	docker run -v $(CM):/cm -w /cm --rm -it cloudmesh/bookmanager:${VERSION}  /bin/bash

winshell:
	winpty docker run -v $(CM):/cm -w /cm --rm -it cloudmesh/bookmanager:${VERSION}  /bin/bash

cms:
	docker run --rm -it cloudmesh/bookmanager:${VERSION}

dockerclean:
	-docker kill $$(docker ps -q) --force
	-docker rm $$(docker ps -a -q) --force
	-docker rmi $$(docker images -q) --force

push:
	docker push cloudmesh/bookmanager:${VERSION}
	docker push cloudmesh/bookmanager:latest

run:
	docker run cloudmesh/bookmanager:${VERSION} /bin/sh -c "cd books/book/cloud; git pull; make"
