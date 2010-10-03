#!/usr/bin/python

def version():
    #Displays author and version information
    print ' Written by Barney_1, AKA. Szczys'
    print ' Maintained by Adam Outler (outleradam at hotmail.com'
    print ' for support, please visit: http://forum.xbmc.org/showthread.php?t=65644'
    print ' This file was written for the mythicalLibrarian project,'
    print ' and is licensed under INSERT LICENSE HERE which allows adaptation.'
    print ' ------------------------------------------------------------------'
    print 'Beta'
    print '  $this utilizes mythtv python bindings to obtain information'
    print '  about a recording and will print the information to a file.'
    print ''
    return


def help():
    #Displays usage information
    print 'Usage:'
    print ' $this --filename=file.ext : returns information to showData.txt'
    print '       --DBHostName        : sets the DB Host, default: localhost'
    print '       --DBName            : sets the DB Name, default: mythconverg'
    print '       --DBUserName        : sets the User Name, default: mythtv'
    print '       --DBPassword        : sets the Password, default, mythtv'
    print '       --output=file.txt   : sets the output, default: ./showdata.txt'
    print '       --version|-v|-ver   : displays version information'
    print ' example:'
    print ' $ $this --filename=1000_20101010101010.mpg --DBHostName=localhost --DBName=mythconverg --DBUserName=mythtv --DBPassword=mythtv --output=/home/myfile.txt'
    print ''
    return

def invalidFile():
    print 'target is not valid.  Please choose a valid target.'
    print 'usage: $this --filename='
    help()

    return


#requires libmyth-python python-lxml
import sys, os

#Setup default database information
dbInfo = {
    "DBHostName" : "localhost",
    "DBName"     : "mythconverg",
    "DBUserName" : "mythtv",
    "DBPassword" : "mythtv"
    }
#Setup default flag information
flags = {
    "auto"       : "False" ,
    "output"     : "./showData.txt",
    "filename"   : "" }
print flags
#A list of valid command line options and flags
validOptions = ['--DBHostName','--DBName','--DBUserName','--DBPassword']
validFlags = [ '--auto', '--output', '--filename', '--version', '-v', '-ver', '--help', '-?' ] #auto flag looks up login from mysql.txt

                
####
#Handle Command Line Arguments
####

#If there were no arguments
if len(sys.argv) < 2:
    sys.exit("Filename must be passed as an argument")

#set the filename variable
filename = sys.argv[1]

#parse through the arguments
if len(sys.argv) > 2:
    #create an argument list without scriptname and filename
    myArgs = sys.argv[1:]
    for arg in myArgs:
        if '=' in arg and arg.split('=')[0] in validOptions:
            #This is a valid option, do something with it
            if arg.split('=')[0][2:] in dbInfo:
                #It's a DB login item, save it in dbInfo
                dbInfo[arg.split('=')[0][2:]] = arg.split('=')[1].replace('"','')
        if '=' in arg and arg.split('=')[0] in validFlags or arg in validFlags:
            #handling for version
            versionFlags = ['-v', '--version', '-ver']
            if arg in versionFlags:
                version()
 	        sys.exit( arg + 'Version information complete.'

            #handling for help switches
            helpFlags = ['-?', '--help']:
            if arg in helpFlags:
                help()
                sys.exit( arg + 'Help information complete.'

        #this is a valid flag, do something
            else: 
                flags[arg.split('=')[0][2:]] = arg.split('=')[1].replace('"','')
                if arg.split('=')[0][2:] in flags:
            #It's a DB login item, save it in flags
                    flags[arg.split('=')[0][2:]] = arg.split('=')[1].replace('"','') 	 	
        else:
            #this is an unacceptable argument, raise an exception
            sys.exit("Invalid command line argument: " + arg)


filename = '1006_20100823173000.mpg'
#!!!!!!!!!!!!!!!!!!!!!!
#!!!!!!!!!!!!!!!!!!!!!!
#EXIT FOR TESTING ONLY
print "Database Information:"
for item in dbInfo:
	print item + " = " + dbInfo[item]
for item in flags:
	print item + " = " + flags[item]
 	

#sys.exit(0)



###############################
#Function: readMysqlTxt
#Arguments: None
#Returns: list of five values:
#  0 or 1 for success or error
#  DBHostName
#  DBName
#  DBUserName
#  DBPassword
#
#Note: Need to add error catching in case file read problems
###############################
def readMysqlTxt():
    #Read database settings from ~/.mythtv/mysql.txt
    mysqlTXT = os.path.expanduser('~') + "/.mythtv/mysql.txt"

    with open(mysqlTXT,'r') as f:
	mysqlData = f.read()
	#Add error handling here... return [1] if error

    lines = mysqlData.split('\n')

    for line in lines:
        line = line.replace(' ','') #strip spaces
        if line.startswith('DBHostName'):
            DBHostName = line.split('=')[1]
        if line.startswith('DBUserName'):
            DBUserName = line.split('=')[1]
        if line.startswith('DBPassword'):
            DBPassword = line.split('=')[1]
        if line.startswith('DBName'):
            DBName = line.split('=')[1]
    return [0,'DBHostName=\''+DBHostName+'\'','DBName=\''+DBName+'\'','\'DBUserName=\''+DBUserName+'\'','\'DBPassword=\''+DBPassword+'\'']


#Get data from mythtv database
'''
from MythTV import MythDB
filename = '1004_20100823003000.mpg'
db = MythDB()
# do some error handling here so we can return a better failure on error
try:
    rec = db.searchRecorded(basename=filename).next()
except StopIteration:
    # thrown when pulling data from an empty iterator
    raise Exception('Recording Not Found')
chanid, starttime = rec.chanid, rec.starttime
print chanid
print starttime
'''


from MythTV import MythDB

print 'Establishing database connection'
try:
 	db = MythDB(DBHostName=dbInfo['DBHostName'], DBName=dbInfo['DBName'], DBUserName=dbInfo['DBUserName'], DBPassword=dbInfo['DBPassword']) 
except: 
	try:
            print 'Failed: attempting to use system default configuration'
 	    db = MythDB() 
        except:
            try:
 	        print 'Failed: attempting to read from default mythtv file'
 	        db = MythDB(readMysqlTxt()) 
            except: 
                print 'Failed: Please specify defaults manually'

#Insert statement if db could not be accessed.



try:
    rec = db.searchRecorded(basename=flags['filename']).next()
except StopIteration:
    raise Exception('Recording Not Found')


#Import all information from database regarding file

'''
#print out data (just for testing)
for x in test.items():
    print x[0] + " = " + str(x[1])
'''

####
#Commercial skip information
####
# gathers all markup into two lists:
# markupstart
# markupstop
####
markup = rec.markup
markupstart = []
markupstop = []


for data in markup:
    if data.type == 4:
        markupstart.append(data.mark)
    if data.type == 5:
        markupstop.append(data.mark)

####
#write data to a text file
####
with open(flags['output'], 'w') as f:
    #iterate through each Recorded() data item and write it to the file
    for x in rec.items():
        f.write(x[0] + " = " + str(x[1]) + "\n")
    f.write("--------FRAME START--------\n")
    for data in markupstart: f.write(str(data) + "\n")
    f.write("--------FRAME STOP---------\n")
    for data in markupstop: f.write(str(data) + "\n")
    f.write("--------END FRAMES---------\n")

if rec.chanid != '':
    print "Operation complete"


