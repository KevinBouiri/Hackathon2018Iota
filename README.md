python3 -m pip install virtualenv
python3 -m virtualenv venv
vens/scripts/activate
pip install pyota flake8 flask flask_restful flask-jsonpify
pip install pyota[ccurl]

Dann eine config.cfg datei anlegen und den Inhalt füllen .Beispiel:
[IOTA]
Seed = XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX