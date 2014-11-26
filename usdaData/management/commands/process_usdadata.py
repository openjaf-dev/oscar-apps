# -*- coding: utf-8 -*-
'''
Created on 17/11/2014

@author: José Andrés Hernández Bustio
'''
import logging
from optparse import make_option

from django.core.management.base import BaseCommand, CommandError
from apps.usdaData.main import main

from oscar.core.loading import get_class
CalculatePrices = get_class('markets.importer', 'CalculatePrices')
USDAImporter = get_class('markets.importer', 'USDAImporter')
USDAImporterror = get_class('markets.exceptions', 'ImportError')

logger = logging.getLogger('oscar.catalogue.import')

class Command(BaseCommand):
    args = '/path/to/file1.csv /path/to/file2.csv ...'
    help = 'Download and processing data from USDA'

    def handle(self, *args, **options):
        file_path = main()
        print file_path
        importer = USDAImporter(
            logger, delimiter='@',
            flush=options.get('flush'))
        logger.info(" - Importing records from '%s'" % file_path)
        try:
            importer.handle(file_path)
        except USDAImporterror, e:
            raise CommandError(str(e))
        logger.info(" - Calculating prices - ")
        CalculatePrices()
        print 'Se ejecuto el comando con exito'

