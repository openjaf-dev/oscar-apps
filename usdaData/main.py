# -*- coding: utf-8 -*-
'''
Created on 20/11/2014

@author: José Andrés Hernández Bustio
'''
from django.conf import settings

from process_data import ProcessData

def main():
	process_data = ProcessData(settings.REPORT_EXT,settings.REPORT_BASE_URL,settings.REPORT_TYPES,settings.REPORT_FREC,settings.REPORT_PROXIES)
	return process_data.main()