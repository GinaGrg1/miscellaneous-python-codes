
from StringIO import StringIO
import pandas as pd

from extract_postgres import getftp
from connections import conn_ftp

from pyspark.sql import SparkSession
sparksession = SparkSession.builder.appName("FTP-To-HDFS").getOrCreate()


def ftpfilesize(ftpconn, ftpfolder, ftpfile):
    existingfiles = [files for files in ftpconn.nlst(ftpfolder)]
    for filename in ftpconn.nlst(ftpfolder):
        if filename == ftpfile:
            r = StringIO()
            ftpconn.retrbinary('RETR /{}/{}'.format(ftpfolder, filename), r.write)
            testdata = StringIO(r.getvalue())
            df = pd.read_csv(testdata)
            sparkdf = sparksession.createDataFrame(df)
            sparkdf.coalesce(1).write.csv('Some landing path')

    if ftpfile not in existingfiles:
        raise Exception("File Not Found. Please check if the filename is correct.")


if __name__ == '__main__':
    ftpfilename = 'fakefriends.csv'

    ftpdetails = getftp(2)  # Get ftp connection details for this extractid.
    ftp_hostname = ftpdetails[0][0]
    ftp_username = ftpdetails[0][1]
    ftp_password = ftpdetails[0][2]
    ftp_folder = ftpdetails[0][3]

    ftp = conn_ftp(ftp_hostname, ftp_username, ftp_password)  # Make ftp connection.
    ftpfiledetails = ftpfilesize(ftp, ftp_folder, ftpfilename)







