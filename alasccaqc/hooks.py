#!/usr/bin/env python
""" MultiQC hook functions - we tie into the MultiQC
core here to add in extra functionality. """

from __future__ import print_function
from collections import OrderedDict
import logging
import os
import re
import yaml
import multiqc
from multiqc.utils import report, config

log = logging.getLogger('multiqc')

report.ngi = dict()


# def set_sample_status():
#     print("zxcasd")


# HOOK CLASS AND FUNCTIONS
class set_sample_status():

    def __init__(self):
        pass
        # Add code here to set sample pass/fail status based on data from
        # * hzconcordance
        # * coverage in alascca regions