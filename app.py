from datetime import date
import sqlite3 
from flask import Flask, redirect, render_template, url_for
from forms import (HealthMonitorForm, DietExerciseSuggestionForm,
                   ExerciseCounterForm, CalorieCounterForm,
                   WeightGoalCalculatorForm)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'a random string'

cals={12:'Apple', 137:'Rice', 60:'Chocolate', 175:'Cake', 19:'Orange'}
exer={12:'Walking',137:'Running', 60:'Jogging', 175:'Yoga', 19:'Weight Lifting'}

@app.route('/')
def index():
    return redirect(url_for('weight_goal'))

@app.route('/weight_goal', methods=['GET', 'POST'])
def weight_goal():
    title = 'Weight Goal Calculator'
    form = WeightGoalCalculatorForm()
    result = None
    if form.validate_on_submit():
        curr_age = (date.today() - form.birth_date.data).days
        goal_age = (form.at_time.data - form.birth_date.data).days
        days_to_goal = goal_age - curr_age
        act_level = form.act_level.data
        curr_weight = form.curr_weight.data
        curr_height = form.curr_height.data
        goal_weight = form.goal_weight.data
        pred_height = form.pred_height.data
        r_raw = act_level * (66.473 + 6.8758 * (curr_weight + goal_weight)
                             + 2.50165 * (curr_height + pred_height) - 6.755
                             * 2 / 1461 * (curr_age + goal_age)) + 7716 * \
                             (goal_weight - curr_weight) / days_to_goal
        result = round(r_raw, 2)
    return render_template(
        'weight_goal.html',
        title=title,
        form=form,
        result=result
    )


@app.route('/calorie_count', methods=['GET', 'POST'])
def calorie_count():
    title = 'Calorie Counter'
    form = CalorieCounterForm()
    if form.view.data:
    	 return redirect(url_for('calorie_table'))
    if form.validate_on_submit():
        vals = [
            form.food.data,
            form.grams_consumed.data
        ]
        vals.append((vals[0]*vals[1])/100)
        vals[0] = cals[vals[0]]
        with sqlite3.connect("database/fitness360.db") as con:  
                cur = con.cursor()  
                cur.execute("INSERT into calorie_count (food, grams, calories) values (?,?,?)",(vals[0],vals[1],vals[2]))  
                con.commit()  
    return render_template(
        'calorie_count.html',
        title=title,
        form=form
    )
    con.close()  


@app.route('/exercise_count', methods=['GET', 'POST'])
def exercise_count():
    title = 'Exercise Counter'
    form = ExerciseCounterForm()
    if form.view.data:
    	 return redirect(url_for('exercise_table'))
    if form.validate_on_submit():
        vals = [
            form.exercise.data,
            form.time.data
        ]
        vals.append((vals[0]*vals[1])/10)
        vals[0] = exer[vals[0]]
        with sqlite3.connect("database/fitness360.db") as con:  
                cur = con.cursor()  
                cur.execute("INSERT into exercise_count (exercise, minutes, calories) values (?,?,?)",(vals[0],vals[1],vals[2]))  
                con.commit()
    return render_template(
        'exercise_count.html',
        title=title,
        form=form
    )
    con.close()


@app.route('/diet_exercise_suggestion', methods=['GET', 'POST'])
def diet_exercise_suggestion():
    title = 'Diet Exercise Suggestion'
    form = DietExerciseSuggestionForm()
    suggestion = None
    if form.validate_on_submit():
    	weight=form.weight.data
    	heigth=form.heigth.data
    	age=form.age.data
    	surgery=form.surgery.data
    	deno = (heigth*heigth)/10000
    	bmi = weight/deno
    	if bmi<25 and surgery == 1:
    		suggestion = "Emphasize fruits, vegetables, whole grains, and fat-free or low-fat milk and milk products. \n Includes lean meats, poultry, fish, beans, eggs, and nuts.\n Is low in saturated fats, trans fats, cholesterol, salt (sodium), and added sugars."
    	elif surgery == 1:
    		suggestion = "Eat a high protein diet. \n Reduce your stress levels. \n Don't eat a lot of sugary foods. \n Do aerobic exercise (cardio) \n Cut back on carbs — especially refined carbs."
    	elif surgery == 2:
    		suggestion="Lots of fruits and vegetables. \n lean meats. \n skinless poultry. \n nuts, beans, and legumes. \n fish. \n whole grains. \n plant-based oils, such as olive oil. \n low-fat dairy products."
    	else:
    		suggestion="2-3 cups of vegetables. \n 1-2 cups of fruit. \n 5-7 servings of grain-based foods (at least half should be whole grain) \n 2-3 servings of dairy (fat-free or low-fat milk, yogurt, cheese) \n 3-4 servings of protein"
        
    return render_template(
        'diet_exercise_suggestion.html',
        title=title,
        form=form,
        suggestion=suggestion
    )


@app.route('/health_monitor', methods=['GET', 'POST'])
def health_monitor():
    title = 'Health Monitor'
    form = HealthMonitorForm()
    if form.view.data:
    	 return redirect(url_for('health_table'))
    if form.validate_on_submit():
        vals = [
        form.heart_rate.data,
        form.sleep_time.data
        ]
        with sqlite3.connect("database/fitness360.db") as con:
        	cur = con.cursor()  
        	cur.execute('SELECT sum(calories) FROM calorie_count;')
        	sumc=cur.fetchone()[0]
        	vals.append(sumc)
        	cur.execute('SELECT sum(calories) FROM exercise_count;')
        	sume=cur.fetchone()[0]
        	vals.append(sume)
        	cur.execute("INSERT into health_monitor (heartrate, sleeptime, caloriesate, caloriesspent) values (?,?,?,?)",(vals[0],vals[1],vals[2],vals[3]))
        	cur.execute("delete from calorie_count;")
        	cur.execute("delete from exercise_count;")
        	con.commit()
    return render_template(
        'health_monitor.html',
        title=title,
        form=form
    )
    con.close()

@app.route('/calorie_table', methods=['GET', 'POST'])
def calorie_table():
	with sqlite3.connect("database/fitness360.db") as con:
        	cur = con.cursor()  
        	cur.execute('SELECT * FROM calorie_count;')
        	fooditem = cur.fetchall()
        	con.commit()
	return render_template("calorie_table.html",fooditem = fooditem)
	con.close()
	
@app.route('/exercise_table', methods=['GET', 'POST'])
def exercise_table():
	with sqlite3.connect("database/fitness360.db") as con:
        	cur = con.cursor()  
        	cur.execute('SELECT * FROM exercise_count;')
        	fooditem = cur.fetchall()
        	con.commit()
	return render_template("exercise_table.html",fooditem = fooditem)
	con.close()

@app.route('/health_table', methods=['GET', 'POST'])
def health_table():
	with sqlite3.connect("database/fitness360.db") as con:
        	cur = con.cursor()  
        	cur.execute('SELECT * FROM health_monitor;')
        	fooditem = cur.fetchall()
        	con.commit()
	return render_template("health_table.html",fooditem = fooditem)
	con.close()
if __name__ == '__main__':
    app.run(debug=True)
