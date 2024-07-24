VERSION=0.4.0

install i:
	virtualenv -p python3.11 env
	. env/bin/activate
	timeout 1
	pip install -r requirements.txt
	. env/bin/deactivate


build b:
	docker build . -t ghcr.io/jaime-project/jaime-agent:$(VERSION) -f Dockerfile --build-arg ARG_VERSION=$(VERSION)
	docker build . -t ghcr.io/jaime-project/jaime-agent-cluster:$(VERSION) -f Dockerfile.cluster --build-arg ARG_VERSION=$(VERSION)
	docker build . -t ghcr.io/jaime-project/jaime-agent-pushgateway:$(VERSION) -f Dockerfile.pushgateway --build-arg ARG_VERSION=$(VERSION)


push p:
	docker push ghcr.io/jaime-project/jaime-agent:$(VERSION)
	docker push ghcr.io/jaime-project/jaime-agent-cluster:$(VERSION) 
	docker push ghcr.io/jaime-project/jaime-agent-pushgateway:$(VERSION) 


run r:
	docker run -it --rm -p 7001:7001 ghcr.io/jaime-project/jaime-agent:$(VERSION)


compile c:
	python -m compile -b -f -o dist/ .
	rm -fr dist/repo_modules_default dist/env/
	cp -rf variables.env dist/
