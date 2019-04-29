from mysql import connector
import pandas as pd
from bs4 import BeautifulSoup
import re


location = '/Users/benjaminhewett/PycharmProjects/MScProjectFinal/Data_Display/templates/'


def create_view_asr_processed_fluent():
    # Config MySQL
    connection = connector.connect(user='root', password='elsamax1981',
                                   host='localhost',
                                   database='mscproject')

    cursor = connection.cursor()

    _SQL = str.format(
        """SELECT filename, fluent, disfluent, script_id, script_word_count, ASR_script_word_count, ASR_accuracy_rate, misrecognition_count  FROM ASR_Results WHERE fluent=1""")
    cursor.execute(_SQL)
    fetch = cursor.fetchall()

    filename = []
    fluent = []
    disfluent = []
    script_id = []
    script_word_count = []
    asr_script_word_count = []
    asr_accuracy_rate = []
    misrec_count = []
    results = []

    data = filename, fluent, disfluent, script_id, script_word_count, asr_script_word_count, asr_accuracy_rate, \
           misrec_count, results

    for row in fetch:
        data[0].append(row[0])
        if row[1] == 1:
            data[1].append('True')
        else:
            data[1].append('False')
        if row[2] == 1:
            data[2].append('True')
        else:
            data[2].append('False')
        data[3].append(row[3])
        data[4].append(row[4])
        data[5].append(row[5])
        data[6].append(row[6])
        data[7].append(row[7])
        data[8].append('LINK')

    table_data = {'Filename': data[0], 'Fluent': data[1], 'Disfluent': data[2], 'Script_id': data[3],
                  'Script_word_count': data[4],
                  'ASR_script_word_count': data[5],
                  'ASR_accuracy_rate': data[6], 'Misrecognition_count': data[7], 'Results': data[8]}

    data_frame = pd.DataFrame(data=table_data)
    pd.set_option('display.max_colwidth', 80)

    data_frame.to_html(location + 'ASR_Processed_Fluent_Data.html')

    # Amendments
    # Append HTML header onto file
    file = open(location + 'ASR_Processed_Fluent_Data.html')
    soup = BeautifulSoup(file, 'html.parser')

    soup_string = '<a href=\"../../Final.html\">Main Menu</a>' + '\n' \
                  + '<br>' + '\n' + '<br>' + '\n' + '<h3 align="center">ASR Processed Data - Fluent</h3>' + str(soup)

    string_iter = re.finditer('LINK', soup_string)

    iter_length = 0
    for line in string_iter:
        iter_length += 1

    for i in range(iter_length):
        if filename[i][-13:-4] == 'R1!Fluent':
            results_html = '<a href="../templates/Results/' + filename[i][:-4] + '.html">RESULTS</a>'
            soup_string = soup_string.replace('LINK', results_html, 1)
        elif filename[i][-13:-4] == 'R2!Fluent':
            results_html = '<a href="../templates/Results/' + filename[i][:-4] + '.html">RESULTS</a>'
            soup_string = soup_string.replace('LINK', results_html, 1)
        elif filename[i][-13:-4] == 'R3!Fluent':
            results_html = '<a href="../templates/Results/' + filename[i][:-4] + '.html">RESULTS</a>'
            soup_string = soup_string.replace('LINK', results_html, 1)
        elif filename[i][-13:-4] == 'G1!Fluent':
            results_html = '<a href="../templates/Results/' + filename[i][:-4] + '.html">RESULTS</a>'
            soup_string = soup_string.replace('LINK', results_html, 1)

    soup_list = soup_string.split('\n')
    file1 = open(location + 'ASR_Processed_Fluent_Data.html', 'w')
    for line in soup_list:
        file1.write(line + '\n')

    print('Fluent Data ASR Result HTML Table Generated')


