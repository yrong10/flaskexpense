from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField
from wtforms.validators import Email, EqualTo, InputRequired, Length, ValidationError

from flaskexpense.models import User


class RegistrationForm(FlaskForm):
    username = StringField(
        "Username",
        [InputRequired(message="Please enter username"), Length(min=2, max=20)],
    )
    email = StringField("Email", [InputRequired(message="Please enter email"), Email()])
    password = PasswordField(
        "Password", [InputRequired(message="Please enter password")]
    )
    confirm_password = PasswordField(
        "Confirm Password",
        [
            InputRequired(message="Please confirm password"),
            EqualTo("password", message="Passwords must match"),
        ],
    )
    submit = SubmitField("Sign Up")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("Email already exists")


class LoginForm(FlaskForm):
    email = StringField("Email", [InputRequired(message="Please enter email"), Email()])
    password = PasswordField(
        "Password", [InputRequired(message="Please enter password")]
    )
    remember = BooleanField("Remember Me")
    submit = SubmitField("Sign In")


def valdate_category(self, field):
    if field.data == "":
        raise ValidationError("Please select category")
