VERSION=1.5.0

install i:
	virtualenv -p python3.9 env
	. env/bin/activate
	timeout 1
	pip install -r requirements.txt
	. env/bin/deactivate

build b:
	docker build . -t brianwolf94/jaime-agent:$(VERSION) -f Dockerfile
	docker build . -t brianwolf94/jaime-agent-kubernetes:$(VERSION) -f Dockerfile.kubernetes
	docker build . -t brianwolf94/jaime-agent-openshift:$(VERSION) -f Dockerfile.openshift

compile c:
	python -m compile -b -f -o dist/ .
	rm -fr dist/repo_modules_default dist/env/
	cp -rf variables.env dist/
