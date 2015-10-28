#!/usr/bin/env python
import sys, os,getopt,shutil
from subprocess import call, Popen, PIPE

def precompile():
    mydir = os.getcwd();
    os.chdir('../data.common')
    if not os.path.isfile('lineNumber100000h2.csv.gz'):
        print 'File does not exist, creating.'
        sys.path.append(os.getcwd())
        amp = __import__('ampFile')
        amp.createGzipFile('lineNumber',100000,2)
        del amp
        del sys.modules['ampFile']
        sys.path.remove(os.getcwd())
    os.chdir(mydir);
    
