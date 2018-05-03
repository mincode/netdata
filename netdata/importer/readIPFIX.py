import sys
import os
import silk
from subprocess import Popen
import string
import random

def id_generator(size=8, chars=string.ascii_letters):
    """
    Generate random string.
    size: size of the string to be generated.
    chars: list of letters for the string.
    :return: random string generated.
    """
    L = []
    for _ in range(size):
        L.append(random.choice(chars))
    return ''.join(L)
    # return ''.join(random.choice(chars) for _ in range(size))

def main():
    ipfix_file = sys.argv[1]
    # print('Program: ' + sys.argv[0])
    print('File: ' + ipfix_file)
    # create some more random file 
    silk_file = '/tmp/' + os.path.basename(ipfix_file) + id_generator() + '.rw'
    print('Temporary file: ' + silk_file)
    os.mkfifo(silk_file)
    Popen(['rwipfix2silk', '--silk-output='+silk_file, ipfix_file])
    in_file = silk.silkfile_open(silk_file, silk.READ)
    for rec in in_file:
         print(rec)
         print('======================================================')
    in_file.close()
    os.remove(silk_file)

if __name__ == '__main__':
    main()


