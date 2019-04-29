from flask import Flask, render_template


# Create instance of Flask
app = Flask(__name__)


# Home page
@app.route('/')
def home():
    return render_template('home.html')


# Page 1_fluent
@app.route('/page1_fluent')
def page1_f():
    return render_template('page1_fluent.html')


# Page 1_disfluent
@app.route('/page1_disfluent')
def page1_d():
    return render_template('page1_disfluent.html')


# Page 2_fluent
@app.route('/page2_fluent')
def page2_f():
    return render_template('page2_fluent.html')


# Page 2_disfluent
@app.route('/page2_disfluent')
def page2_d():
    return render_template('page2_disfluent.html')


# Page 3_fluent
@app.route('/page3_fluent')
def page3_f():
    return render_template('page3_fluent.html')


# Page 3_disfluent
@app.route('/page3_disfluent')
def page3_d():
    return render_template('page3_disfluent.html')


# Page 4_fluent
@app.route('/page4_fluent')
def page4_f():
    return render_template('page4_fluent.html')


# Page 4_disfluent
@app.route('/page4_disfluent')
def page4_d():
    return render_template('page4_disfluent.html')


# Project explanation
@app.route('/project')
def project():
    return render_template('project.html')


if __name__ == '__main__':
    app.run(debug=True)
