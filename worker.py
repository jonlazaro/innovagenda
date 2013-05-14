#!/usr/bin/env python

import os
import sys

#Enviroment configuration
os.environ['DJANGO_SETTINGS_MODULE']='settings_prod'

#Get module and functions to call
mod = sys.argv[1]
function_name = sys.argv[2]

#Import module
module = __import__(mod, globals(), locals(), [''])

#Function calling
getattr(module, function_name)()

