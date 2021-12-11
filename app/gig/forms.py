from flask_wtf import FlaskForm
from wtforms.validators import NumberRange, InputRequired, Length
from wtforms.fields import StringField, TextAreaField, DecimalField, SubmitField
from wtforms.widgets import Input
from markupsafe import Markup

class PriceInput(Input):
    input_type = "number"

    def __call__(self, field, **kwargs):
        kwargs.setdefault("id", field.id)
        kwargs.setdefault("type", self.input_type)
        kwargs.setdefault("step", "0.01")
        if "value" not in kwargs:
            kwargs["value"] = field._value()
        if "required" not in kwargs and "required" in getattr(field, "flags", []):
            kwargs["required"] = True
        return Markup("""<div class="input-group mb-3">
            <div class="input-group-prepend">
                <span class="input-group-text">$</span>
            </div>
            <input %s>
        </div>""" % self.html_params(name=field.name, **kwargs))


class PriceField(DecimalField):
    widget = PriceInput()

class GigForm(FlaskForm):
    title =         StringField("Title", 
                        validators=[
                            InputRequired("Gig must have a title"),
                            Length(min=5, max=80, message="Title must be between %(min)d and %(max)d characters"),
                        ])
    description =   TextAreaField("Description", 
                        validators=[
                            InputRequired(),
                            Length(min=10, max=200, message="Title must be between %(min)d and %(max)d characters"),
                        ])
    payment =       PriceField("Payment", 
                        validators=[
                            NumberRange(min=0.0, message="Cannot be negative")
                        ])
    location =      StringField("Location", 
                        validators=[
                            InputRequired(),
                            Length(min=3, max=50, message="Title must be between %(min)d and %(max)d characters"),
                        ])

class CreateGigForm(GigForm):
    submit      = SubmitField("Create gig")

class UpdateGigForm(GigForm):
    submit      = SubmitField("Update gig")