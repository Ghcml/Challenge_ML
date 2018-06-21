import mysql.connector
import imaplib
import email

user = input("Ingresar usuario gmail:")
pwd = input("Ingresar contraseña gmail:")

server = imaplib.IMAP4_SSL("imap.gmail.com")
server.login (user, pwd)
sts, count = server.select('INBOX')

rslt, data = server.search(None,'(TEXT "Devops")')
inbox_item_list = data[0].split()

for i in inbox_item_list:
    _host_ = input("Ingresar host mysql:")
    _user_ = input("Ingresar usuario mysql:")
    _password_ = input("Ingresar password mysql:")

    cnx = mysql.connector.connect(host=_host_, user=_user_, passwd=_password_)
    cursr = cnx.cursor()

    typ, sbjct = server.fetch(i, '(RFC822)')
    text= sbjct[0][1]
    message = email.message_from_bytes(text)
    subjects = message['Subject']
    from_= message['From']
    fecha = message['Date']

    cursr.execute('CREATE DATABASE IF NOT EXISTS challenge_ml')
    cursr.execute('USE challenge_ml')
    cursr.execute('CREATE TABLE IF NOT EXISTS data(Remitente VARCHAR(50), Asunto VARCHAR(50), Fecha VARCHAR(50))')
    cursr.execute("INSERT INTO data VALUES (%s, %s, %s)", (from_, subjects, fecha))

    select = """select * from data"""
    cursr.execute(select)
    row = cursr.fetchall()
    print(row)

    cnx.commit()
    cnx.close()


server.logout()










