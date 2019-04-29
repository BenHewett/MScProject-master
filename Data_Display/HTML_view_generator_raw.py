import pandas as pd
from mysql import connector
from bs4 import BeautifulSoup
import re


location = '/Users/benjaminhewett/PycharmProjects/MScProjectFinal/Data_Display/templates/'


def create_view_raw_data():
    """
    Pull data from DB
    Parse into a HTML file
    :return: HTML file for raw data view
    """
    # Config MySQL
    connection = connector.connect(user='root', password='elsamax1981',
                                   host='localhost',
                                   database='mscproject')

    cursor = connection.cursor()

    _SQL = str.format("""SELECT file_name, script, fluent, disfluent, frame_rate, channels, sample_width FROM Audio_Data_Raw""")
    cursor.execute(_SQL)
    fetch = cursor.fetchall()

    filename = []
    script = []
    fluent = []
    disfluent = []
    frame_rate = []
    channels = []
    sample_width = []
    play_file = []

    data = filename, script, fluent, disfluent, frame_rate, channels, sample_width, play_file

    for row in fetch:
        data[0].append(row[0])
        data[1].append(row[1])
        if row[2] == 1:
            data[2].append('True')
        else:
            data[2].append('False')
        if row[3] == 1:
            data[3].append('True')
        else:
            data[3].append('False')
        data[4].append(row[4])
        data[5].append(row[5])
        data[6].append(row[6])
        data[7].append('TEST')

    table_data = {'Filename': data[0], 'Script': data[1], 'Fluent': data[2], 'Disfluent': data[3], 'Frame_Rate': data[4], 'Channels': data[5], 'Sample_Width': data[6], 'Play File': data[7]}

    data_frame = pd.DataFrame(data=table_data)
    pd.set_option('display.max_colwidth', 150)

    data_frame.to_html(location + 'Raw_Audio_Data_Table.html')

    # Amendments
    # Append HTML header onto file
    file = open(location + 'Raw_Audio_Data_Table.html')
    soup = BeautifulSoup(file, 'html.parser')

    html_to_add = '<!doctype html>' + '\n' + \
                  '<html>' + '\n' + \
                  '<head>' + '\n' + \
                  '<meta charset="utf-8">' + '\n' + \
                  '<title>ASR and Disfluent Speech Processing</title>' + '\n' + \
                  '<meta name="viewport" content="width=device-width, initial-scale=1.0">' + '\n' + \
                  '</head>' + '\n' + \
                  '<h3 align="center">Project Data - Raw Data</h3>' + '\n' + \
                  '<a href=\"../../Final.html\">Main Menu</a>' + '\n' + '<br>' + '\n' + \
                  '<br>' + '\n'

    soup_string = html_to_add + str(soup)

    string_iter = re.finditer('TEST', soup_string)

    iter_length = 0
    for line in string_iter:
        iter_length += 1

    for i in range(iter_length):
        if filename[i][-13:-4] == 'R1!Fluent':
            audio_html = '<audio controls><source src=\"../../Audio_Data/R1/Fluent/' + filename[
                i] + '\" type=\"audio/wav\"></audio>'
            soup_string = soup_string.replace('TEST', audio_html, 1)
        elif filename[i][-16:-4] == 'R1!Disfluent':
            audio_html = '<audio controls><source src=\"../../Audio_Data/R1/Disfluent/' + filename[
                i] + '\" type=\"audio/wav\"></audio>'
            soup_string = soup_string.replace('TEST', audio_html, 1)
        elif filename[i][-13:-4] == 'R2!Fluent':
            audio_html = '<audio controls><source src=\"../../Audio_Data/R2/Fluent/' + filename[
                i] + '\" type=\"audio/wav\"></audio>'
            soup_string = soup_string.replace('TEST', audio_html, 1)
        elif filename[i][-16:-4] == 'R2!Disfluent':
            audio_html = '<audio controls><source src=\"../../Audio_Data/R2/Disfluent/' + filename[
                i] + '\" type=\"audio/wav\"></audio>'
            soup_string = soup_string.replace('TEST', audio_html, 1)
        elif filename[i][-13:-4] == 'R3!Fluent':
            audio_html = '<audio controls><source src=\"../../Audio_Data/R3/Fluent/' + filename[
                i] + '\" type=\"audio/wav\"></audio>'
            soup_string = soup_string.replace('TEST', audio_html, 1)
        elif filename[i][-16:-4] == 'R3!Disfluent':
            audio_html = '<audio controls><source src=\"../../Audio_Data/R3/Disfluent/' + filename[
                i] + '\" type=\"audio/wav\"></audio>'
            soup_string = soup_string.replace('TEST', audio_html, 1)
        elif filename[i][-13:-4] == 'G1!Fluent':
            audio_html = '<audio controls><source src=\"../../Audio_Data/G1/Fluent/' + filename[
                i] + '\" type=\"audio/wav\"></audio>'
            soup_string = soup_string.replace('TEST', audio_html, 1)
        elif filename[i][-16:-4] == 'G1!Disfluent':
            audio_html = '<audio controls><source src=\"../../Audio_Data/G1/Disfluent/' + filename[
                i] + '\" type=\"audio/wav\"></audio>'
            soup_string = soup_string.replace('TEST', audio_html, 1)

    soup_list = soup_string.split('\n')
    new_line = soup_list[8][:-1] + ' align="center"'
    soup_list[8] = new_line + '>'
    soup_list.append('<br>' + '\n' + '</html>')

    file1 = open(location + 'Raw_Audio_Data_Table.html', 'w')
    for line in soup_list:
        file1.write(line + '\n')

    print('Raw Data HTML Table Generated')


