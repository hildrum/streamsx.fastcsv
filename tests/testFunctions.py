#!/usr/bin/env python
import sys, os,getopt,shutil
from subprocess import call, Popen, PIPE
from testCommon import exec_noexit,TestFailure

#class TestFailure(Exception):
#   def __init__(self, message,out, err):
#      self.message=message
#      self.stdout = out
#      self.stderr = err
#   def say(self, test_name):
#      print test_name + ' fail:\n' + \
#      '\tmessage: '+self.message +'\n'+\
#      '\tstdout: ' + self.stdout + '\n' + \
#      '\tstderr: ' + self.stderr + '\n'


#def exec_noexit(seq):
#   p = Popen(seq, stdout=PIPE, stderr=PIPE)
#   stdout, stderr = p.communicate()
#   return stdout, stderr, p.returncode

def precompile():
    return 0

def postrun():
    return

def run(extrarun):
    (run_stdout,run_stderr,run_code) = exec_noexit(['output/bin/standalone']+extrarun)
    if (run_code != 0):
       raise TestFailure("run",run_stdout,run_stderr);


def run_test(dirname,extracompile,extrarun): 
   print "Beginning test "+dirname
   topdir = os.getcwd();
   os.chdir(dirname);
   # Cleanup first.  We don't do this at the end because on failures we'll want to look.
   if os.path.isdir('output'):
      print "output directory found, removing"
      shutil.rmtree('output')
   # see if the data generation file exists.
   if os.path.isfile('scenario.py'):
      sys.path.append(os.getcwd())
      tester = __import__('scenario')
   else: 
      tester = sys.modules[__name__]
   try: 
# any pre-compile steps??
      try:
         tester.precompile()
      except AttributeError:
         precompile()
# compile
      (stdout,stderr,code) = exec_noexit(['sc','-T','-t','../../../com.ibm.streamsx.fastcsv','--data-directory=../data.common','-M','Main']+extracompile);
      if code != 0:
         raise TestFailure("compile",stdout,stderr)
# run
      try:
          tester.run(extrarun)
      except AttributeError:
          run(extrarun);
# check results
      try: 
         tester.postrun()
      except AttributeError:
         postrun()
   except TestFailure as tf:
      tf.say(dirname)
      return False
   finally:
     if os.path.isfile('scenario.py'):
        del tester
        del sys.modules['scenario']
        sys.path.remove(os.getcwd())
     os.chdir(topdir)
   return True

def runDirectory(dir,testlist,compileargs,runargs):
    topdir = os.getcwd();
    os.chdir(dir)
    files = [f for f in os.listdir('.') if (os.path.isdir(f) & ("common" not in f))]
    if len(testlist) > 0:
        files = [f for f in files if f in testlist]
    runall = [(f,run_test(f,['-t','../'+dir+'.common']+compileargs,runargs)) for f in files];
    passed = [f for (f,result) in runall if result];
    failed = [f for (f,result) in runall if not result];
    numpassed = len(passed)
    numfailed = len(failed)
    print "Passed: "+str(numpassed)+" Failed: "+str(numfailed)+"\n"
    print "Passed: "+str(passed);
    print "Failed: "+str(failed);

def main(argv):
    options, extras = getopt.getopt(argv,'t:ag',['test:','tracelevel='])
    testlist = [name for (opt,name) in options if opt == '-t']
    compileargs =[]
    runargs=[]
    for (o,a) in options:
        if (o == '-g'):
           compileargs = compileargs +['--cxx-flags=-g'];
        if ('-a' == o):
           compileargs = compileargs + ['-a'];
        if ('--tracelevel' == o):
            runargs=['-t',str(level)]
    exec_noexit(['spl-make-toolkit','-i','source.common'])
    exec_noexit(['spl-make-toolkit','-i','../../com.ibm.streamsx.fastcvs'])
    if (len(extras) == 0):
       runDirectory('source',testlist,compileargs,runargs)
       runDirectory('sink',testlist,compileargs,runargs)
    else:
       runDirectory(extras[0],testlist,compileargs,runargs)

main(sys.argv[1:])

