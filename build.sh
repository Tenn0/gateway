rm -r ./dist
pip3 uninstall -y TheengsGateway
python3 setup.py sdist
cd dist
pip3 install TheengsGateway-0.1.4.tar.gz --no-deps