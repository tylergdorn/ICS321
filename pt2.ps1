./venv/Scripts/activate
$env:FLASK_APP = "main.py"
flask initdb
flask run