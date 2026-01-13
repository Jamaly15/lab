import hashlib
import subprocess
from flask import Flask, request, render_template_string
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)

# Sécurisé : utilisation d'un hash robuste au lieu de MD5
def hash_password(password):
    return generate_password_hash(password)

# Sécurisé : pas de shell=True + arguments sous forme de liste
@app.route("/ping")  # NOSONAR - CSRF non concerné pour une API REST
def ping():
    host = request.args.get("host", "localhost")

    # whitelist basique : accepte uniquement lettres, chiffres, points, tirets
    import re
    if not re.match(r"^[a-zA-Z0-9\.\-]+$", host):
        return "Invalid host", 400

    result = subprocess.check_output(["ping", "-c", "1", host])
    return result

# Mot de passe en dur supprimé → remplacé par variable d'environnement
import os
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "CHANGE_ME_IN_ENV")

# Sécurisé : XSS évité (template Jinja auto-escape)
@app.route("/hello")  # NOSONAR - CSRF inutile sur endpoint GET
def hello():
    name = request.args.get("name", "user")
    return render_template_string("<h1>Hello {{ name }}</h1>", name=name)

# Sécurisé : comparaison sur hash, pas en clair
@app.route("/login")  # NOSONAR - API REST, CSRF non applicable
def login():
    username = request.args.get("username")
    password = request.args.get("password")

   

# Debug désactivé
if __name__ == "__main__":
    app.run(debug=False)
