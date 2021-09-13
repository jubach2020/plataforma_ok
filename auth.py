from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import current_user, login_user, logout_user, login_required, login_manager
from models import Usuario
from flask import Blueprint, Flask, url_for, redirect, render_template, request, flash
from forms import LoginForm, RegistrationForm, SolicitarPasswordForm, RecuperarPassForm
from app import db
#import MySQLdb.cursors

from models import Departamento
auth = Blueprint('auth', __name__)


@auth.route('/administrador')
@login_required
def administrador():
    return render_template('index.html')

@auth.route('/operaciones')
@login_required
def operaciones():
    return render_template('index.html')

'''
@login_manager.unauthorized_handler     
def unauthorized_callback():            
       return redirect(url_for('login'))
'''

@auth.route('/', methods=['GET', 'POST'])
def index():
    if current_user.is_authenticated:
        return redirect(url_for('auth.administrador'))
    form = LoginForm()
    if request.method == 'POST':
        #if form.validate_on_submit():
        user = Usuario.query.filter_by(nombreUsuario=form.username.data).first()
        print(form.username.data)
        if user is None or not user.checkPassword(form.password.data):
            flash('Usuario o contraseña incorrectos', 'danger')
            return redirect(url_for('auth.login',form=form))
        login_user(user, remember=form.remember_me.data)
        if user.is_admin():
            #return render_template('index.html')
            return redirect(url_for('auth.administrador'))
        return redirect(url_for('auth.operaciones'))
        #return render_template('index.html')
    return render_template('login.html',  form=form , title='Login')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('auth.administrador'))
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = Usuario.get_by_username(form.username.data)
       
        if user is None or not user.checkPassword(form.password.data):
            flash('Usuario o contraseña incorrectos', 'danger')
            return redirect(url_for('auth.login',form=form))
        login_user(user, remember=form.remember_me.data)
        if user.is_admin():
            return redirect(url_for('auth.administrador'))
        return redirect(url_for('auth.operaciones'))
    return render_template('login.html',  form=form , title='Login')
  

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/registro', methods=['GET', 'POST'])
def registro():
   
    if current_user.is_authenticated:
        return redirect(url_for('auth.index'))
    form = RegistrationForm()
 
    if request.method == 'POST':     
        print(request.form['empDpto'])
        userMail = Usuario.existe_email(form.email.data)         
        if userMail:
            flash('El email ya existe', 'danger')
        else: 
           userNom = Usuario.existe_username(form.username.data)
           if userNom:
            flash('El nombre de usuario ya existe', 'danger')
           else:
                if request.form['empDpto']==0:
                    flash('Seleccione un departamento', 'danger')
                else:
                    user = Usuario(nomUsuario=form.username.data, nombre=form.name.data, email=form.email.data, password=generate_password_hash(form.password.data), idRol=0, idDpto=request.form['empDpto'])
                    user.save()
                    flash('Enhorabuena, ya está registrado como usuario!', 'success')
                    return redirect(url_for('auth.login'))       
    departamentos = Departamento.get_all()
    return render_template("registro.html",form=form ,departamentos=departamentos)       


@auth.route('/olvido-password', methods=['GET', 'POST'])
def solicitarPassword():
    form = SolicitarPasswordForm()
    if request.method == 'POST':
        try:
            user = Usuario.get_by_email(form.email.data)
        except:
            flash('Email incorrecto', 'danger')
            return render_template('olvido-password.html", form=form', form=form)
    return render_template('olvido-password.html', form=form)

'''
def solicitarPasswordtmp():
    if user.email_confirmed:
        send_password_reset_email(user.email)
        flash('En su correo electónico obtendrá un correo con un enlace para restablecer el password.', 'success')
    else:
        flash('Debe confirmar su dirección de correo electrónico antes de intentar restablecer su password.', 'warning')
        return redirect(url_for('users.login'))    
    return render_template('olvido-password.html', form=form)
'''

def enviarEmailResetPass():
    if request.method == 'POST':
        user_email = request.form['empMail'] 
        password_reset_serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])     
        password_reset_url = url_for('users.reset_with_token', token = password_reset_serializer.dumps(user_email, salt='password-reset-salt'),
                                _external=True)
        html = render_template('email_password_reset.html',password_reset_url=password_reset_url)
        send_email('Solicitud de restablecimiento de password', [user_email], html)
        password_reset_serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])     
        password_reset_url = url_for('users.reset_with_token', token = password_reset_serializer.dumps(user_email, salt='password-reset-salt'),
                                _external=True)
        html = render_template('email_password_reset.html',password_reset_url=password_reset_url)
        send_email('Solicitud de restablecimiento de password', [user_email], html)
        return 'ok'
    return render_template("olvido-password.html", form=form)


#solo puede cambiarla desde el link que se envía que estará relacionado con el email y por lo tanto el usuario
@auth.route('/recuperar-password', methods=['GET', 'POST'])
def recuperarPasssword():
    form = RecuperarPassForm()
    if request.method == 'POST':
        pass1 = request.form['pass1'] 
        pass2 = request.form['pass2'] 
        #enviar mail para recuperar password
    return render_template("recuperar-password.html", form=form)

@auth.route('/home')
def home():
    return render_template("index.html", titulo="HOME")

@auth.route('/terminos-y-condiciones', methods=['GET', 'POST'])
def terminosYcondiciones():
    return render_template("condiciones.html")   


