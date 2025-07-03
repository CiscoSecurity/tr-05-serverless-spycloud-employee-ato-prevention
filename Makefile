NAME:="tr-05-spycloud-employee-ato-prevention"
PORT:="9090"
PM_PATH:="code/tests/functional/postman_collection.json"

all: stop build test test_pm scout

run: # app locally
	cd code; python -m main; cd -

# Docker
build: stop_name
	docker build -q -t $(NAME) .;
	docker run -dp $(PORT):$(PORT) --name $(NAME) $(NAME)
stop:
	docker stop $(shell docker ps | tail -1 | grep :9090 | awk '{ print $$1 }')
stop_name:
	docker stop $(NAME); docker rm $(NAME); true

# Tools
env:
	pip3 install --no-cache-dir --upgrade pipenv && pipenv install --dev && pipenv shell
	brew install newman
black:
	black code/ -l 120 -t py311 --exclude=payloads_for_tests.py
lint: black
	flake8 code/

# Tests
test:
	cd code; coverage run --source api/ -m pytest --verbose tests/unit/ && coverage report --fail-under=80; cd -
test_lf:
	cd code; coverage run --source api/ -m pytest --verbose -vv --lf tests/unit/ && coverage report -m --fail-under=80; cd -
test_pm:
	newman run $(PM_PATH)
scout:
	curl -sSfL https://raw.githubusercontent.com/docker/scout-cli/main/install.sh | sh -s --
	docker scout cves $(NAME) --only-fixed
	pip-audit

# ---------------------------------------------------------------- #
# If ngrok can be used by you then you can run below make commands #
# ---------------------------------------------------------------- #
up: down build expose
down: unexpose stop_name

expose:
	ngrok http $(PORT) > /dev/null &
echo_ngrok:
	curl -s localhost:4040/api/tunnels | jq -r ".tunnels[0].public_url"
unexpose:
	pkill ngrok; true
