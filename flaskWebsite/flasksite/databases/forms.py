from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, ValidationError
from flasksite.databases.databaseMgmt import checkIfStudentExists

class AddStudentForm(FlaskForm):
    studentName = StringField("Student's Name", validators=[DataRequired(), Length(min=2, max=128)])
    teacherName = SelectField("Teacher's Name", choices=[])
    submit = SubmitField('Add student!')

    def validate_studentName(self, studentName):
        resp = checkIfStudentExists(studentName)
        print(resp)
        if resp:
            raise ValidationError('This student already exists!')