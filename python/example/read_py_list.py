#!/usr/bin/env python

import os
import sys

class GetOptions:
    def __init__(self):
        from optparse import OptionParser
        self.parser = OptionParser()
        self.parser.add_option("-i", "--input", dest="input_file", help="input list file", metavar="FILE")
        options, args = self.parser.parse_args()

        if not options.input_file:
            self.parser.error("-i File is required")

        if not os.path.isfile(options.input_file):
            print "{} doesn't exist".format(options.input_file)
            sys.exit(2)

        self.input_file = os.path.abspath(options.input_file)

    def inputFile(self):
        return self.input_file

class ReadList:
    def __init__(self, input_file):
        self.path = os.path.dirname(input_file)
        sys.path.append(self.path)
        self.list = __import__(os.path.basename(input_file[:-2]))

    def showIP(self):
        if self.list.__dict__.has_key('ue_list'):
            for k, v in self.list.ue_list.items():
                print "testbed: {}\tip: {}".format(k, v['client_ip'])
        elif self.list.__dict__.has_key('ap_list'):
            for k, v in self.list.ap_list.items():
                print "testbed: {}\tip: {}".format(k, v['ap_ip'])
        else:
            print "format error"

def main():
    l = ReadList(GetOptions().inputFile())
    l.showIP()

if __name__ == '__main__':
    main()
