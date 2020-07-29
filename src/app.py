from flask import request, redirect, render_template, url_for
from models import app, User, Video, db, Section
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
    videos = Video.query.all()    

    return render_template('home.html', videos=videos) 
    

@app.route('/admin/', methods=['GET', 'POST'])
def admin():
    abo_adel = User.query.filter_by(email='mohamed09@gmail.com').first()
    form = Log_in_form()

    if request.method == "POST" and form.validate_on_submit():
        password = form.password.data
        if form.email.data == abo_adel.email and check_password_hash(abo_adel.password, password):
            login_user(abo_adel)
            return redirect(url_for('admin_bag'))
        

    return render_template('admin_login.html', form=form)


@login_required
@app.route('/admin/home/')
def admin_bag():
    sections = Section.query.order_by(Section.added_at).all()

    return render_template('admin_bag.html', sections=sections)




@login_required
@app.route('/admin/sections/add/', methods=['GET', 'POST'])
def add_section():

    if request.method == "POST":
        title = request.form['title']
        description = request.form['description']
        new_section = Section(title=title, description=description)
        db.session.add(new_section)
        db.session.commit()
        return redirect(url_for('admin_bag'))
    
    return render_template('add_section.html')


@login_required
@app.route('/admin/sections/<int:section_id>/videos/')
def section_bag(section_id):
    videos = Video.query.filter_by(section_id=section_id).order_by(Video.added_at).all()
    for video in videos:
        print(video.title)
    section = Section.query.filter_by(id=section_id).first()

    return render_template('section_bag.html', videos=videos, section=section)



@login_required
@app.route('/admin/sections/<int:section_id>/edit/', methods=['GET', 'POST'])
def edit_section(section_id):
    section = Section.query.filter_by(id=section_id).first()

    if request.method == "POST":
        title = request.form['title']
        description = request.form['description']
        
        section.title = title
        section.description = description
        db.session.commit()

        return redirect(url_for('admin_bag'))

    return render_template('edit_section.html', section=section)


@login_required
@app.route('/admin/section/<int:section_id>/delete/', methods=['GET', 'POST'])
def delete_section(section_id):
    section = Section.query.filter_by(id=section_id).first()

    if request.method == "POST":
        db.session.delete(section)
        db.session.commit()

        return redirect(url_for('admin_bag'))

    return render_template('delete_section.html', section=section)


@login_required
@app.route('/admin/sections/<int:section_id>/videos/add/', methods=['GET', 'POST'])
def add_video(section_id):
    section = Section.query.filter_by(id=section_id).first()

    if request.method == "POST":
        title = request.form['title']
        i_frame = request.form['i_frame']
        new_video = Video(title=title, i_frame=i_frame, section_id=section_id)
        db.session.add(new_video)
        db.session.commit()
        return redirect(url_for('section_bag', section_id=section_id))
    
    return render_template('add_video.html', section=section)


@login_required
@app.route('/admin/sections/<int:section_id>/videos/<int:video_id>/edit/', methods=['GET', 'POST'])
def edit_video(section_id, video_id):
    section = Section.query.filter_by(id=section_id).first()
    video = Video.query.filter_by(id=video_id).first()

    if request.method == "POST":
        title = request.form['title']
        i_frame = request.form['i_frame']
        video.title = title
        video.i_frame = i_frame
        db.session.commit()
        return redirect(url_for('section_bag', section_id=section_id))
    
    return render_template('edit_video.html', section=section, video=video)


@login_required
@app.route('/admin/sections/<int:section_id>/videos/<int:video_id>/delete/', methods=['GET', 'POST'])
def delete_video(section_id, video_id):
    section = Section.query.filter_by(id=section_id).first()
    video = Video.query.filter_by(id=video_id).first()
    if request.method == "POST":
        db.session.delete(video)
        db.session.commit()

        return redirect(url_for('section_bag', section_id=section_id))

    return render_template('delete_video.html', section=section, video=video)

if __name__ == "__main__":
    app.run(debug=True)
