#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  3 10:31:30 2018

@author: BallBlueMeercat

"""

import pickle
import os.path

def save(save_path, output_name, output): 
    # Saving results to run directory.
    filename = output_name+'.p'
    filename = os.path.join(save_path, filename)
    
    pickle.dump(output, open(filename, 'wb'))

    return


def load(save_path, filename):
    
    load_path = os.path.join(save_path, filename)
    
    with open(load_path,'rb') as rfp: 
        content = pickle.load(rfp)
    
    return content

#noise = load('1526030522', 'error.p')
