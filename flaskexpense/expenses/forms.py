from flask_wtf import FlaskForm
from wtforms import DateField, FloatField, SelectField, StringField, SubmitField
from wtforms.validators import InputRequired, Length, NumberRange, ValidationError
from wtforms.fields.html5 import DateField as Date

categories = [
    ("", "-- -- --"),
    ("Food", "Food"),
    ("Daily", "Daily"),
    ("Electronics", "Electronics"),
    ("Education", "Education"),
    ("Transportation", "Transportation"),
    ("Shopping", "Shopping"),
    ("Clothes", "Clothes"),
    ("Book", "Book"),
    ("Gift", "Gift"),
    ("Rent", "Rent"),
    ("Travel", "Travel"),
    ("Medical", "Medical"),
    ("Other", "Other"),
]


def valdate_category(self, field):
    if field.data == "":
        raise ValidationError("Please select category")


class ExpenseForm(FlaskForm):
    name = StringField(
        "Name", [InputRequired(message="Please enter expense name"), Length(max=50)]
    )
    date = DateField("Date", [InputRequired(message="Please enter date")])
    category = SelectField(
        "Category", choices=categories, validators=[valdate_category]
    )
    price = FloatField(
        "Amount",
        [
            InputRequired(message="Please enter amount"),
            NumberRange(min=0, message="Amount can't be negative"),
        ],
    )
    submit = SubmitField("Submit")


class DateForm(FlaskForm):
    start_date = Date("Start Date")
    end_date = Date("End Date")
    submit = SubmitField("Show")

    def validate_end_date(self, end_date):
        if end_date.data < self.start_date.data:
            raise ValidationError("End date must not be earlier than start date.")
