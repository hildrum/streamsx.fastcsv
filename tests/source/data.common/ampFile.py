#!/usr/bin/env python
import getopt,sys,gzip;


def createFile(base,repeats,headerlines=0):
    if (headerlines == 0):
        outfile=base+str(repeats)+'.csv'
    else:
        outfile=base+str(repeats)+'h'+str(headerlines)+'.csv'
    createFileRaw(base+'.base',outfile,repeats,headerlines)

def createFileRaw(infile,outfile,repeats,headerlines=0):
    out = open(outfile, "w")
    for i in range (headerlines):
        out.write('# infile: '+infile+' repeats ' + str(repeats) + ' header line ' +str(i)+'\n')
    for i in range(repeats):
        with open(infile, "r") as messages:
           for m in messages:
              if "#" not in m:
                 out.write(m);
    out.close();

def createGzipFile(base,repeats,headerlines=0):
    if (headerlines >0):
        outfilename = base+str(repeats)+'h'+str(headerlines)+'.csv.gz'
    else:
        outfilename=base+str(repeats)+'.csv.gz'
    out = gzip.open(outfilename,'wb')
    for i in range (headerlines):
        out.write('# base: '+base+' repeats ' + str(repeats) + ' header line ' +str(i)+'\n')
    for i in range (repeats):
        with open(base+'.base','r') as messages:
            for m in messages:
                if "#" not in m:
                    out.write(m);
    out.close();

def main(argv):
    replays = 2
    infile = "in.txt"
    outfile = "out.txt"
    options, extras = getopt.getopt(argv,'i:o:r:',['infile=','outfile=','repeats'])
    for o, a in options:
        if o in ('-i','--infile'):
            infile = a
        elif o in ('-o','--outfile'):
            outfile = a
        elif o in ('-r','--repeats'):
            replays= int(a)
        else: 
            assert False, "unhandled option"
    createFileRaw(infile,outfile,replays,0)

if __name__ == "__main__":
    main(sys.argv[1:])
