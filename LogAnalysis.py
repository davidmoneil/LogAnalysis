import argparse, os,sys
__author__='DavidONeil'
parser = argparse.ArgumentParser(description='This is a script by David ONeil : David.ONeil@fishnetsecurity.com. This script will parse through any number of files within a subdirectory and search for specific strings as passed by the --input argument.')
parser.add_argument('-i','--input', help='Text file with Search Terms -one per line (-i toSearch.txt)',required=True)
parser.add_argument('-dir','--directory', help='Select the Directory to Search (-d c:\\test) DEFAULT is working directory',required=False)
parser.add_argument('-o','--output',help='Output file name. example: (-o results) default is results', required=False)
parser.add_argument('-s','--size',help='Input the line size for breaking result files (-b 50000) DEFAULT is 5000', required=False, type=int)
parser.add_argument('-del','--delimiter',help='Delimiter  to use (-del ,) comma is default', required=False)
args = parser.parse_args()

searchArgs = []
rootdir = os.getcwd()
if args.input:
  theSearch = open(args.input, 'r')
else:
  theSearch = open(rootdir + '\\toSearch.txt', 'r')
with theSearch as line:
  searchArgs = [line.strip() for line in theSearch]
  print 'Searching for: ',searchArgs
if args.directory:
  dirSearch = args.directory
else:
  dirSearch = rootdir
print 'Searching the directory: ',dirSearch
if args.output:
  outName = args.output
else:
  outName = 'results.txt'
if args.size:
  outSize = args.size
else:
  outSize = 5000
if args.delimiter:
  sepeartor = args.delimiter
else:
  sepeartor = ','

  #---------------------- Break out the args with ! and put them in a List ------------
#Not In 3D List 
#for i in Array
  #if '!' in i:
    #extract word from between !! example: !Sep! 
# array[0] = Search Term
#array[1] = Search Term 
# array[2] = Not in Line
def getDate(arg):
  import re
  searchObj = re.search( r'(((\d{4}|\d{2}))(-|\/)((0[0-9])|([12])([0-9]?)|(3[01]?))(-|\/)((\d{4})|(\d{2}))|(0?[2469]|11)(-|\/)((0[0-9])|([12])([0-9]?)|(3[0]?))(-|\/)(0?[13578]|10|12))', arg, re.M|re.I)
  if searchObj:
    results = searchObj.group()
    return str(results)
  else:
    return 'NA'

def getIP(arg):
  import re
  searchObj = re.search( r'[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}',arg, re.I)
  if searchObj:
    results = searchObj.group()
    return str(results)
  else:
    return 'NA'

def checkRegEx(arg, reg):
  import re
  #print 'searching ', arg ,'for ', reg
  searchObj = re.search( reg, arg, re.M|re.I)
  if searchObj:
    results = searchObj.group()
    return str(results)


thelist = []

theHeader = []
thelist.append('FileName' + sepeartor + 'SearchTerm' + sepeartor + 'LineNumber' + sepeartor+ 'Date' + sepeartor + 'IP' + sepeartor + 'LineItem')
lineNumb = 1 # this is the line number of the file
lineNumb = int(lineNumb)
theFileNumb = 0
linesPrint = 0
for root, _, files in os.walk(dirSearch):
  for f in files: # Each file in the Directory 
    lineNumb = 1
    fname = os.path.join(root, f) # Set the name and path of the file 
    print 'Opening', fname # Displays name of the file
    theFile = open(fname,'r') # Opens the file
    for line in theFile: # Walks through each line in the file
      lineNumb = lineNumb + 1 # Counts the current line
      if linesPrint >= outSize: #If lines pushed into the array is larger than set limit, dump to file
        theFileNumb = theFileNumb + 1
        print 'the linesPrint', linesPrint , 'was equal to the ourSize', outSize, 'Writing log file to Disk' # check
        theLog = rootdir + '\\'+  str(theFileNumb) + outName + '.txt' # Sets the log name
        writeLog = open(theLog, 'w') # Opens log file
        for item in thelist: # Walks through each item in the array
          writeLog.write(item) #dumps from array to log
          linesPrint = linesPrint + 1 # Increases the for saving logs
        writeLog.close() # Closes the log file
        thelist = [] #Empties the array
        linesPrint = 0 # Resets the number of printed lines back to 1 for log start  
      else: # If the linesPrinted  ins't greater than outSize 
        tick =0
        for arg in searchArgs: # Walk through each of the args passed through -input
          notIn = False
          if '!' in arg:
            notIn = True
          if arg[0:5] == 'regex':
            theReg = arg[6:]
            FindBadness = checkRegEx(line,theReg)
            if FindBadness:
              theDate = getDate(line)
              theIP = getIP(line)
              theLine = (f + sepeartor + FindBadness + sepeartor + str(lineNumb) + sepeartor + theDate + sepeartor + theIP + sepeartor + line) # Format output string
              thelist.append(theLine)
            
          else:
            if '&' in arg:
              print 'Comparing for two or more'
              x = arg.split('&')
              for a in x:
                a.strip()
                if a in line:
                  tick = tick +1
                if tick == len(x):
                  arg.replace('&','-')
                  theDate = getDate(line)
                  theIP = getIP(line)
                  theLine = (f + sepeartor + arg + sepeartor + str(lineNumb) + sepeartor + str(theDate) + sepeartor + str(theIP) + sepeartor + line) # Format output string
                  thelist.append(theLine)
                  linesPrint = linesPrint + 1 # Increas the lines print by one
              tick =0  #no reason to search single item if both ar found
            else: 
              if arg in line: # is the arg found in the line? 
                theDate = getDate(line)
                theIP = getIP(line)
                theLine = (f + sepeartor + arg + sepeartor + str(lineNumb) + sepeartor + str(theDate) + sepeartor + str(theIP) + sepeartor + line)# Format output string
                print 'Writing', theLine # Display
                thelist.append(theLine) # Write to array
                linesPrint = linesPrint + 1 # Increas the lines print by one
                print 'The Lines printed is', linesPrint
    theFile.close() # Close open file to read
if not thelist: # After the all files have been read
  print 'The search returned no results... Sorry - better luck next time'
else: #If the array isn't empty
  print 'Writing log file to disk' # Display
  print 'the lineNumb is ', lineNumb
  theLog = rootdir + '\\'+  str(theFileNumb) + outName + '.txt'
  writeLog = open(theLog, 'w')
  for item in thelist:
    writeLog.write(item)
  writeLog.close()
  thelist = []