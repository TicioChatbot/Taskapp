from flask import Blueprint, render_template, request, redirect, url_for 
from .models import *
from .utils import * 
from datetime import datetime
import os 

view_blueprint =Blueprint('views', __name__)
color = os.environ.get('color', default='#910A0A')

@view_blueprint.context_processor
def inject_globals():
    return make_variables(color)

@view_blueprint.get('/')
def get_home(): 
    users = User.query.all()
    tasks = Task.query.all()
    activas = len([task for task in tasks if task.complete == False])
    projects = Project.query.all()
    return render_template('home.html', users = users, tasks = tasks, projects = projects, activas = activas)

@view_blueprint.get('/create_user')
def get_create_user():
    users = User.query.all()
    tasks = Task.query.all()
    projects = Project.query.all()
    return render_template('create_user.html', users = users, tasks = tasks, projects = projects)


@view_blueprint.post('/create_user')
def post_create_user():
    user = request.form['username']
    create_user(user)
    return redirect(url_for('views.get_home'))

@view_blueprint.post('/edit_user')
def post_edit_user():
    user_id = request.form['user']
    username = request.form['username']
    edit_user(user_id, username)
    return redirect(url_for('views.get_home'))

@view_blueprint.post('/simple_delete_user')
def post_simple_delete_user():
    user_id = request.form['user']
    simple_delete(user_id)
    return redirect(url_for('views.get_home'))

@view_blueprint.post('/migrate_delete_user')
def post_migrate_delete_user():
    user_id = request.form['user']
    migrate_id = request.form['migrate']
    if user_id == migrate_id:
        return redirect(url_for('views.get_home'))
    else:
        migrate_delete(user_id, migrate_id)
        return redirect(url_for('views.get_home'))

@view_blueprint.post('/create_task')
def post_create_task():
    try:
        content = request.form['content']
        duedate = datetime.strptime(request.form['duedate'], date_format)
        project = int(request.form['project'])
        task_id = create_task(content, duedate, project)
        user_id = int(request.form['user'])
        assign_task(user_id, task_id)
        return redirect(find_redirect(request.form['type'], request.form['id']))
    except:
        return redirect(find_redirect(request.form['type'], request.form['id']))

@view_blueprint.post('/assign_task')
def post_assign_task():
    user_id = request.form['user']
    task_id = request.form['task']
    assign_task(user_id, task_id)
    return redirect(find_redirect(request.form['type'], request.form['id']))

@view_blueprint.post('/unassign')
def post_unassign():
    user_id = request.form['user']
    task_id = request.form['task']
    unassign(user_id, task_id)
    return redirect(find_redirect(request.form['type'], request.form['id']))

@view_blueprint.post('/change_duedate')
def post_change_duedate():
    task_id = request.form['task']
    duedate = request.form['duedate']
    change_duedate(task_id, duedate)
    return redirect(find_redirect(request.form['type'], request.form['id']))

@view_blueprint.post('/delete_task')
def post_delete_task():
    task_id = request.form['task']
    delete_task(task_id)
    return redirect(find_redirect(request.form['type'], request.form['id']))

@view_blueprint.post('/edit_task')
def post_edit_task():
    task_id = request.form['task']
    content = request.form['content']
    change_content(task_id, content)
    return redirect(find_redirect(request.form['type'], request.form['id']))

@view_blueprint.get('/user/<int:user_id>')
def user_dashboard(user_id):
    users = User.query.all()
    tasks = Task.query.all()
    for task in tasks: 
        task.is_overdue()
    db.session.commit()
    projects = Project.query.all()
    user = User.query.filter_by(id=user_id).first()
    return render_template('user.html', user = user, users = users, task=tasks, projects=projects)

@view_blueprint.post('/user/<int:user_id>')
def post_user_dashboard(user_id):
    task_id = request.form['id']
    task = Task.query.filter_by(id=int(task_id)).first()
    task.complete = True 
    db.session.commit()
    return redirect(url_for('views.user_dashboard', user_id=user_id))

@view_blueprint.get('/project/<int:project_id>')
def project_dashboard(project_id):
    users = User.query.all()
    tasks = Task.query.all()
    for task in tasks: 
        task.is_overdue()
    db.session.commit()
    projects = Project.query.all()
    project = Project.query.filter_by(id=project_id).first()
    return render_template('project.html', project = project, users = users, task=tasks, projects=projects, len = len)

@view_blueprint.post('/project/<int:project_id>')
def post_project_dashboard(project_id):
    task_id = request.form['id']
    task = Task.query.filter_by(id=int(task_id)).first()
    task.complete = True 
    db.session.commit()
    return redirect(url_for('views.project_dashboard', project_id=project_id))

@view_blueprint.post('/create_project')
def post_create_project():
    project = request.form['name']
    create_project(project)
    return redirect(url_for('views.get_home'))

@view_blueprint.get('/create_project')
def get_create_project():
    users = User.query.all()
    tasks = Task.query.all()
    projects = Project.query.all()
    return render_template('create_project.html', users = users, tasks = tasks, projects = projects)