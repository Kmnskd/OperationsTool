# !/bin/python3

from flask import Flask, render_template
from flask_mail import Mail, Message
import os
from configs import BaseConfig
# from views.upload import upload
# from views.version_rollout import rollout
# from views.auth import auth
# from views.feature import feature
# from views.ldap_manage import ldap_manage
from views import init_view
# from init_handler import init_plugs
from init_handler import init_mail


def create_app():
    app = Flask(__name__)
    app.config.from_object(BaseConfig)
    # init_plugs(app)

    init_mail(app)
    init_view(app)
    # app.register_blueprint(upload, url_prefix='/upload')
    # app.register_blueprint(rollout, url_prefix='/rollout')
    # app.register_blueprint(auth, url_prefix='/auth')
    # app.register_blueprint(feature, url_prefix='/feature')
    # app.register_blueprint(ldap_manage, url_prefix='/ldap_manage')

    @app.route("/")
    def index():
        return render_template("index.html")

    return app


app = create_app()


if __name__ == '__main__':
    app.run(debug=True)
