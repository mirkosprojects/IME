#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 21 14:15:00 2021

@authors: kutalmisince and ufukefe
"""

import os

def create_virtual_env(name, directory):

    if not name in os.popen('conda env list').read():       
        os.system('conda env create -f' + os.path.join(directory, 'environment.yml'))
        print(f"conda environment '{name}' was created")