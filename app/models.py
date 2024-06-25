from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from datetime import date 
from math import floor

db = SQLAlchemy()

user_task = db.Table('User_Task',
                        db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                        db.Column('task_id', db.Integer, db.ForeignKey('task.id'))
                        )

class User(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(500))

    def __repr__(self):
        return self.username
    
    def carga_laboral_pctg(self, activas):
        if activas > 0:
            propias = len([task for task in self.backref if task.complete == False])
            return f'{floor(propias/activas * 100)} %'
        else: 
            return '0%'
        
    def on_time_pctg(self): 
        terminadas = [task for task in self.backref if task.complete == True]
        on_time = [task for task in terminadas if task.overdue == False]
        if len(terminadas) > 0: 
            return f'{floor(len(on_time)/len(terminadas)* 100)} %'
        else: 
            return '0%'
    
    def carga_laboral_total(self, activas):
        if activas > 0:
            propias = len([task for task in self.backref if task.complete == False])
            return f'{propias}/{activas}'
        else:
            return '0/0' 

    def on_time_total(self): 
        terminadas = [task for task in self.backref if task.complete == True]
        on_time = [task for task in terminadas if task.overdue == False]
        if len(terminadas) > 0: 
            return f'{len(on_time)}/{len(terminadas)}'
        else: 
            return '0/0'

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(500))
    assigned = db.relationship('User', secondary= user_task, backref='backref')
    duedate = db.Column(db.Date())
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    complete = db.Column(db.Boolean, default=False)
    overdue = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return self.content

    def __lt__(self, other): 
        return self.duedate < other.duedate

    def find_project(self):
        project = Project.query.filter_by(id=self.project_id).first()
        if project:
            return project.name
        else:
            return 'deleted project'

    def is_overdue(self):
        if not self.complete: 
            dif = self.duedate - date.today()
            if dif.days < 0: 
                self.overdue = True
            else: 
                self.overdue = False


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(500))
    tasks = db.relationship('Task', backref='project')

    def __repr__(self):
        return self.name


