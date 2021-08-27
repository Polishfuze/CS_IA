from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, ValidationError
from flasksite.databases.databaseMgmt import checkIfStudentExists

class AddStudentForm(FlaskForm):
    studentName = StringField('StudentName', validators=[DataRequired(), Length(min=2, max=128)])
    teacherName = SelectField('TeacherName', choices=[])
    submit = SubmitField('Sign in')

    def validate_studentName(self, studentName):
        if checkIfStudentExists(studentName):
            raise ValidationError('This student already exists!')