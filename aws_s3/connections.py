import sys
import os
import ftplib
import psycopg2
import paramiko
from boto.s3.connection import S3Connection
from boto.sts import STSConnection

sys.path.append(os.path.abspath("/usr/lib64/python2.7/site-packages"))


def getconfig(*params):
    """
    Gets all the connection details from config.properties. First creates a dictionary and
    returns the values of keys provided as parameters.
    :param params:
    :return: returns a tuple for e.g ('localhost', 'admin', 'db')
    """
    configdict, connectiondetails = {}, []
    with open("./config.properties", "r") as configfile:
        for line in configfile:
            if not line.startswith('#') and line.strip():
                key, value = line.strip().split("=", 1)
                configdict[key.strip()] = value.strip()

    for items in params:
        connectiondetails.append(configdict[items])
    return connectiondetails


def conn_pg():
    """
    Make connection to postgres.
    :return:
    """
    configs = getconfig('DB_POSTGRESS_HOST', 'DB_POSTGRESS_USER', 'DB_POSTGRESS_PASSWORD', 'DB_POSTGRESS_DATABASE')
    # connect=None
    try:
        connect = psycopg2.connect(host=configs[0], user=configs[1], password=configs[2], dbname=configs[3])
        print "Successfully connected to database : " + configs[3]
        return connect

    except Exception as exn:
        print "Can't connect to database {}. {} : {}".format(getconfig(configs[3]), exn.__class__.__name__, exn)
        return None


def conn_ftp(ftp_hostname, ftp_username, ftp_password):
    """
    Making connection to ftp server.
    """
    try:
        ftp = ftplib.FTP(ftp_hostname, ftp_username, ftp_password)
        return ftp

    except Exception as ftp_err:
        print "Connection to ftp {} : {}".format(ftp_err.__class__.__name__, ftp_err)


def conn_sftp(sftp_hostname, sftp_username, sftp_password):
    """
    Making connection to sftp server.
    :param sftp_hostname:
    :param sftp_username:
    :param sftp_password:
    :return:
    """
    try:
        transport = paramiko.Transport(sftp_hostname, 22)
        transport.connect(username=sftp_username, password=sftp_password)
        sftp_client = paramiko.SFTPClient.from_transport(transport)
        return sftp_client
    except Exception as sftp_err:
        print "Connection to ftp {} : {}".format(sftp_err.__class__.__name__, sftp_err)



def conn_aws_s3(aws_access_key, aws_secret_key, aws_bucket):
    """

    Makes connection to AWS S3 bucket. The connection details comes from extract_postgres.getargosaws(id)
    :return: Returns the bucket.
    If using boto3:
        session = boto3.Session(aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key)
        s3 = session.resource('s3')
        return s3.Bucket(aws_bucket)
    """
    try:
        conn = S3Connection(aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key)
        return conn.get_bucket(aws_bucket)
    except Exception as exn:
        print "The error is {} : {}".format(exn.__class__.__name__, exn)


def conn_aws_arnrole_s3(aws_arn_role, aws_arn_session_name, aws_arn_session_duration, aws_bucket):
    """

    Makes connection to AWS S3 bucket with arn details. The connection details comes from extract_postgres.getawsarn(id)
    :return: Returns the bucket.

    If using boto3:
        sts_client = boto3.client('sts')
        assumedroleobject = sts_client.assume_role(RoleArn=aws_arn_role,
                                                   RoleSessionName=aws_arn_session_name,
                                                   DurationSeconds=aws_arn_session_duration)
        credentials = assumedroleobject['Credentials']
        s3_resource = boto3.resource(
            's3', aws_access_key_id=credentials['AccessKeyId'],
            aws_secret_access_key=credentials['SecretAccessKey'],
            aws_session_token=credentials['SessionToken'])
        return s3_resource.Bucket(aws_bucket)

    """
    try:
        sts_connection = STSConnection()
        tempCredentials = sts_connection.assume_role(role_arn=aws_arn_role,
                                                     role_session_name=aws_arn_session_name,
                                                     duration_seconds=aws_arn_session_duration)

        s3_connection = S3Connection(aws_access_key_id=tempCredentials.credentials.access_key,
                                     aws_secret_access_key=tempCredentials.credentials.secret_key,
                                     security_token=tempCredentials.credentials.session_token)
        return s3_connection.get_bucket(aws_bucket)

    except Exception as exn:
        print "The error is {} : {}".format(exn.__class__.__name__, exn)
