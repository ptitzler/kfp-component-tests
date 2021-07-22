.PHONY: lint clean

clean:
	rm -f count_lines_component.yaml

lint: clean
	pip install -r test-requirements.txt
	flake8 .