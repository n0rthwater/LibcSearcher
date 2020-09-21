#! /usr/bin/env python3

####################################
# Extract a .so file's symbols info
####################################

import sys
import os

def gen_symbols_file(filename):
    if not filename.endswith('.so'):
        print("Need a .so file!")
        sys.exit(0)
    
    try:
        untreated_symbols_filename = filename[:-3] + '.symbols.untreated'
        symbols_filename = filename[:-3] + '.symbols'

        get_symbols_sh = 'readelf -s %s > %s' % (filename,untreated_symbols_filename)
        print("Execute '%s'" % get_symbols_sh)
        os.system(get_symbols_sh)

        untreadted_fd = open(untreated_symbols_filename,'r')
        fd = open(symbols_filename,'w')
        untreadted_fd.readline()    #If extracted successfully,the first line will be empty.

        if not untreadted_fd.readline().startswith("Symbol"):
            print("Untreadted symbols unstandard.")
            sys.exit(0)
        
        #readelf successfully
        untreadted_fd.readline()
        untreadted_fd.readline()    #Discard the first four line. 
        print("Extract symbols...")
        for eachline in untreadted_fd:
            addr = eachline[8:24]
            func = eachline[59:eachline.find('@')]  #each line endwith a "\r\n"
            fd.write(func + ' ' + addr + '\n')

    except Exception as e:
        print("Exception %s occurred!" % e)
    finally:
        untreadted_fd.close()
        fd.close()
        os.system('rm *.untreated')

def usage():
    print("usage:./extractSymbol.py <so filename>")


if __name__ == "__main__":
    if len(sys.argv) == 1:
        usage()
        sys.exit(0)
    filename = sys.argv[1]
    gen_symbols_file(filename)
