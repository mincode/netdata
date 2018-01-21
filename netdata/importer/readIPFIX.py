import sys
import os
import silk
import tempfile
from subprocess import Popen


def main():
    ipfix_file = sys.argv[1]
    print('File: ' + ipfix_file)
    # create some more random file 
    silk_file = '/tmp/' + ipfix_file + '.rw'
    os.mkfifo(silk_file)
    Popen(['rwipfix2silk', '--silk-output='+silk_file, ipfix_file])

    in_file = silk.silkfile_open(silk_file, silk.READ)
    for rec in in_file:
        print(rec)


if __name__ == '__main__':
    main()

