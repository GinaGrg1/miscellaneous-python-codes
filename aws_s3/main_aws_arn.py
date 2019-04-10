import sys

from extract_postgres import getawsarn, updatepostgres
from connections import conn_aws_arnrole_s3


def filesize(bucketname, folder, filename):
    """
    This function takes in the s3 bucket object object and filters it based on the folder. It checks if the given file
    exists in the folder. It will raise an exception if the given file is not found.

    :param bucketname: the bucket object returned from making the aws s3 connection.
    :param folder: the s3 folder where the file is located.
    :param filename: the file in the folder that we want to find the size and row count of.
    :return: returns the size and row count of the given filename as integers
    """
    thebucket = bucketname.objects.filter(Prefix=folder, Delimiter='/')
    existingfiles = [thefile.key.encode('ascii', 'ignore').split('/')[1] for thefile in thebucket]
    for awsfile in thebucket:
        if awsfile.key.encode('ascii', 'ignore').split('/')[1] == filename and awsfile.size > 0:
            return filename, awsfile.size, awsfile.get()["Body"].read().decode('utf8').count('\n') - 1
    if filename not in existingfiles:
        raise Exception("File not found. Please check the file name.")


if __name__ == '__main__':
    extractid = sys.argv[1].split("=")[1]
    detaillogid = sys.argv[2].split("=")[1]
    awsfilename = sys.argv[3].split("=")[1]

    awsarndetails = getawsarn(6)  # Get aws arn credentials for this extractid.
    aws_arn_bucket = awsarndetails[0][0]
    aws_arn_role = awsarndetails[0][1]
    aws_arn_session_name = awsarndetails[0][2]
    aws_arn_session_duration = awsarndetails[0][3]
    aws_arn_folder = awsarndetails[0][4]

    aws_bucket_object = conn_aws_arnrole_s3(aws_arn_role, aws_arn_session_name, aws_arn_session_duration, aws_arn_bucket)
    filedetails = filesize(aws_bucket_object, aws_arn_folder, awsfilename)
    updatepostgres(filedetails[0], filedetails[1], detaillogid)
