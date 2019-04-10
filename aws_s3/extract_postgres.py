from connections import conn_pg


def getaws(extractid):
    """

    Returns the aws access key id, secret key, bucket name and target directory for a given extract id.
    :param extractid:
    :return: Returns the cursor connections.

    """
    postgres = conn_pg()
    cursor = postgres.cursor()
    cursor.execute("SELECT aws_access_key_id, aws_secret_access_key, aws_bucket_name, target_directory \
                    FROM \"postgres\".table_metainfo WHERE extract_id = {}".format(extractid)
                   )
    return cursor.fetchall()


def getawsarn(extractid):
    """

    Returns the aws access key id, secret key, bucket name and target directory for a given extract id.
    :param extractid:
    :return:

    """
    postgres = conn_pg()
    cursor = postgres.cursor()
    cursor.execute("SELECT aws_bucket_name, aws_role_arn ,aws_role_arn_session_name, aws_role_arn_session_duration,\
                    target_directory FROM \"postgres\".table_metainfo WHERE extract_id = {}".format(extractid))

    return cursor.fetchall()


def getftp(extractid):
    """
    Depending on the connection details saved in the database in relation to the given extractid, this could be
    either ftp or sftp host, username, password and target director.

    :param extractid:
    :return:
    """
    postgres = conn_pg()
    cursor = postgres.cursor()
    cursor.execute("SELECT sftp_host, sftp_username, sftp_password, target_directory \
                    FROM \"postgres\".table_metainfo WHERE extract_id = {}".format(extractid))
    return cursor.fetchall()


def updatepostgres(size, rowcount, logid):
    """
    Update the postgres table dl_job_detail_extract_ctrl_log for either s3, ftp or sftp.
    :param size:
    :param rowcount:
    :param logid:
    :return:
    """
    conn = conn_pg()
    cursor = conn.cursor()
    cursor.execute("UPDATE \"postgres\".detail_ctrl_log \
                   SET target_filesize = {}, target_record_count = {} \
                   WHERE detail_log_id = {} ;".format(size, rowcount, logid)
                   )
    conn.commit()
    conn.close()

