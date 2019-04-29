from configparser import ConfigParser
from mysql.connector import MySQLConnection, Error


def read_ini(filename='/Users/benjaminhewett/PycharmProjects/MScProjectFinal/Web_Application_Data_Collection_Prototype/data_processing/MScProject.ini'):
    """
    Reads the .ini file for DB login
    :param filename: filename of .ini file
    :return: login details for MScProject data_processing
    """
    config = ConfigParser()

    config.read(filename)

    db = {}

    if config.has_section('mysql'):
        items = config.items('mysql')
        for item in items:
            db[item[0]] = item[1]

    return db


def connect():
    """
    Connect to MySQL database: MScProject
    :return: SQL connection object
    """

    # Read the configuration ini file
    db_config = read_ini()

    try:
        print('Connecting to MySQL database...')
        con = MySQLConnection(**db_config)

        if con.is_connected():
            print('Connection Established!')
            return con
        else:
            print('Connection Failed')
            return 'Connection Failed'

    except Error as error:
        print(error)