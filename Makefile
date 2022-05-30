create-venv:
	# Setup Virtual Environment
	python3 -m pip install --upgrade pip
	pip3 install virtualenv

	test -d sensor-fusion-venv || virtualenv sensor-fusion-venv

	# Certificates for Access to Apple pypi
	. sensor-fusion-venv/bin/activate; python3 -m pip install --upgrade pip; pip3 install apple-certifi --index https://pypi.apple.com/simple

install-requirements:
	. sensor-fusion-venv/bin/activate; pip install -r requirements.txt