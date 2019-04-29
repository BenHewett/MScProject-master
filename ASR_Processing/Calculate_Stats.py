from mysql import connector
from bs4 import BeautifulSoup

########################################################################################################################

# MySQL Database connection and cursor objects
connection = connector.connect(user='root', password='elsamax1981',
                               host='localhost',
                               database='mscproject')

cursor = connection.cursor()

########################################################################################################################


def get_fluent_stats() ->list:
    """
    Retrieve required data for fluent speakers from the database.
    Calculate required statistics, as per in-line comments.
    :return: List of data
    """
    # Fetch all data from the database
    _SQL = str.format("""SELECT filename, script_id, ASR_accuracy_rate FROM ASR_Results WHERE fluent=TRUE """)
    cursor.execute(_SQL)
    fetch = cursor.fetchall()

    # Create lists to delineate data
    filenames = []
    script_id = []
    ar = []

    # Loop through DB data. If fluent file, distribute data to relevant list
    for line in fetch:
        if line[2] > 14:
            filenames.append(line[0])
            script_id.append(line[1])
            ar.append(line[2])

    # Calculate required stats in a list of lists
    # Number of files, Number of R1 files, Number of R2 files, Number of R3 files, Number of G1 files
    # Lowest accuracy rate, Highest accuracy rate, Average accuracy rate
    fluent = [len(filenames), len([c for c in script_id if c == 'R1']), len([c for c in script_id if c == 'R2']),
              len([c for c in script_id if c == 'R3']), len([c for c in script_id if c == 'G1']),
              min([c for c in ar]), round(max([c for c in ar]), 2),  round(sum([c for c in ar]) / len([c for c in ar]), 2)]

    # Lowest accuracy rate, highest accuracy rate, average accuracy rate
    fluent_r1 = [round(min([ar[t] for t in range(len(script_id)) if script_id[t] == 'R1']), 2),
                 round(max([ar[t] for t in range(len(script_id)) if script_id[t] == 'R1']), 2),
                 round(sum([ar[t] for t in range(len(script_id)) if script_id[t] == 'R1']) /
                       len([ar[t] for t in range(len(script_id)) if script_id[t] == 'R1']), 2)]

    # Lowest accuracy rate, highest accuracy rate, average accuracy rate
    fluent_r2 = [round(min([ar[t] for t in range(len(script_id)) if script_id[t] == 'R2']), 2),
                 round(max([ar[t] for t in range(len(script_id)) if script_id[t] == 'R2']), 2),
                 round(sum([ar[t] for t in range(len(script_id)) if script_id[t] == 'R2']) /
                       len([ar[t] for t in range(len(script_id)) if script_id[t] == 'R2']), 2)]

    # Lowest accuracy rate, highest accuracy rate, average accuracy rate
    fluent_r3 = [round(min([ar[t] for t in range(len(script_id)) if script_id[t] == 'R3']), 2),
                 round(max([ar[t] for t in range(len(script_id)) if script_id[t] == 'R3']), 2),
                 round(sum([ar[t] for t in range(len(script_id)) if script_id[t] == 'R3']) /
                       len([ar[t] for t in range(len(script_id)) if script_id[t] == 'R3']), 2)]

    # Lowest accuracy rate, highest accuracy rate, average accuracy rate
    fluent_g1 = [round(min([ar[t] for t in range(len(script_id)) if script_id[t] == 'G1']), 2),
                 round(max([ar[t] for t in range(len(script_id)) if script_id[t] == 'G1']), 2),
                 round(sum([ar[t] for t in range(len(script_id)) if script_id[t] == 'G1']) /
                       len([ar[t] for t in range(len(script_id)) if script_id[t] == 'G1']), 2)]

    # Return a list of lists of all results
    results = [fluent, fluent_r1, fluent_r2, fluent_r3, fluent_g1]

    return results


