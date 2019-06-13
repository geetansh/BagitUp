#!/usr/bin/python3


from environs import Env
import sys, getopt, os
import zipfile 
import hashlib
import random

from pathlib import Path


def values():
    #global directory_location
    argv = sys.argv[1:]
    try:
        opts, args = getopt.getopt(argv, 'd:h:', ['dir=','help'])
    except getopt.GetoptError:
            print ("exiting")
            sys.exit(2)
        

    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print ("-d parameter required")
            sys.exit(2)
        elif opt in ('-d', '--dir'):
            values.directory_location = arg
            print (values.directory_location)
            values.directory_location = str(Path(values.directory_location))
            print (values.directory_location)
    return           
    
values()    

def find_replace(search,replace):
    # Read in the file
    with open(values.directory_location + '/.env', 'r') as file :
        find_replace.filedata = file.read()

    # Replace the target string
    find_replace.filedata = find_replace.filedata.replace(search, replace)

    # Write the file out again
    with open(values.directory_location + '/.env', 'w') as file:
        file.write(find_replace.filedata)

def read_env_file():
    read_env_file.path = values.directory_location + "/.env"
    
    env = Env()
    env.read_env(read_env_file.path)  # read .env file, if it exists

    #check if .env file exist
    if not (os.path.exists(read_env_file.path)):    
        print (".env file missing, copy .env.example to .env and update values")
        sys.exit(2)

    else:
        print ("file is here")        
        
        if not env("token_key"):
            token = random.randrange(1, 99999999999999999999999999999999999, 30)
            token = str(token)
            print ("generating token: " + token)
            find_replace('token_key=""','token_key="' + token + '"')
            read_env_file.token_key = env("token_key")
            

        else:
            #import variables .from env file
            #token_keys
            read_env_file.token_key = env("token_key")
            
            #git creds
            if not env("git_url"):
                print ("Git URL is empty")
            else:
                read_env_file.git_url = env("git_url")
            
            #mysql credentials
            if not env("mysql_host"):
                print ("MySQL Host is empty")
            else:        
                read_env_file.mysql_host = env("mysql_host")
                
            if not env("mysql_username"):
                print ("MySQL Host is empty")
            else:        
                read_env_file.mysql_username = env("mysql_username")
                
            read_env_file.mysql_pass = env("mysql_pass")
            
            if not env("mysql_dbname"):
                print ("MySQL Database in .env is empty")
            else:        
                read_env_file.mysql_dbname = env("mysql_dbname")
        
read_env_file()

def zipcommand_ex(token_key):
    zf = zipfile.ZipFile(hidden_room.path + token_key + ".zip", 'w', zipfile.ZIP_DEFLATED)

    for dirname, subdirs, files in os.walk(values.directory_location):

        if '.hidden_room' in subdirs:
            subdirs.remove('.hidden_room')
        if '.git' in subdirs:
            subdirs.remove('.git')
        if '.env' in files:
            files.remove('.env')

        zf.write(dirname)
        for filename in files:
            zf.write(os.path.join(dirname, filename))
            
    zf.close()

def git_init():
    clone = ("git clone " + read_env_file.git_url + " " + values.directory_location + "/.hidden_room")
    print (clone)  
    os.system (clone) # Cloning


def git_run():
    git_run.git_addfiles = ("git add .")
    git_run.git_commit = ("git commit -m 'initial commit'")
    git_run.git_push = ("git push --repo " + read_env_file.git_url)
git_run()

def hidden_room():
    hidden_room.path = values.directory_location + "/.hidden_room/"

    #check if .hidden_room exists    
    if not (os.path.isdir(hidden_room.path)):
        # create folder
        os.mkdir(hidden_room.path)
        print ("creating folder")
        git_init()
        
        #check if files inside .hidden_room exists
        if not (os.path.exists(hidden_room.path + "/" + read_env_file.token_key + ".zip")):
            #if not
            # archive the dir to token_key
            zipcommand_ex(read_env_file.token_key) 

        else:
            #if exist
            os.remove(hidden_room.path + read_env_file.token_key + ".db")

            # archive the dir to token_key
            zipcommand_ex(read_env_file.token_key) 

        if not (os.path.exists(hidden_room.path + read_env_file.token_key + ".db")):
            #if not
            #take DB backup to token_key
            mysqldump = ("mysqldump -h " + read_env_file.mysql_host + " -u " + read_env_file.mysql_username + " -p'" + read_env_file.mysql_pass + "' " + read_env_file.mysql_dbname + " > " + hidden_room.path + read_env_file.token_key + ".db")
            os.system(mysqldump)
            
            #Git add + commit -m + push
            os.chdir(hidden_room.path)
            os.system(git_run.git_addfiles)
            os.system(git_run.git_commit)
            os.system(git_run.git_push)
        else:
            os.remove(hidden_room.path + read_env_file.token_key + ".db")

            #take DB backup to token_key
            mysqldump = ("mysqldump -h " + read_env_file.mysql_host + " -u " + read_env_file.mysql_username + " -p'" + read_env_file.mysql_pass + "' " + read_env_file.mysql_dbname + " > " + hidden_room.path + read_env_file.token_key + ".db")
            os.system(mysqldump)
            
            #Git add + commit -m + push
            os.chdir(hidden_room.path)
            os.system(git_run.git_addfiles)
            os.system(git_run.git_commit)
            os.system(git_run.git_push)
            
    else:
        #check if files inside .hidden_room exists
        if not (os.path.exists(hidden_room.path + read_env_file.token_key + ".zip")):
            #if not

            # archive the dir to token_key
            zipcommand_ex(read_env_file.token_key)            
            
        else:
            #if exist
            os.remove(hidden_room.path + read_env_file.token_key + ".zip")

            # archive the dir to token_key
            zipcommand_ex(read_env_file.token_key) 
            
        if not (os.path.exists(hidden_room.path + read_env_file.token_key + ".db")):
            #if not
            #take DB backup to token_key
            mysqldump = ("mysqldump -h " + read_env_file.mysql_host + " -u " + read_env_file.mysql_username + " -p'" + read_env_file.mysql_pass + "' " + read_env_file.mysql_dbname + " > " + hidden_room.path + read_env_file.token_key + ".db")
            os.system(mysqldump)
            
            #Git add + commit -m + push
            os.chdir(hidden_room.path)
            os.system(git_run.git_addfiles)
            os.system(git_run.git_commit)
            os.system(git_run.git_push)
            
        else:
            os.remove(hidden_room.path + read_env_file.token_key + ".db")
            
            #take DB backup to token_key
            mysqldump = ("mysqldump -h " + read_env_file.mysql_host + " -u " + read_env_file.mysql_username + " -p'" + read_env_file.mysql_pass + "' " + read_env_file.mysql_dbname + " > " + hidden_room.path + read_env_file.token_key + ".db")
            os.system(mysqldump)
            
            #Git add + commit -m + push
            os.chdir(hidden_room.path)
            os.system(git_run.git_addfiles)
            os.system(git_run.git_commit)
            os.system(git_run.git_push)


hidden_room()