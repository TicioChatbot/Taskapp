from .models import *
from flask import url_for
from datetime import datetime
import os


date_format = "%Y-%m-%d"

def create_user(username):
    user = User(username = username)
    db.session.add(user)
    db.session.commit()
    return 'Success!' 

def edit_user(user_id, username):
    user = User.query.filter_by(id=user_id).first()
    user.username = username
    db.session.commit()
    return 'Success!' 

def diagnose_delete(user_id):
    user = User.query.filter_by(id=user_id).first()
    danger_tasks = []
    for task in user.backref:
        if len(task.assigned) == 1: 
            danger_tasks.append(task)
    return danger_tasks

def create_task(content, duedate, project_id):
    task = Task(content=content, duedate=duedate, project_id = project_id)
    db.session.add(task)
    db.session.commit()
    return task.id 

def delete_task(task_id):
    task = Task.query.filter_by(id = int(task_id)).first()
    db.session.delete(task)
    db.session.commit()
    return 'Success!' 

def assign_task(user_id, task_id): 
    user = User.query.filter_by(id=user_id).first()
    task = Task.query.filter_by(id=task_id).first()
    task.assigned.append(user)
    db.session.commit()
    return 'Success!' 

def unassign(user_id, task_id): 
    user = User.query.filter_by(id=user_id).first()
    task = Task.query.filter_by(id=task_id).first() 
    task.assigned.remove(user)
    db.session.commit()
    return 'Success!'

def simple_delete(user_id):
    user = User.query.filter_by(id=user_id).first()
    db.session.delete(user)
    db.session.commit()
    return 'Success!' 

def migrate_delete(user_id, migrate_id):
    user = User.query.filter_by(id=user_id).first()
    migrate = User.query.filter_by(id= migrate_id).first()
    for task in user.backref:
        task.assigned.append(migrate)
    db.session.delete(user)
    db.session.commit()
    return 'Success!' 


def create_project(name):
    project = Project(name=name)
    db.session.add(project)
    db.session.commit()
    return 'Success!'

def delete_project(project_id): 
    project = Project.query.filter_by(id = project_id).first()
    for task in project.tasks:
        if task.complete == False: 
            delete_task(task.id)
    db.session.delete(project)
    db.session.commit()
    return 'Success!'

def kill_project(project_id): 
    project = Project.query.filter_by(id = project_id).first()
    for task in project.tasks: 
        delete_task(task.id)
    db.session.delete(project)
    db.session.commit()
    return 'Success!'
    

def change_duedate(task_id, duedate):
    task = Task.query.filter_by(id=task_id).first()
    task.duedate = datetime.strptime(duedate, date_format)
    db.session.commit()
    return 'Success!'

def change_content(task_id, content):
    task = Task.query.filter_by(id=task_id).first()
    task.content = content
    db.session.commit()
    return 'Success!'

def find_redirect(type, id): 
    if type == 'proyect':
        return url_for('views.project_dashboard', project_id= id)
    elif type =='user':
        return url_for('views.user_dashboard', user_id= id)
    else: 
        return url_for('views.get_home')

def on_time(user): 
    terminadas = [task for task in user.backref if task.complete == True]
    on_time = [task for task in terminadas if task.overdue == False]
    if len(terminadas) > 0: 
        return f'{len(on_time)/len(terminadas) * 100} % {len(on_time)}/{len(terminadas)}'
    else: 
        return '0% 0/0'
    
def create_note(content, task_id, user_id):
    note = Note(content = content, task_id = task_id, user_id = user_id)
    db.session.add(note)
    db.session.commit()
    return 'Success!'

def edit_note(note_id, content):
    note = Note.query.find_by(id=note_id).first()
    note.content = content
    db.session.commit()
    return 'Success!'

def delete_note(note_id):
    note = Note.query.filter_by(id=note_id).first()
    db.session.delete(note)
    db.session.commit()
    return 'Success!'

def adjust_component(comp, factor):
    adjusted_value = comp * factor
    clamped_value = max(0, min(255, int(adjusted_value)))
    return clamped_value

#0.8 darkens, 1.2 lightens
def adjust_hex_brightness(hex_color, factor):
    # Ensure hex_color starts with '#', and factor is a float
    if hex_color.startswith('#'):
        hex_color = hex_color[1:]
    # Split the hex_color into three components (r, g, b)
    r, g, b = (int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    # Adjust each component
    r, g, b = adjust_component(r, factor), adjust_component(g, factor), adjust_component(b, factor)
    # Format the adjusted components back into a hex string with leading '#'
    return f'#{r:02x}{g:02x}{b:02x}'


def make_variables(color): 
    return {
        'color': color,
        'border': adjust_hex_brightness(color, 0.8), 
        'hover': adjust_hex_brightness(color, 1.2),
        'active_color': adjust_hex_brightness(color, 0.6),  
        'active_border': adjust_hex_brightness(color, 0.5)  
    }