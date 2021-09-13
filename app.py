from flask import Flask
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap

import os

login_manager = LoginManager()
# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()
#migrate = Migrate()

def create_app(settings_module='config.development'):
    app = Flask(__name__)
    Bootstrap(app)

    app.config['SECRET_KEY'] = 'nvjdskgrshglrslgjrgkjweñlrkñwqkewqkedscsdvdsvdsvdsfvdsfvfdsvdfvfv'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Ubach@2020!@127.0.0.1:3306/Operaciones'
    app.config['SQLALCHEMY_POOL_SIZE']=20
    app.config['SQLALCHEMY_MAX_OVERFLOW']=0
    app.config['UPLOAD_FOLDER'] = '/static/assets/uploads'
    #app.config['USE_X_SENDFILE'] = True


    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True 
    db = SQLAlchemy(app)
  
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    mail = Mail(app)
    
    #db.init_app(app)
    #migrate.init_app(app, db) # Se inicializa el objeto migrate

    # blueprint for auth routes in our app
    from auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from models import Usuario
    @login_manager.user_loader
    def load_user(user_id):
	    return Usuario.get_by_userid(user_id)

    return app