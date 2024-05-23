from .models import *
import os


def create_user(username):
    user = User(username = username)
    db.session.add(user)
    db.session.commit()
    return 'Success!' 
    
def create_task(content, duedate, project_id):
    task = Task(content=content, duedate=duedate, project_id = project_id)
    db.session.add(task)
    db.session.commit()
    return task.id 

def assign_task(user_id, task_id): 
    user = User.query.filter_by(id=user_id).first()
    task = Task.query.filter_by(id=task_id).first()
    task.assigned.append(user)
    db.session.commit()
    return 'Success!' 

def create_project(name):
    project = Project(name=name)
    db.session.add(project)
    db.session.commit()
    return 'Success!'


def on_time(user): 
    terminadas = [task for task in user.backref if task.complete == True]
    on_time = [task for task in terminadas if task.overdue == False]
    if len(terminadas) > 0: 
        return f'{len(on_time)/len(terminadas) * 100} % {len(on_time)}/{len(terminadas)}'
    else: 
        return '0% 0/0'
    
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


def make_variabes(color): 
    return {
        'color': color,
        'border': adjust_hex_brightness(color, 0.8), 
        'hover': adjust_hex_brightness(color, 1.2)
    }
