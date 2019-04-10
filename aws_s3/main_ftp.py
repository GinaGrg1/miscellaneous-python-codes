import sys
from StringIO import StringIO
from datetime import datetime

from extract_postgres import getftp, updatepostgres
from connections import conn_ftp


def ftpfilesize(ftpconn, ftpfolder, ftpfile):
    """
    For the given file name, first check if the file is in the given folder and if it is there then return
    the its size and row count as a tuple. If the file doesn't exist, then raise an exception.

    :param ftpconn: ftp connection.
    :param ftpfolder: the folder in the server where the file lands.
    :param ftpfile: the file that we want to find the file size and row count of.
    :return: returns the size of the file and row count as integers.
    """
    existingfiles = [files for files in ftpconn.nlst(ftpfolder)]
    for filename in ftpconn.nlst(ftpfolder):
        if filename == ftpfile:
            r = StringIO()
            ftpconn.retrbinary('RETR /{}/{}'.format(ftpfolder, filename), r.write)
            return ftpconn.size(ftpfolder + '/{}'.format(filename)), r.getvalue().count("\n") + 1
    if ftpfile not in existingfiles:
        raise Exception("File Not Found. Please check if the filename is correct.")


if __name__ == '__main__':
    extractid = sys.argv[1].split("=")[1]
    detaillogid = sys.argv[2].split("=")[1]
    ftpfilename = sys.argv[2].split("=")[1]

    ftpdetails = getftp(extractid)  # Get ftp connection details for this extractid.
    ftp_hostname = ftpdetails[0][0]
    ftp_username = ftpdetails[0][1]
    ftp_password = ftpdetails[0][2]
    ftp_folder = ftpdetails[0][3]
    updated_datetime = datetime.now()

    ftp = conn_ftp(ftp_hostname, ftp_username, ftp_password)  # Make ftp connection.
    ftpfiledetails = ftpfilesize(ftp, ftp_folder, ftpfilename)

    updatepostgres(ftpfiledetails[0], ftpfiledetails[1], detaillogid)



