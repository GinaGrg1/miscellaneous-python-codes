import argparse
import roles as r

parser = argparse.ArgumentParser(description='Creating DDL Scripts')
parser.add_argument('-e','--environment', type=str, help='The environment the DDL will run for.')
parser.add_argument('-acl', '--additionalacl', type=str, help='Check if additional ACL is required.')

args = parser.parse_args()

environment = args.environment.lower()
addadditionalaclsfordatalakeapp = True if args.additionalacl.lower() == "true" else False


def postfix(environ):
    mappings = {'dev' : '_dev', 'preprod' : '_pp', 'prod': ''}
    return mappings.get(environ)


def validations():
    if r.PrimaryDatabase.startswith('ods_'):
        if r.PrimaryApplicationRole.startswith("r_")| r.ApplicationAdminsRole.startswith("r_")| r.BusinessUsersRole.startswith("r_"):
            return True
    else:
        print("ERROR : must start with ods_ and r_")
        exit()


def rolestogroupsddl():
    return """
    GRANT ROLE {0} TO GROUP {1};
    GRANT ROLE {2} TO GROUP {3};
    GRANT ROLE {4} TO GROUP {5};
    """.format(PrimaryApplicationRole, PrimaryServiceAccountName, ApplicationAdminsRole, ApplicationAdminGroup, BusinessUsersRole, BusinessUsersGroup)


def createdatabaseddl(PrimaryDatabase):
    return  """
    CREATE DATABASE IF NOT EXISTS {0}_stage;
    CREATE DATABASE IF NOT EXISTS {0}_data;
    CREATE DATABASE IF NOT EXISTS {0}_sandbox;
    CREATE DATABASE IF NOT EXISTS {0}_presentation;
    """.format(PrimaryDatabase)


def grantsentrypermissionsddl(PrimaryDatabase, PrimaryApplicationRole, ApplicationAdminsRole, BusinessUsersRole):
    return """
    -- Grants for the Primary Application Role (i.e. the bit that does the work)
    -- If you want, you can reduce this down as you feel appropriate
    GRANT ALL ON DATABASE {0}_stage TO ROLE {1};
    GRANT ALL ON DATABASE {0}_data TO ROLE {1};
    GRANT ALL ON DATABASE {0}_presentation TO ROLE {1};
    
    -- Application Admins
    GRANT SELECT ON DATABASE {0}_stage TO ROLE {2};
    GRANT SELECT ON DATABASE {0}_data TO ROLE {2};
    GRANT SELECT ON DATABASE {0}_presentation TO ROLE {2};
    GRANT ALL ON DATABASE {0}_sandbox TO ROLE {2};
    
    
    -- Business users
    GRANT SELECT ON DATABASE {0}_presentation TO ROLE {3};
    GRANT ALL ON DATABASE {0}_sandbox TO ROLE {3};
    """.format(PrimaryDatabase, PrimaryApplicationRole, ApplicationAdminsRole, BusinessUsersRole)


def addACLS(PrimaryServiceAccount,PrimaryDatabase):
    return """
    hdfs dfs -setfacl -m -R user::rwx,group::rwx,group:{0}:r-x,other::r-x /user/hive/warehouse/{1}_data.db
    hdfs dfs -setfacl -m -R user::rwx,group::rwx,group:{0}:r-x,other::r-x /user/hive/warehouse/{1}_presentation.db
    hdfs dfs -setfacl -m -R user::rwx,group::rwx,group:{0}:r-x,other::r-x /user/hive/warehouse/{1}_stage.db
    hdfs dfs -setfacl -m -R user::rwx,group::rwx,group:{0}:rwx,other::r-x /user/hive/warehouse/{1}_sandbox.db
    """.format(PrimaryServiceAccount, PrimaryDatabase)


def additionalACLS(PrimaryServiceAccount, PrimaryDatabase):
    addedACLS = addACLS(PrimaryServiceAccount, PrimaryDatabase)
    additionalacls = addedACLS + """
    hdfs dfs -setfacl -m -R group:{0}:rwx,group:{1}:rwx /user/hive/warehouse/{2}_stage.db
    hdfs dfs -setfacl -m -R group:{0}:rwx,group:{1}:rwx /user/hive/warehouse/{2}_data.db
    hdfs dfs -setfacl -m -R group:{0}:rwx,group:{1}:rwx /user/hive/warehouse/{2}_presentation.db
    hdfs dfs -setfacl -m -R group:{0}:rwx,group:{1}:rwx /user/hive/warehouse/{2}_sandbox.db
        """.format(DataLakeAppGroup, DataLakeAdminGroup, PrimaryDatabase)
    return additionalacls

if __name__ == '__main__':
    validations()
    PrimaryServiceAccountName = r.PrimaryServiceAccountName + postfix(environment)
    PrimaryDatabase = r.PrimaryDatabase.lower()
    PrimaryApplicationRole = r.PrimaryApplicationRole + postfix(environment)
    ApplicationAdminGroup = r.ApplicationAdminGroup + postfix(environment)
    ApplicationAdminsRole = r.ApplicationAdminsRole + postfix(environment)
    BusinessUsersGroup = r.BusinessUsersGroup + postfix(environment)
    BusinessUsersRole = r.BusinessUsersRole + postfix(environment)
    DataLakeAppGroup = r.DataLakeAppGroup + postfix(environment)
    DataLakeAdminGroup = r.DataLakeAdminGroup + postfix(environment)
    sentryfilename = 'sentry_script_' + PrimaryDatabase + postfix(environment) + '.hql'
    aclfilename = 'acl_scripts_' + PrimaryDatabase + postfix(environment) + '.txt'

    with open(sentryfilename, 'a') as myfile:
        myfile.write(rolestogroupsddl())
        myfile.write(createdatabaseddl(PrimaryDatabase))
        myfile.write(grantsentrypermissionsddl(PrimaryDatabase, PrimaryApplicationRole, ApplicationAdminsRole, BusinessUsersRole))

    with open(aclfilename, 'a') as aclfile:
        if addadditionalaclsfordatalakeapp:
            aclfile.write(additionalACLS(PrimaryServiceAccountName, PrimaryDatabase))
        else:
            aclfile.write(addACLS(PrimaryServiceAccount, PrimaryDatabase))