def get_disfluent_stats() -> list:
    """
    Retrieve required data for disfluent speakers from the database.
    Calculate required statistics, as per in-line comments.
    :return: List of data
    """
    # Fetch all data from the database
    _SQL = str.format("""SELECT filename, script_id, ASR_accuracy_rate FROM ASR_Results WHERE disfluent=TRUE """)
    cursor.execute(_SQL)
    fetch = cursor.fetchall()

    # Create lists to delineate data
    filenames = []
    script_id = []
    ar = []

    # Loop through DB data. If disfluent file, distribute data to relevant list
    for line in fetch:
        if line[2] > 14:
            filenames.append(line[0])
            script_id.append(line[1])
            ar.append(line[2])

    # Calculate required stats in a list of lists
    # Number of files, Number of R1 files, Number of R2 files, Number of R3 files, Number of G1 files
    # Lowest accuracy rate, Highest accuracy rate, Average accuracy rate
    disfluent = [len(filenames), len([c for c in script_id if c == 'R1']), len([c for c in script_id if c == 'R2']),
              len([c for c in script_id if c == 'R3']), len([c for c in script_id if c == 'G1']),
              min([c for c in ar]), round(max([c for c in ar]), 2),
              round(sum([c for c in ar]) / len([c for c in ar]), 2)]

    # Lowest accuracy rate, highest accuracy rate, average accuracy rate
    disfluent_r1 = [round(min([ar[t] for t in range(len(script_id)) if script_id[t] == 'R1']), 2),
                 round(max([ar[t] for t in range(len(script_id)) if script_id[t] == 'R1']), 2),
                 round(sum([ar[t] for t in range(len(script_id)) if script_id[t] == 'R1']) /
                       len([ar[t] for t in range(len(script_id)) if script_id[t] == 'R1']), 2)]

    # Lowest accuracy rate, highest accuracy rate, average accuracy rate
    disfluent_r2 = [round(min([ar[t] for t in range(len(script_id)) if script_id[t] == 'R2']), 2),
                 round(max([ar[t] for t in range(len(script_id)) if script_id[t] == 'R2']), 2),
                 round(sum([ar[t] for t in range(len(script_id)) if script_id[t] == 'R2']) /
                       len([ar[t] for t in range(len(script_id)) if script_id[t] == 'R2']), 2)]

    # Lowest accuracy rate, highest accuracy rate, average accuracy rate
    disfluent_r3 = [round(min([ar[t] for t in range(len(script_id)) if script_id[t] == 'R3']), 2),
                 round(max([ar[t] for t in range(len(script_id)) if script_id[t] == 'R3']), 2),
                 round(sum([ar[t] for t in range(len(script_id)) if script_id[t] == 'R3']) /
                       len([ar[t] for t in range(len(script_id)) if script_id[t] == 'R3']), 2)]

    # Lowest accuracy rate, highest accuracy rate, average accuracy rate
    disfluent_g1 = [round(min([ar[t] for t in range(len(script_id)) if script_id[t] == 'G1']), 2),
                 round(max([ar[t] for t in range(len(script_id)) if script_id[t] == 'G1']), 2),
                 round(sum([ar[t] for t in range(len(script_id)) if script_id[t] == 'G1']) /
                       len([ar[t] for t in range(len(script_id)) if script_id[t] == 'G1']), 2)]

    # Return a list of lists of results
    results = [disfluent, disfluent_r1, disfluent_r2, disfluent_r3, disfluent_g1]

    return results


