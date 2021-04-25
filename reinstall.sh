pylint **/*.py --include-naming-hint=y "--variable-rgx=^[a-z][a-z0-9]*((_[a-z0-9]+)*)?$" "--argument-rgx=^[a-z][a-z0-9]*((_[a-z0-9]+)*)?$" --disable=C0103
rm dist -rf
python3 setup.py sdist bdist_wheel
cd dist
pip3 uninstall tactile_patterns -y
pip3 install --user *.whl
cd ..
python3 -m "nose"
cd generated_patterns
python3 generate.py
# twine upload dist/* # to upload to PyPi
