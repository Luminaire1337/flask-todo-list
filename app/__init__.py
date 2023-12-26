from flask import Flask
import os

app = Flask(__name__, template_folder="views")
app.config["SECRET_KEY"] = os.environ.get("APP_KEY") != None and os.environ.get("APP_KEY") or os.urandom(24).hex()

from app.utils import time_ago
@app.context_processor
def utility_processor():
    return dict(time_ago=time_ago)

from app.controllers import index_blueprint, todo_blueprint
app.register_blueprint(index_blueprint)
app.register_blueprint(todo_blueprint)