from flask import request, redirect, render_template, url_for
from models import app, User, Video, db
from werkzeug.security import generate_password_hash, check_password_hash
from forms import Log_in_form
from flask_login import login_required, login_manager, login_user, logout_user, LoginManager

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route('/')
def home():
    
    video = '<iframe width="560" height="315" src="https://www.youtube.com/embed/U8VM9G2D7i0" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>'
    
    return render_template('home.html', video=video) 

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    abo_adel = User.query.filter_by(email='mohamed@gmail.com').first()
    form = Log_in_form()

    if request.method == "POST" and form.validate_on_submit():
        print("good")
        password = form.password.data
        if form.email.data == abo_adel.email and check_password_hash(abo_adel.password, password):
            login_user(abo_adel)
            return "done login"
        

    return render_template('admin_login.html', form=form)



if __name__ == "__main__":
    app.run(debug=True)
