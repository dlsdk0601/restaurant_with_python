from flask import Flask
from flask_cors import CORS

from ex.flask_ex import load_submodules, register_blueprints
from was import config, model
from was.blueprints import api

app = Flask(__name__)
app.config.from_object(config)

# DB 기능 초기화
model.db.init_app(app)
load_submodules(model)

api_url_prefix = '/api'
register_blueprints(app, (api, api_url_prefix))

# 개발중에만 활성화 해준다.
if app.debug:
    CORS(app, supports_credentials=True, resources=['*'])


@app.route('/')
def index():
    return "hello world"
