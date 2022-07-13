import pyodbc
server = 'localhost'
database = 'zoom_face_recognition'
username = 'SA'
password = 'daedalusS1'
driver = '{ODBC Driver 17 for SQL Server}' # Driver you need to connect to the database
port = '1433'
cnn = pyodbc.connect('DRIVER='+driver+';PORT=port;SERVER='+server+';PORT=1443;DATABASE='+database+';UID='+username+
                 ';PWD='+password)
cursor = cnn.cursor()
