import sys
import smbus2 as smbus
import time
import sqlite3
import os.path
import datetime 
import smtplib, ssl

I2C_SLAVE_ADDRESS1 = 0xf

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "db.sqlite3")


def sendmail_list():
    port = 587  # For starttls
    smtp_server = "smtp.gmail.com"
    sender_email = "smichelsen@hawk.iit.edu"
    receiver_email = "sammymichelsen@gmail.com"
    password = ""
    message = """\
    Subject: Hi there

    This message is sent from Python."""

    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo()  # Can be omitted
        server.starttls(context=context)
        server.ehlo()  # Can be omitted
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)

def convertStringsToBytes(src):
    converted = []
    for b in src:
        converted.append(ord(b))
    return converted

def main(args):
    I2Cbus = smbus.SMBus(1)
    conn = sqlite3.connect(db_path)
    print("connected to SQLite")
    while True:
        email_list = []
        now = datetime.datetime.now()
        dt_string = now.strftime("%H:%M:%S")
        with smbus.SMBus(1) as I2Cbus:
            try:
                data1 = I2Cbus.read_i2c_block_data(I2C_SLAVE_ADDRESS1,0x00,21)
                #data comes in as array of bytes, in this format:
                #[flame1,flame2,flame3,flame4,flame5,flame6,flame7,flame8,smoke1,smoke2,smoke3,smoke4,smoke5,smoke6,smoke7,smoke8,motion,humidity,temp1,temp2,water]
                print(str(data1))
                file = open("logfile.txt","w")
                file.write(str(data1))
                file.close()
                for x in range(1,22):
                    status = ""
                    if x < 9 and int(data1[x-1]) < 1:
                        status = "critical"
                    elif x<9 and int(data1[x-1]) > 0:
                        status = "normal"
                    elif x >= 9 and x <= 16 and int(data1[x-1]) < 160:
                        status = "normal"
                    elif x>=9 and x<=16 and int(data1[x-1]) < 200:
                        status = "warning"
                    elif x>=9 and x<=16 and int(data1[x-1])>=200:
                        status = "critical"
                        email_list.append("y")
                    elif x == 17 and data1[x-1] == 1:
                        status = "critical"
                    elif x == 17 and data1[x-1] == 0:
                        status = "nornal"
                    elif x == 18 and data1[x-1] >=80:
                        status = "critical"
                    elif x == 18 and data1[x-1] <80:
                        status = "normal"
                    elif x >=19 and x <=20 and data1[x-1] > 82:
                        status = "critical"
                    elif x>=19 and x<=20 and data1[x-1] <=82:
                        status = "normal"
                    
                    else:
                        status = "undefined"
                    conn.execute("UPDATE myapp_sensors_table SET value = ?, time = ?, status = ? WHERE id = ?",(data1[x-1], dt_string,status,x))
                conn.commit()
                print("values updated")
                print("The length of the list is " + str(len(email_list)))
                time.sleep(3)
            except KeyboardInterrupt:
                print("exiting")
                exit(0)
    return 0

if __name__ == "__main__":
    try:
        main(sys.argv)
    except KeyboardInterrupt:
        print("stopped")
    input()

