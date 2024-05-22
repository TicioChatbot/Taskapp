import click
from flask import Blueprint
from .models import *
from .utils import *


cli_blueprint =Blueprint('cli', __name__)

@cli_blueprint.cli.command('create_user')
@click.argument('username')
def cli_create_user(username):
    print(create_user(username))

@cli_blueprint.cli.command('create_task')
@click.argument('task')
def cli_create_user(task):
    print(create_task(task))

@cli_blueprint.cli.command('create_project')
@click.argument('project')
def cli_create_user(project):
    print(create_project(project))
