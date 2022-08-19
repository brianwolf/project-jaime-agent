VERSION=1.6.2

install i:
	virtualenv -p python3.9 env
	. env/bin/activate
	timeout 1
	pip install -r requirements.txt
	. env/bin/deactivate

build b:
	podman build . -t brianwolf94/jaime-agent:$(VERSION) -f Dockerfile
	podman build . -t brianwolf94/jaime-agent-kubernetes:$(VERSION) -f Dockerfile.kubernetes
	podman build . -t brianwolf94/jaime-agent-openshift:$(VERSION) -f Dockerfile.openshift
	podman build . -t brianwolf94/jaime-agent-pushgateway:$(VERSION) -f Dockerfile.pushgateway

compile c:
	python -m compile -b -f -o dist/ .
	rm -fr dist/repo_modules_default dist/env/
	cp -rf variables.env dist/
