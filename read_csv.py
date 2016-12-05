"""
An example of reading a csv file, this one can be used 
to read in the iris data and translate it as defined in the homework writeup

Andy Exley
"""
import sys

def main():
    if len(sys.argv) < 2:
        print('please enter a csv file name as a command-line argument')
        sys.exit(1)

    # get the csv filename from commandline args
    fname = sys.argv[1]
    fp = open(fname, 'r')

    firstline = fp.readline().strip()
    print(firstline)

    for line in fp:
        # split by commas
        vals = line.strip().split(',')

        out = ''
        # iris translation stuff
        plen = float(vals[0])
        pwid = float(vals[1])
        slen = float(vals[2])
        swid = float(vals[3])

        out += sml(plen, 2.5, 4.9)
        out += sml(pwid, 1.7, 1.8)
        out += sml(slen, 6, 7)
        out += sml(swid, 2, 4)
        out += vals[4]
        print(out)

def sml(val, sval, mval):
    if val < sval:
        return 'short,'
    elif val < mval:
        return 'medium,'
    else:
        return 'long,'

if __name__ == '__main__':
    main()
