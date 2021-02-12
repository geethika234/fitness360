from flask_wtf import FlaskForm
from wtforms import SelectField, FloatField, SubmitField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, NumberRange, Optional


class WeightGoalCalculatorForm(FlaskForm):
    curr_weight = FloatField('Current Weight',
                             validators=[DataRequired(),
                                         NumberRange(min=20, max=300)],
                             render_kw={'unit': 'kg'})
    curr_height = FloatField('Current Height',
                             validators=[DataRequired(),
                                         NumberRange(min=80, max=240)],
                             render_kw={'unit': 'cm'})
    birth_date = DateField('Birth Date', validators=[DataRequired()])
    act_level = SelectField('Activity Level',
                            coerce=float,
                            choices=[(1.2, 'Sedentary'),
                                     (1.375, 'Light Activity'),
                                     (1.55, 'Moderate Activity'),
                                     (1.725, 'Intense Activity'),
                                     (1.9, 'Elite Athlete')],
                            validators=[DataRequired()])
    goal_weight = FloatField('Goal Weight',
                             validators=[DataRequired(),
                                         NumberRange(min=20, max=300)],
                             render_kw={'unit': 'kg'})
    at_time = DateField('Exactly On', validators=[DataRequired()])
    pred_height = FloatField('Predicted Height',
                             validators=[DataRequired(),
                                         NumberRange(min=80, max=240)],
                             render_kw={'unit': 'cm'})
    submit = SubmitField('Calculate')


class CalorieCounterForm(FlaskForm):
    food = SelectField('Food',
                            coerce=int,
                            choices=[(12, 'Apple'),
                                     (137, 'Rice'),
                                     (60, 'Chocolate'),
                                     (175, 'Cake'),
                                     (19, 'Orange')],
                            validators=[DataRequired()])
    grams_consumed = FloatField('Grams Consumed', validators=[DataRequired(),
                                            NumberRange(min=1)],
                       render_kw={'unit': 'grams'})
    submit = SubmitField('Add Data')
    view = SubmitField('View')


class ExerciseCounterForm(FlaskForm):
    exercise = SelectField('Exercise',
                            coerce=int,
                            choices=[(12, 'Walking'),
                                     (137, 'Running'),
                                     (60, 'Jogging'),
                                     (175, 'Yoga'),
                                     (19, 'Weight Lifting')],
                            validators=[DataRequired()])
    time = FloatField('Time', validators=[DataRequired(),
                                            NumberRange(min=1)],
                       render_kw={'unit': 'mins'})
    submit = SubmitField('Add Data')
    view = SubmitField('View')


class DietExerciseSuggestionForm(FlaskForm):
    weight = FloatField('Weight',
                             validators=[DataRequired(),
                                         NumberRange(min=20, max=300)],
                             render_kw={'unit': 'kg'})
    heigth = FloatField('Height',
                           validators=[DataRequired(),
                                       NumberRange(min=1, max=200)],
                            render_kw={'unit': 'cm'})   
    age = FloatField('Age',
                           validators=[DataRequired(),
                                       NumberRange(min=1, max=200)])
    surgery = SelectField('Surgery',
                            coerce=int,
                            choices=[(1, 'NA'),
                                     (2, 'Heart'),
                                     (3, 'Cancer Therapy')],
                            validators=[DataRequired()])  
    submit = SubmitField('Suggest')


class HealthMonitorForm(FlaskForm):
    heart_rate = FloatField('Heart rate',
                        validators=[DataRequired(),
                                    NumberRange(min=50, max=200)])
    sleep_time = FloatField('Sleep Time',
                               validators=[DataRequired(),
                                           NumberRange(min=0)],
                               render_kw={'unit': 'hrs'})
    submit = SubmitField('End Day')
    view = SubmitField('View')
