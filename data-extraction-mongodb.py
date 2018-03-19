#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 27 00:46:38 2018

@author: ReginaGurung
"""

import os

DATADIR = ""
DATAFILE = "beatles-discography.csv"


def parse_file(datafile):
    data = []
    with open(datafile, "r") as f:
        header = f.readline().split(",") # There is no loop here. so this is the first line.
        counter = 0
        for line in f:
            print('*******')
            print(line)
            if counter == 10:
                break
        
            fields = line.split(",")
            print('&&&&&&')
            print(fields)
            entry = {}
        
            for i, value in enumerate(fields):
                print(i, value)
                entry[header[i].strip()] = value.strip()

    return data


def test():
    datafile = os.path.join(DATADIR, DATAFILE)
    d = parse_file(datafile)
    firstline = {'Title': 'Please Please Me', 'UK Chart Position': '1', 'Label': 'Parlophone(UK)', 'Released': '22 March 1963', 'US Chart Position': '-', 'RIAA Certification': 'Platinum', 'BPI Certification': 'Gold'}
    tenthline = {'Title': '', 'UK Chart Position': '1', 'Label': 'Parlophone(UK)', 'Released': '10 July 1964', 'US Chart Position': '-', 'RIAA Certification': '', 'BPI Certification': 'Gold'}

    assert d[0] == firstline
    assert d[9] == tenthline

    
test()