def create_view_fluent_data():
    """
      Pull data from DB
      Parse into a HTML file
      :return: HTML file for raw data view
      """
    # Config MySQL
    connection = connector.connect(user='root', password='elsamax1981',
                                   host='localhost',
                                   database='mscproject')

    cursor = connection.cursor()

    _SQL = str.format("""SELECT file_name, script, fluent, disfluent, frame_rate, channels, sample_width FROM Audio_Data_Raw WHERE fluent=1""")
    cursor.execute(_SQL)
    fetch = cursor.fetchall()

    filename = []
    script = []
    fluent = []
    disfluent = []
    frame_rate = []
    channels = []
    sample_width = []
    play_file = []

    data = filename, script, fluent, disfluent, frame_rate, channels, sample_width, play_file

    for row in fetch:
        data[0].append(row[0])
        data[1].append(row[1])
        if row[2] == 1:
            data[2].append('True')
        else:
            data[2].append('False')
        if row[3] == 1:
            data[3].append('True')
        else:
            data[3].append('False')
        data[4].append(row[4])
        data[5].append(row[5])
        data[6].append(row[6])
        data[7].append('TEST')

    table_data = {'Filename': data[0], 'Script': data[1], 'Fluent': data[2], 'Disfluent': data[3], 'Frame_Rate': data[4],
                  'Channels': data[5], 'Sample_Width': data[6], 'Play File': data[7]}

    data_frame = pd.DataFrame(data=table_data)
    pd.set_option('display.max_colwidth', 80)

    data_frame.to_html(location + 'Fluent_Audio_Data_Table.html')

    # Append HTML header onto file
    file = open(location + 'Fluent_Audio_Data_Table.html')
    soup = BeautifulSoup(file, 'html.parser')

    html_to_add = '<!doctype html>' + '\n' + \
                  '<html>' + '\n' + \
                  '<head>' + '\n' + \
                  '<meta charset="utf-8">' + '\n' + \
                  '<title>ASR and Disfluent Speech Processing</title>' + '\n' + \
                  '<meta name="viewport" content="width=device-width, initial-scale=1.0">' + '\n' + \
                  '</head>' + '\n' + \
                  '<h3 align="center">Project Data - Fluent Data</h3>' + '\n' + \
                  '<a href=\"../../Final.html\">Main Menu</a>' + '\n' + '<br>' + '\n' + '<br>' + '\n'

    soup_string = html_to_add + str(soup)

    string_iter = re.finditer('TEST', soup_string)

    iter_length = 0
    for line in string_iter:
        iter_length += 1

    for i in range(iter_length):
        if filename[i][-13:-4] == 'R1!Fluent':
            audio_html = '<audio controls><source src=\"../../Audio_Data/R1/Fluent/' + filename[
                i] + '\" type=\"audio/wav\"></audio>'
            soup_string = soup_string.replace('TEST', audio_html, 1)
        elif filename[i][-13:-4] == 'R2!Fluent':
            audio_html = '<audio controls><source src=\"../../Audio_Data/R2/Fluent/' + filename[
                i] + '\" type=\"audio/wav\"></audio>'
            soup_string = soup_string.replace('TEST', audio_html, 1)
        elif filename[i][-13:-4] == 'R3!Fluent':
            audio_html = '<audio controls><source src=\"../../Audio_Data/R3/Fluent/' + filename[
                i] + '\" type=\"audio/wav\"></audio>'
            soup_string = soup_string.replace('TEST', audio_html, 1)
        elif filename[i][-13:-4] == 'G1!Fluent':
            audio_html = '<audio controls><source src=\"../../Audio_Data/G1/Fluent/' + filename[
                i] + '\" type=\"audio/wav\"></audio>'
            soup_string = soup_string.replace('TEST', audio_html, 1)

    soup_list = soup_string.split('\n')
    new_line = soup_list[8][:-1] + ' align="center"'
    soup_list[8] = new_line + '>'
    soup_list.append('<br>' + '\n' + '\n' + '</html>')

    file1 = open(location + 'Fluent_Audio_Data_Table.html', 'w')
    for line in soup_list:
        file1.write(line + '\n')

    print('Fluent Data HTML Table Generated')


