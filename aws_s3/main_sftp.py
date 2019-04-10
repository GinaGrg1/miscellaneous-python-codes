import sys

from extract_postgres import getftp, updatepostgres
from connections import conn_sftp


def sftpfilesize(sftpclient, sftpfolder, filename):
    """
    For the given file name, first check if the file is in the given folder and if it is there then return
    the its size and row count as a tuple. If the file doesn't exist, then raise an exception.

    :param sftpclient: this is the sftp connection.
    :param sftpfolder: the folder in the server where the file is located.
    :param filename: the file that we want to find the size and row count of.
    :return: returns the size of the file and row count as integers.
    """
    existingfile = [thefiles for thefiles in sftpclient.listdir(sftpfolder)]
    for sftpfile in sftpclient.listdir(sftpfolder):
        if sftpfile == filename:
            rowcount = len(sftpclient.open(sftpfolder+'/'+sftpfile, 'r').readlines())
            sizeoffile = sftpclient.stat(sftpfolder+'/'+sftpfile).st_size
            return sizeoffile, rowcount
    if filename not in existingfile:
        raise Exception("The given file doesn't exist. Please check if the filename is correct.")


if __name__ == "__main__":
    extractid = sys.argv[1].split("=")[1]
    detaillogid = sys.argv[2].split("=")[1]
    sftpfilename = sys.argv[3].split("=")[1]

    sftpdetails = getftp(1)  # Get sftp connection details for this extractid.
    sftp_hostname = sftpdetails[0][0]
    sftp_username = sftpdetails[0][1]
    sftp_password = sftpdetails[0][2]
    sftp_folder = sftpdetails[0][3]

    sftp_client = conn_sftp(sftp_hostname, sftp_username, sftp_password)

    sftpfiledetails = sftpfilesize(sftp_client, sftp_folder, sftpfilename)
    updatepostgres(sftpfiledetails[0], sftpfiledetails[1], detaillogid)
