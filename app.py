import random
from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key

dice_art = {
    1: '''
     -----
    |     |
    |  *  |
    |     |
     -----''',
    2: '''
     -----
    | *   |
    |     |
    |   * |
     -----''',
    3: '''
     -----
    | *   |
    |  *  |
    |   * |
     -----''',
    4: '''
     -----
    | * * |
    |     |
    | * * |
     -----''',
    5: '''
     -----
    | * * |
    |  *  |
    | * * |
     -----''',
    6: '''
     -----
    | * * |
    | * * |
    | * * |
     -----'''
}

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'dice_values' not in session:
        session['dice_values'] = [random.randint(1, 6) for _ in range(5)]
    dice_representations = [dice_art[val] for val in session['dice_values']]

    if 'correct_guesses' not in session:
        session['correct_guesses'] = 0

    total = 0

    for die in session['dice_values']:
        if die == 3:
            total += 2
        elif die == 5:
            total += 4

    if request.method == 'POST':
        user_guess = int(request.form.get('guess'))
        
        if user_guess == total:
            session['correct_guesses'] += 1
            flash('Correct! Correct Value: ' + str(total) + ' Correct guesses: ' + str(session['correct_guesses']),'success')
            if session['correct_guesses'] == 3:
                session['correct_guesses'] = 0
                return render_template('congrats.html')
        else:
            flash('Incorrect! Correct Value: ' + str(total) , 'danger')
            session['correct_guesses'] = 0
        
        session.pop('dice_values', None)  # Remove dice values from session
        return redirect(url_for('index'))

    return render_template('index.html', dice_art=dice_representations)

if __name__ == '__main__':
    app.run(debug=True)