def create_view_disfluent_data():
    """
      Pull data from DB
      Parse into a HTML file
      :return: HTML file for raw data view
      """
    # Config MySQL
    connection = connector.connect(user='root', password='elsamax1981',
                                   host='localhost',
                                   database='mscproject')

    cursor = connection.cursor()

    _SQL = str.format("""SELECT file_name, script, fluent, disfluent, frame_rate, channels, sample_width FROM Audio_Data_Raw WHERE disfluent=1""")
    cursor.execute(_SQL)
    fetch = cursor.fetchall()

    filename = []
    script = []
    fluent = []
    disfluent = []
    frame_rate = []
    channels = []
    sample_width = []
    play_file = []

    data = filename, script, fluent, disfluent, frame_rate, channels, sample_width, play_file

    for row in fetch:
        data[0].append(row[0])
        data[1].append(row[1])
        if row[2] == 1:
            data[2].append('True')
        else:
            data[2].append('False')
        if row[3] == 1:
            data[3].append('True')
        else:
            data[3].append('False')
        data[4].append(row[4])
        data[5].append(row[5])
        data[6].append(row[6])
        data[7].append('TEST')

    table_data = {'Filename': data[0], 'Script': data[1], 'Fluent': data[2], 'Disfluent': data[3], 'Frame_Rate': data[4],
                  'Channels': data[5], 'Sample_Width': data[6], 'Play File': data[7]}

    data_frame = pd.DataFrame(data=table_data)
    pd.set_option('display.max_colwidth', 80)

    data_frame.to_html(location + 'Disfluent_Audio_Data_Table.html')

    # Amendments
    # Append HTML header onto file
    file = open(location + 'Disfluent_Audio_Data_Table.html')
    soup = BeautifulSoup(file, 'html.parser')

    html_to_add = '<!doctype html>'+'\n'+  \
             '<html>'+'\n'+ \
             '<head>'+'\n'+ \
             '<meta charset="utf-8">'+'\n'+ \
             '<title>ASR and Disfluent Speech Processing</title>'+'\n'+ \
             '<meta name="viewport" content="width=device-width, initial-scale=1.0">'+'\n'+ \
             '</head>'+'\n'+ \
             '<h3 align="center">Project Data - Disfluent Data</h3>'+'\n'+ \
             '<a href=\"../../Final.html\">Main Menu</a>' + '\n'+ '<br>' + '\n'+ \
             '<br>' + '\n'

    soup_string = html_to_add + str(soup)

    string_iter = re.finditer('TEST', soup_string)

    iter_length = 0
    for line in string_iter:
        iter_length += 1

    for i in range(iter_length):
        if filename[i][-16:-4] == 'R1!Disfluent':
            audio_html = '<audio controls><source src=\"../../Audio_Data/R1/Disfluent/' + filename[
                i] + '\" type=\"audio/wav\"></audio>'
            soup_string = soup_string.replace('TEST', audio_html, 1)
        elif filename[i][-16:-4] == 'R2!Disfluent':
            audio_html = '<audio controls><source src=\"../../Audio_Data/R2/Disfluent/' + filename[
                i] + '\" type=\"audio/wav\"></audio>'
            soup_string = soup_string.replace('TEST', audio_html, 1)
        elif filename[i][-16:-4] == 'R3!Disfluent':
            audio_html = '<audio controls><source src=\"../../Audio_Data/R3/Disfluent/' + filename[
                i] + '\" type=\"audio/wav\"></audio>'
            soup_string = soup_string.replace('TEST', audio_html, 1)
        elif filename[i][-16:-4] == 'G1!Disfluent':
            audio_html = '<audio controls><source src=\"../../Audio_Data/G1/Disfluent/' + filename[
                i] + '\" type=\"audio/wav\"></audio>'
            soup_string = soup_string.replace('TEST', audio_html, 1)

    soup_list = soup_string.split('\n')
    new_line = soup_list[8][:-1] + ' align="center"'
    soup_list[8] = new_line + '>'
    soup_list.append('<br>' + '\n' +  '\n' + '</html>')

    file1 = open(location + 'Disfluent_Audio_Data_Table.html', 'w')
    for line in soup_list:
        file1.write(line + '\n')

    print('Disfluent Data HTML Table Generated')