def create_view_asr_processed_disfluent():
    # Config MySQL
    connection = connector.connect(user='root', password='elsamax1981',
                                   host='localhost',
                                   database='mscproject')

    cursor = connection.cursor()

    _SQL = str.format(
        """SELECT filename, fluent, disfluent, script_id, script_word_count, ASR_script_word_count, ASR_accuracy_rate, misrecognition_count  FROM ASR_Results WHERE disfluent=1""")
    cursor.execute(_SQL)
    fetch = cursor.fetchall()

    filename = []
    fluent = []
    disfluent = []
    script_id = []
    script_word_count = []
    asr_script_word_count = []
    asr_accuracy_rate = []
    misrec_count = []
    results = []

    data = filename, fluent, disfluent, script_id, script_word_count, asr_script_word_count, asr_accuracy_rate, \
           misrec_count, results

    for row in fetch:
        data[0].append(row[0])
        if row[1] == 1:
            data[1].append('True')
        else:
            data[1].append('False')
        if row[2] == 1:
            data[2].append('True')
        else:
            data[2].append('False')
        data[3].append(row[3])
        data[4].append(row[4])
        data[5].append(row[5])
        data[6].append(row[6])
        data[7].append(row[7])
        data[8].append('LINK')

    table_data = {'Filename': data[0], 'Fluent': data[1], 'Disfluent': data[2], 'Script_id': data[3],
                  'Script_word_count': data[4],
                  'ASR_script_word_count': data[5],
                  'ASR_accuracy_rate': data[6], 'Misrecognition_count': data[7], 'Results': data[8]}

    data_frame = pd.DataFrame(data=table_data)
    pd.set_option('display.max_colwidth', 80)

    data_frame.to_html(location + 'ASR_Processed_Disfluent_Data.html')

    # Amendments
    # Append HTML header onto file
    file = open(location + 'ASR_Processed_Disfluent_Data.html')
    soup = BeautifulSoup(file, 'html.parser')

    soup_string = '<a href=\"../../Final.html\">Main Menu</a>' + '\n' + '<br>' + '\n' + \
                  '<br>' + '\n' + '<h3 align="center">ASR Processed Data - Disfluent</h3>' + str(soup)

    string_iter = re.finditer('LINK', soup_string)
    iter_length = 0
    for line in string_iter:
        iter_length += 1

    for i in range(iter_length):
        if filename[i][-16:-4] == 'R1!Disfluent':
            results_html = '<a href="../templates/Results/' + filename[i][:-4] + '.html">RESULTS</a>'
            soup_string = soup_string.replace('LINK', results_html, 1)
        elif filename[i][-16:-4] == 'R2!Disfluent':
            results_html = '<a href="../templates/Results/' + filename[i][:-4] + '.html">RESULTS</a>'
            soup_string = soup_string.replace('LINK', results_html, 1)
        elif filename[i][-16:-4] == 'R3!Disfluent':
            results_html = '<a href="../templates/Results/' + filename[i][:-4] + '.html">RESULTS</a>'
            soup_string = soup_string.replace('LINK', results_html, 1)
        elif filename[i][-16:-4] == 'G1!Disfluent':
            results_html = '<a href="../templates/Results/' + filename[i][:-4] + '.html">RESULTS</a>'
            soup_string = soup_string.replace('LINK', results_html, 1)

    soup_list = soup_string.split('\n')
    file1 = open(location + 'ASR_Processed_Disfluent_Data.html', 'w')
    for line in soup_list:
        file1.write(line + '\n')

    print('Disfluent Data ASR Result HTML Table Generated')


def generate_results_pages():

    html_template = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>ASR and Disfluent Speech Processing</title>
        </head>
        <body style="background-color: ghostwhite">
        <h2 align="center">ASR Processed Data - Result Page</h2>'
        <br>
        Link Here
        <p style="text-align: center">FILENAME</p>
        <br>
        <h3 style="text-decoration: underline; text-align: center">Original Script</h3>
        <br>
        <p style="text-align: center">ORIGINAL</p>
        <br>
        <h3 style="text-decoration: underline; text-align: center">ASR Script</h3>
        <br>
        <p style="text-align: center">ASR-S</p>
        <br>
        <h3 style="text-decoration: underline; text-align: center">Misrecognised Words</h3>
        <br>
        <p style="text-align: center">MISRECS</p>
        <br>
        </body>
        </html>"""

    # Config MySQL
    connection = connector.connect(user='root', password='elsamax1981',
                                   host='localhost',
                                   database='mscproject')

    cursor = connection.cursor()

    _SQL = str.format(
        """SELECT filename, script_text, ASR_script_text, misrecognitions  FROM ASR_Results""")
    cursor.execute(_SQL)
    fetch = cursor.fetchall()

    filename = []
    script = []
    asr_script = []
    misrecs = []

    data = filename, script, asr_script, misrecs

    for row in fetch:
        data[0].append(row[0])
        data[1].append(row[1])
        data[2].append(row[2])
        data[3].append(row[3])

    html = html_template

    for i in range(len(data[0])):
        if data[0][i][-13:-4] == 'Disfluent':
            html = html.replace('Link Here', '<a style="position: absolute; top: 10px" '
                                             'href="../ASR_Processed_DisFluent_Data.html">Back</a>')
            html = html.replace('FILENAME', data[0][i], 1)
            html = html.replace('ORIGINAL', data[1][i], 1)
            html = html.replace('ASR-S', data[2][i], 1)
            html = html.replace('MISRECS', data[3][i], 1)
        else:
            html = html.replace('Link Here', '<a style="position: absolute; top: 10px" '
                                             'href="../ASR_Processed_Fluent_Data.html">Back</a>')
            html = html.replace('FILENAME', data[0][i], 1)
            html = html.replace('ORIGINAL', data[1][i], 1)
            html = html.replace('ASR-S', data[2][i], 1)
            html = html.replace('MISRECS', data[3][i], 1)

        soup_list = html.split('\n')
        file1 = open('/Users/benjaminhewett/PycharmProjects/MScProjectFinal/Data_Display/templates/Results/' + data[0][i][:-4] + '.html', 'w')
        for line in soup_list:
            file1.write(line + '\n')

        html = html_template

    print('Results Pages Generated.')