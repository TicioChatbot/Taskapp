from .models import *

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
    
def test(): 
    users = User.query.all()
    for user in users: 
        print(on_time(user))