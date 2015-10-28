import sys, os,getopt,shutil
from subprocess import call, Popen, PIPE


class TestFailure(Exception):
   def __init__(self, message,out, err):
      self.message=message
      self.stdout = out
      self.stderr = err

   def say(self, test_name):
      print test_name + ' fail:\n' + \
              '\tmessage: '+self.message +'\n'+\
              '\tstdout: ' + self.stdout + '\n' + \
              '\tstderr: ' + self.stderr + '\n'

def exec_noexit(seq):
   p = Popen(seq, stdout=PIPE, stderr=PIPE)
   stdout, stderr = p.communicate()
   return stdout, stderr, p.returncode

def firstLastNumlines(file,expectedFirst,expectedLast,expectedNumlines):
   (firstline,stderrOne,codeOne) = exec_noexit(['head','-n','1',file]);
   (lastline,stderrTwo,codeTwo) = exec_noexit(['tail','-n','1',file])
   (wcout,stderrThree,codeThree) = exec_noexit(['wc','-l',file])
   (numlines,name)=wcout.split(" ")
   if (firstline.strip() != expectedFirst or lastline.strip() != expectedLast or numlines != str(expectedNumlines) or codeOne != 0 or codeTwo != 0 or codeThree != 0):
       raise TestFailure('First line was '+firstline+'expected '+expectedFirst+\
               'last line was '+lastline+'expected '+expectedLast+\
               'num lines was '+numlines+' expected '+str(expectedNumlines)+\
               'return codes: '+str(codeOne)+' '+str(codeTwo)+' '+str(codeThree),'','')
   else:
       print 'Check of '+file+' succeeded'
