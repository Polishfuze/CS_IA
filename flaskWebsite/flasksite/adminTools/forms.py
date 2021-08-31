from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField, StringField

class AddPermsForm(FlaskForm):
    teacherName = SelectField("Person to edit: ", choices=[])
    roleToAdd = SelectField("Role to add: ", choices=[])
    submit = SubmitField('Add roles!')

class RemovePermsForm(FlaskForm):
    teacherName = SelectField("Person to edit: ", choices=[])
    roleToAdd = SelectField("Role to add: ", choices=[])
    submit = SubmitField('Remove roles!')