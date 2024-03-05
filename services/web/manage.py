from flask.cli import FlaskGroup

from project import app, db
from project.models.task import Task

cli = FlaskGroup(app)

# Command line methods useful during dev
@cli.command('create_db')
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()

@cli.command('seed_db')
def seed_db():
    db.session.add(Task(text='買晚餐'))
    db.session.commit()

if __name__ == '__main__':
    cli()