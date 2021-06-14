.PHONY: container-image publish-container-image

CONTAINER_IMAGE_NAME=kfp-ex-component-1
QUAY_ORG=ptitzler

container-image:
	docker build -t $(CONTAINER_IMAGE_NAME) .

publish-container-image: container-image
	docker tag $(CONTAINER_IMAGE_NAME) quay.io/$(QUAY_ORG)/$(CONTAINER_IMAGE_NAME)
	docker push quay.io/$(QUAY_ORG)/$(CONTAINER_IMAGE_NAME)
