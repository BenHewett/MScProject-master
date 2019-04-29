from flask import Flask, render_template, request
from Web_Application_Data_Collection_Prototype import Collection_Data_Process, Practise_Data_Process

app = Flask(__name__, static_folder='static')


# URL ‘/’ rule is bound to the home_page() function.
# As a result, if a user visits the http://localhost:5000/ URL, the output of the home_page() function
# will be rendered in the browser.

# Home page renderer
@app.route('/')
def home_page():
    return render_template('/Home_Page.html')


# Practise page renderer
@app.route('/practise/')
def practise_page():
    return render_template('Practise_Page.html')


# Collection page renderer
@app.route('/collection/')
def collection_page():
    return render_template('Collection_Page.html')

#####################################################


# Practise recording page buttons
@app.route('/practise_record_button1/', methods=['POST'])
def practise_record_start_audio_1():
    fluency_type = request.form['speech_category']
    Practise_Data_Process.process_data(fluency_type)
    return render_template('Practise_Page_Recording1_Done.html')


@app.route('/practise_record_button2/', methods=['POST'])
def practise_record_audio_2():
    fluency_type = request.form['speech_category']
    Practise_Data_Process.process_data(fluency_type)
    return render_template('Practise_Page_Recording2_Done.html')

################################################################


# Collection page buttons
@app.route('/collection_record_button1/', methods=['POST'])
def collection_start_record_audio_1():
    fluency_type = request.form['speech_category']
    Collection_Data_Process.process_data(fluency_type)
    return render_template('Collection_Page_Recording1_Done.html')


# Collection page buttons
@app.route('/collection_record_button2/', methods=['POST'])
def collection_start_record_audio_2():
    fluency_type = request.form['speech_category']
    Collection_Data_Process.process_data(fluency_type)
    return render_template('Collection_Page_Recording2_Done.html')


# Collection page buttons
@app.route('/collection_record_button3/', methods=['POST'])
def collection_start_record_audio_3():
    fluency_type = request.form['speech_category']
    Collection_Data_Process.process_data(fluency_type)
    return render_template('Collection_Page_Recording3_Done.html')


def run():
    app.run(debug=True, port=5000)


if __name__ == '__main__':
    run()
