.PHONY: container-image publish-container-image lint

# Customize the variables as desired/required
CONTAINER_IMAGE_NAME=kfp-ex-component-0:v000
DH_ORH=
QUAY_ORG=ptitzler

lint:
	pip install -r test-requirements.txt
	flake8 .

container-image: lint
	docker build -t $(CONTAINER_IMAGE_NAME) .

publish-container-image: container-image
	docker tag $(CONTAINER_IMAGE_NAME) quay.io/$(QUAY_ORG)/$(CONTAINER_IMAGE_NAME)
	docker push quay.io/$(QUAY_ORG)/$(CONTAINER_IMAGE_NAME)
	# docker tag $(CONTAINER_IMAGE_NAME) docker.io/$(DH_ORG)/$(CONTAINER_IMAGE_NAME)
	# docker push docker.io/$(DH_ORG)/$(CONTAINER_IMAGE_NAME)
