#!/usr/bin/env python
import sys, os,getopt,shutil
from subprocess import call, Popen, PIPE

def precompile():
    mydir = os.getcwd();
    os.chdir('../data.common')
    sys.path.append(os.getcwd())
    amp = __import__('ampFile')
    if not os.path.isfile('lineNumber100000.csv'):
        amp.createFile('lineNumber',100000)
    if not os.path.isfile('lineNumber100.csv'):
        amp.createFile('lineNumber',100);
    if not os.path.isfile('allErrors100000.csv'):
        amp.createFile('allErrors',100000)
    del amp
    del sys.modules['ampFile']
    sys.path.remove(os.getcwd())
    os.chdir(mydir);
    
