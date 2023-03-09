from views.upload import upload
from views.version_rollout import rollout
from views.auth import auth
from views.feature import feature
from views.ldap_manage import ldap_manage


def init_view(app):
    app.register_blueprint(upload, url_prefix='/upload')
    app.register_blueprint(rollout, url_prefix='/rollout')
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(feature, url_prefix='/feature')
    app.register_blueprint(ldap_manage, url_prefix='/ldap_manage')