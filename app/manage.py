from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
import os
from project import app, db

app.config.from_object("config.DevelopmentConfig") # app's config settings
migrate = Migrate(app, db) # migration instance 
manager = Manager(app) # manager instance

manager.add_command("db", MigrateCommand) # add db command to the manager so that we can run migrations from terminal

if __name__ == "__main__":
    manager.run()