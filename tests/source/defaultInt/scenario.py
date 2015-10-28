#!/usr/bin/env python
import sys, os,getopt,shutil
from subprocess import call, Popen, PIPE

def precompile():
    mydir = os.getcwd();
    os.chdir('../data.common')
    if not os.path.isfile('lineNumber100000.csv'):
        print 'File does not exist, creating.'
        sys.path.append(os.getcwd())
        amp = __import__('ampFile')
        amp.main(['-i','lineNumber.base','-o','lineNumber100000.csv','-r','100000'])
        del amp
        del sys.modules['ampFile']
        sys.path.remove(os.getcwd())
    os.chdir(mydir);
    
