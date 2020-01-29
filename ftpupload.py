import os
from ftplib import FTP

from credentials import ftplogin, ftppassword, ftpserver


# print(ftpserver + ftplogin + ftppassword)


def ftpfileupload(filename='rawdata_now.csv', filepath='data/rawdata_now.csv'):
    ftp = FTP(ftpserver)
    ftp.login(ftplogin, ftppassword)
    print(filename)
    with open(f'{filepath}', 'rb') as f:
        ftp.storbinary(f'STOR {filename}', f)
    print(f'{filename} hochgeladen')
    ftp.quit()
    print(f'ftp upload von {filename} an {ftpserver} erfolgreich')


def ftpupload(folderpath='data/dwcharts/'):
    ftp = FTP(ftpserver)
    ftp.login(ftplogin, ftppassword)
    directory = os.fsencode(folderpath)

    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        print(file)
        print(filename)
        with open(f'{folderpath}{filename}', 'rb') as f:
            ftp.storbinary(f'STOR {filename}', f)
        print(f'{filename} hochgeladen')
    ftp.quit()
    print(f'ftp upload an {ftpserver} erfolgreich')
