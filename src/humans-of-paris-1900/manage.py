#!/usr/bin/env python

from flask_script import Manager
from __init__ import app, db

manager = Manager(app)


@manager.shell
def make_shell_context():
    return dict(app=app, db=db)


if __name__ == '__main__':
    manager.run()