import subprocess
from shutil import copyfile
import sys
import re
import socket 
import datetime

two_d_array = []
nbr_netcards = 0
rows_count = 1

def printMessage(s):
  print("--------------------------------------------------------")
  print("   ", s)
  print("--------------------------------------------------------")

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def addToNetworkFile(line):
  with open("networkData.txt", "a") as myfile:
    myfile.write(line+"\n")

def addToLogFile(line):
  with open("logData.txt", "a") as myfile:
    myfile.write(line+"\n")

def parseHeader(s):
    global two_d_array
    global nbr_netcards
    global rows_count
    # count the first row columns (equals network cards)
    nbr_netcards = count_cols(s)
    #print(nbr_netcards)
    #print(s)
    two_d_array = [[0 for j in range(nbr_netcards*2)] for i in range(rows_count)]
    for i in range(nbr_netcards):
        two_d_array[0][i] = s[11:28].strip() + "|kbps_in"
        two_d_array[0][i+1] = s[11:28].strip() + "|kbps_out"
    #print(two_d_array)
    #exit()

def count_cols(s):
     s2 = s.split()
     return len(s2) - 1

def extract_line(s):
  s = re.sub('\x1b[^m]*m', '', s)
  s = re.sub(r'\x1b\[([0-9,A-Z]{1,2}(;[0-9]{1,2})?(;[0-9]{3})?)?[m|K]?', '', s)
  sep = re.compile('[\s]+')
  s = sep.split(s)
  return s


def parseLine(s):
     #addToLogFile(s)
     print(s)
     exit()
     return (s[0:8].strip() + '|' + \
     s[11:19].strip() + '|' + \
     s[20:28].strip() + '|' + \
     s[31:38].strip() + '|' + \
     s[40:48].strip() + '|' + \
     s[51:58].strip() + '|' + \
     s[60:68].strip() + '|' + \
     s[71:78].strip() + '|' + \
     s[80:88].strip() + '|' + \
     s[91:98].strip() + '|' + \
     s[100:108].strip() + '').replace("\n","")

def GetIfStat():
    global two_d_array
    global nbr_netcards
    # Get running containers
    command = ['ifstat', '-bt']
    process = subprocess.Popen(command, stdout=subprocess.PIPE)

    # header 1
    l1 = process.stdout.readline().decode('utf-8')
    parseHeader(l1)

    # header 2
    l2 = process.stdout.readline().decode('utf-8')
    #print("l2 = " + l2)
    #exit()
    #parseLine(l2)

    try:
        while(True):
           s = process.stdout.readline().decode('utf-8')
           #addToLogFile(s)
           if (s.find("Time") != -1 or  s.find("HH:MM") != -1):
              continue
           #data = parseLine(s)
           data = extract_line(s)
           data = data[:-1]
           #print(data)
           new_row = socket.gethostname() + "|" + (datetime.datetime.now()).strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
           for j in range(0,nbr_netcards*2,2):
              new_row = socket.gethostname() + "|" + (datetime.datetime.now()).strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
              val = data[j+1]
              val = data[j+2]

              #print(data[j+1])
              new_row = new_row + "|" + two_d_array[0][j] + "|" + data[j+1]
              #print(new_row)
              addToNetworkFile(new_row)
              new_row = socket.gethostname() + "|" + (datetime.datetime.now()).strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
              new_row = new_row + "|" + two_d_array[0][j+1] + "|" + data[j+2]
              #print(new_row)
              #print(new_row)
              addToNetworkFile(new_row)
    except KeyboardInterrupt:
        pass
    process.terminate()
    return

printMessage("Calling GetIfStat()")
GetIfStat()




    # print network cards
    #print("network cards = ", count_cols(s))
    # print whole row for fun
    #print(s)
    # for i in range(len(two_d_array)):
    #    for j in range(len(two_d_array[i])):
    #       print(two_d_array[i][j])
    #  Time           eth0              docker0         docker_gwbridge     br-38f536ce9fd0       veth56b7b43
    #1234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890
#if not is_number(val):
 #print(s)
 #print(val)
 #exit()
#if not is_number(val):
 #print(s)
 #print(val)
 #exit()
