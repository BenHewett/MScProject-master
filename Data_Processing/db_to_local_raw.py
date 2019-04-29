from mysql import connector
import wave
import os

location = '/Users/benjaminhewett/PycharmProjects/MScProjectFinal/Audio_Data/'


def from_db_fluent():
    """
    Retrieve all files by fluent speakers from DB and filter by script to specified locations.
    Checks for duplicates.

    location + R1/Fluent
    location + R2/Fluent
    location + R3/Fluent
    location + G1/Fluent

    Prints confirmation.

    :return: None
    """
    print('Retrieving fluent file(s) from DB...')

    # Get list of files currently in directory
    wav_files_f = []

    for path, sub, files in os.walk(location):
        for f in files:
            wav_files_f.append(f)

    # Config MySQL
    connection = connector.connect(user='root', password='elsamax1981',
                                   host='localhost',
                                   database='mscproject')

    cursor = connection.cursor()

    _SQL = str.format("""SELECT * FROM Audio_Data_Raw WHERE fluent=TRUE""")
    cursor.execute(_SQL)
    fetch = cursor.fetchall()

    for row in fetch:
        ident = row[0]
        name = row[1]
        script = row[2]
        fluent = row[3]
        disfluent = row[4]
        frame = row[5]
        chann = row[6]
        samps = row[7]
        data = row[8]

        if script == 'R1' and name not in wav_files_f:
            w = wave.open(location + 'R1/Fluent/' + name, 'w')

            w.setnchannels(chann)
            w.setsampwidth(samps)
            w.setframerate(frame)
            w.setcomptype('NONE', 'Not Compressed')
            w.writeframesraw(data)
            w.close()
        elif script == 'R2' and name not in wav_files_f:
            w = wave.open(location + 'R2/Fluent/' + name, 'w')

            w.setnchannels(chann)
            w.setsampwidth(samps)
            w.setframerate(frame)
            w.setcomptype('NONE', 'Not Compressed')
            w.writeframesraw(data)
            w.close()
        elif script == 'R3' and name not in wav_files_f:
            w = wave.open(location + 'R3/Fluent/' + name, 'w')

            w.setnchannels(chann)
            w.setsampwidth(samps)
            w.setframerate(frame)
            w.setcomptype('NONE', 'Not Compressed')
            w.writeframesraw(data)
            w.close()
        elif script == 'G1' and name not in wav_files_f:
            w = wave.open(location + 'G1/Fluent/' + name, 'w')

            w.setnchannels(chann)
            w.setsampwidth(samps)
            w.setframerate(frame)
            w.setcomptype('NONE', 'Not Compressed')
            w.writeframesraw(data)
            w.close()

    print('Fluent File(s) Retrieved')


def from_db_disfluent():
    """
    Retrieve all files by disfluent speakers from DB and filter by script to specified locations.
    Checks for duplicates.

    location + R1/Disfluent
    location + R2/Disfluent
    location + R3/Disfluent
    location + G1/Disfluent

    Prints confirmation.

    :return: None
    """
    print('Retrieving disfluent file(s) from DB...')

    # Get list of files currently in directory
    wav_files_f = []

    for path, sub, files in os.walk(location):
        for f in files:
            wav_files_f.append(f)

    # Config MySQL
    connection = connector.connect(user='root', password='elsamax1981',
                                   host='localhost',
                                   database='mscproject')

    cursor = connection.cursor()

    _SQL = str.format("""SELECT * FROM Audio_Data_Raw WHERE disfluent=TRUE """)
    cursor.execute(_SQL)
    fetch = cursor.fetchall()

    for row in fetch:
        ident = row[0]
        name = row[1]
        script = row[2]
        fluent = row[3]
        disfluent = row[4]
        frame = row[5]
        chann = row[6]
        samps = row[7]
        data = row[8]

        if script == 'R1' and name not in wav_files_f:
            w = wave.open(location + 'R1/Disfluent/' + name, 'w')

            w.setnchannels(chann)
            w.setsampwidth(samps)
            w.setframerate(frame)
            w.setcomptype('NONE', 'Not Compressed')
            w.writeframesraw(data)
            w.close()
        elif script == 'R2' and name not in wav_files_f:
            w = wave.open(location + 'R2/Disfluent/' + name, 'w')

            w.setnchannels(chann)
            w.setsampwidth(samps)
            w.setframerate(frame)
            w.setcomptype('NONE', 'Not Compressed')
            w.writeframesraw(data)
            w.close()
        elif script == 'R3' and name not in wav_files_f:
            w = wave.open(location + 'R3/Disfluent/' + name, 'w')

            w.setnchannels(chann)
            w.setsampwidth(samps)
            w.setframerate(frame)
            w.setcomptype('NONE', 'Not Compressed')
            w.writeframesraw(data)
            w.close()
        elif script == 'G1' and name not in wav_files_f:
            w = wave.open(location + 'G1/Disfluent/' + name, 'w')

            w.setnchannels(chann)
            w.setsampwidth(samps)
            w.setframerate(frame)
            w.setcomptype('NONE', 'Not Compressed')
            w.writeframesraw(data)
            w.close()

    print('Disfluent File(s) Retrieved')
