import sys

#from lib import conn_aws_s3
from connections import conn_aws_s3

from extract_postgres import getaws, updatepostgres


def awsfilesize(bucketname, awsfolder, thefile):
    """

    :param bucketname: AWS S3 bucketname.
    :param awsfolder: AWS folder name.
    :param thefile: File in the given aws bucket.
    :return: Returns a tuple (filesize, rowcount).

    """
    bucketobject = bucketname.objects.filter(Prefix=awsfolder, Delimiter='/')
    existingfiles = [thefiles.key.encode('ascii', 'ignore').split('/')[1] for thefiles in bucketobject]

    for awsfile in bucketobject:
        filename = awsfile.key.encode('ascii', 'ignore').split('/')[1]

        if filename == thefile and awsfile.size > 0:
            return filename, awsfile.size, awsfile.get()["Body"].read().decode('utf8').count('\n') - 1
    if thefile not in existingfiles:
        raise Exception("The given file doesn't exist. Please check if the filename is correct.")


if __name__ == '__main__':
    extractid = sys.argv[1].split("=")[1]
    detaillogid = sys.argv[2].split("=")[1]
    awsfilename = sys.argv[3].split("=")[1]

    awsdetails = getaws(3)  # Get aws credentials for this extractid. E.g 1
    aws_access_key = awsdetails[0][0]
    aws_secret_key = awsdetails[0][1]
    aws_bucket = awsdetails[0][2]
    aws_folder = awsdetails[0][3]

    aws_bucket_object = conn_aws_s3(aws_access_key, aws_secret_key, aws_bucket)
    filedetails = awsfilesize(aws_bucket_object, aws_folder, awsfilename)
    updatepostgres(filedetails[0], filedetails[1], 105)

