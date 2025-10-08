from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime

app = Flask(__name__)
app.secret_key = "wellness_secret"

weekly_logs = []

def predict_burnout(entry):
    score = (
        (entry['sleep'] * 0.25) +
        (entry['physical'] * 0.15) +
        (entry['study'] * 0.20) +
        ((10 - entry['mood']) * 0.20) +
        (entry['stress'] * 0.20)
    )
    burnout_percent = max(0, min(100, 100 - score))
    return burnout_percent

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        date = request.form.get('date')
        sleep = float(request.form.get('sleep', 0))
        physical = float(request.form.get('physical', 0))
        study = float(request.form.get('study', 0))
        mood = float(request.form.get('mood', 5))
        stress = float(request.form.get('stress', 5))

        entry = {
            'date': date,
            'sleep': sleep,
            'physical': physical,
            'study': study,
            'mood': mood,
            'stress': stress
        }
        entry['burnout'] = predict_burnout(entry)
        weekly_logs.append(entry)

        if entry['burnout'] > 75:
            message = "You're doing great! Keep it up!"
        elif entry['burnout'] > 50:
            message = "You're managing well, but take breaks often."
        else:
            message = "Please take care! Rest and relax more."

        flash(message, "info")
        return redirect(url_for('index'))

    return render_template('index.html', logs=weekly_logs)

if __name__ == '__main__':
    app.run(debug=True)