def create_html(fluent_stats, disfluent_stats) -> None:
    """
    Format HTML template and insert statistical data values for display.
    :param fluent_stats: function call to get_fluent_stats()
    :param disfluent_stats: function call to get_disfluent_stats()
    :return: None
    """
    # Locations for files
    template_path = '/Users/benjaminhewett/PycharmProjects/MScProjectFinal/ASR_Processing/'
    destination_path = '/Users/benjaminhewett/PycharmProjects/MScProjectFinal/Data_Display/templates/'

    # Open file, parse file into Beautiful Soup object, cast object as String for modification
    file = open(template_path + 'Stats_template.html')
    soup = BeautifulSoup(file, 'html.parser')
    soup_string = str(soup)

    # Calls to functions to get required data statistics
    fluent_stats = fluent_stats
    disfluent_stats = disfluent_stats

    # HTML file modification
    # Input stats - fluent box
    soup_string = soup_string.replace('F!', str(fluent_stats[0][0]), 1)
    soup_string = soup_string.replace('R-R1', str(fluent_stats[0][1]), 1)
    soup_string = soup_string.replace('R-R2', str(fluent_stats[0][2]), 1)
    soup_string = soup_string.replace('R-R3', str(fluent_stats[0][3]), 1)
    soup_string = soup_string.replace('G-G1', str(fluent_stats[0][4]), 1)
    soup_string = soup_string.replace('AR-LR', str(fluent_stats[0][5]) + '%', 1)
    soup_string = soup_string.replace('AR-HR', str(fluent_stats[0][6]) + '%', 1)
    soup_string = soup_string.replace('AR-AV', str(fluent_stats[0][7]) + '%', 1)

    # Input stats - disfluent box
    soup_string = soup_string.replace('F!', str(disfluent_stats[0][0]), 1)
    soup_string = soup_string.replace('R-R1', str(disfluent_stats[0][1]), 1)
    soup_string = soup_string.replace('R-R2', str(disfluent_stats[0][2]), 1)
    soup_string = soup_string.replace('R-R3', str(disfluent_stats[0][3]), 1)
    soup_string = soup_string.replace('G-G1', str(disfluent_stats[0][4]), 1)
    soup_string = soup_string.replace('AR-LR', str(disfluent_stats[0][5]) + '%', 1)
    soup_string = soup_string.replace('AR-HR', str(disfluent_stats[0][6]) + '%', 1)
    soup_string = soup_string.replace('AR-AV', str(disfluent_stats[0][7]) + '%', 1)

    # Input stats - 'all' box
    soup_string = soup_string.replace('F!', str(disfluent_stats[0][0] + fluent_stats[0][0]), 1)
    soup_string = soup_string.replace('R-R1', str(disfluent_stats[0][1] + fluent_stats[0][1]), 1)
    soup_string = soup_string.replace('R-R2', str(disfluent_stats[0][2] + fluent_stats[0][2]), 1)
    soup_string = soup_string.replace('R-R3', str(disfluent_stats[0][3] + fluent_stats[0][3]), 1)
    soup_string = soup_string.replace('G-G1', str(disfluent_stats[0][4] + fluent_stats[0][4]), 1)
    soup_string = soup_string.replace('AR-LR', str(min(disfluent_stats[0][5], fluent_stats[0][5])) + '%', 1)
    soup_string = soup_string.replace('AR-HR', str(max(disfluent_stats[0][6], fluent_stats[0][6])) + '%', 1)
    soup_string = soup_string.replace('AR-AV', str(round((disfluent_stats[0][7] + fluent_stats[0][7]) / 2, 2)) + '%', 1)

    # Input stats - R1 box
    soup_string = soup_string.replace('F!', str(fluent_stats[0][1]), 1)
    soup_string = soup_string.replace('F!', str(disfluent_stats[0][1]), 1)
    soup_string = soup_string.replace('AR-LR', str(fluent_stats[1][0]) + '%', 1)
    soup_string = soup_string.replace('AR-HR', str(fluent_stats[1][1]) + '%', 1)
    soup_string = soup_string.replace('AR-LR', str(disfluent_stats[1][0]) + '%', 1)
    soup_string = soup_string.replace('AR-HR', str(disfluent_stats[1][1]) + '%', 1)
    soup_string = soup_string.replace('AR-AF', str(fluent_stats[1][2]) + '%', 1)
    soup_string = soup_string.replace('AR-AD', str(disfluent_stats[1][2]) + '%', 1)

    # Input stats - R2 box
    soup_string = soup_string.replace('F!', str(fluent_stats[0][2]), 1)
    soup_string = soup_string.replace('F!', str(disfluent_stats[0][2]), 1)
    soup_string = soup_string.replace('AR-LR', str(fluent_stats[2][0]) + '%', 1)
    soup_string = soup_string.replace('AR-HR', str(fluent_stats[2][1]) + '%', 1)
    soup_string = soup_string.replace('AR-LR', str(disfluent_stats[2][0]) + '%', 1)
    soup_string = soup_string.replace('AR-HR', str(disfluent_stats[2][1]) + '%', 1)
    soup_string = soup_string.replace('AR-AF', str(fluent_stats[2][2]) + '%', 1)
    soup_string = soup_string.replace('AR-AD', str(disfluent_stats[2][2]) + '%', 1)

    # Input stats - R3 box
    soup_string = soup_string.replace('F!', str(fluent_stats[0][3]), 1)
    soup_string = soup_string.replace('F!', str(disfluent_stats[0][3]), 1)
    soup_string = soup_string.replace('AR-LR', str(fluent_stats[3][0]) + '%', 1)
    soup_string = soup_string.replace('AR-HR', str(fluent_stats[3][1]) + '%', 1)
    soup_string = soup_string.replace('AR-LR', str(disfluent_stats[3][0]) + '%', 1)
    soup_string = soup_string.replace('AR-HR', str(disfluent_stats[3][1]) + '%', 1)
    soup_string = soup_string.replace('AR-AF', str(fluent_stats[3][2]) + '%', 1)
    soup_string = soup_string.replace('AR-AD', str(disfluent_stats[3][2]) + '%', 1)

    # Input stats - G1 box
    soup_string = soup_string.replace('F!', str(fluent_stats[0][4]), 1)
    soup_string = soup_string.replace('F!', str(disfluent_stats[0][4]), 1)
    soup_string = soup_string.replace('AR-LR', str(fluent_stats[4][0]) + '%', 1)
    soup_string = soup_string.replace('AR-HR', str(fluent_stats[4][1]) + '%', 1)
    soup_string = soup_string.replace('AR-LR', str(disfluent_stats[4][0]) + '%', 1)
    soup_string = soup_string.replace('AR-HR', str(disfluent_stats[4][1]) + '%', 1)
    soup_string = soup_string.replace('AR-AF', str(fluent_stats[4][2]) + '%', 1)
    soup_string = soup_string.replace('AR-AD', str(disfluent_stats[4][2]) + '%', 1)

    # Write HTML string to file
    file1 = open(destination_path + 'Stats.html', 'w')
    for line in soup_string.split('\n'):
        file1.write(line + '\n')

    print('Stats HTML Generated.')


