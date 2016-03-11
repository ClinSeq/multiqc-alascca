#!/usr/bin/env python

""" SomaticVariants """

from __future__ import print_function
from collections import OrderedDict
import logging

import vcf
from multiqc import config, BaseMultiqcModule

# Initialise the logger
log = logging.getLogger('multiqc')


class MultiqcModule(BaseMultiqcModule):
    """ SomaticVariants """

    def __init__(self):
        # Initialise the parent object
        super(MultiqcModule, self).__init__(name='SomaticVariants', anchor='somaticvariants',
                                            href="",
                                            info="is a module to monitor somatic variants")

        self.sections = list()
        self.somatic_variants_data = dict()
        conf_sp = {'fn': 'freebayes-somatic.vep.vcf.gz'}
        for f in self.find_log_files(conf_sp, filehandles=True):
            self.parse_somatic_variants(f)

        if len(self.somatic_variants_data) == 0:
            log.debug("Could not find any data in {}".format(config.analysis_dir))
            raise UserWarning

        # Write parsed report data to a file
        self.write_data_file(self.somatic_variants_data, 'multiqc_somaticvariants')

        headers = OrderedDict()
        headers['n_somatic_variants'] = {
            'title': 'Num Somatic',
            'description': 'Number of Somatic variants',
            'format': '{:.0f}',
            'scale': 'Blues',
            'min': 0,
        }
        self.general_stats_addcols(self.somatic_variants_data, headers)

        log.info("Found {} reports".format(len(self.somatic_variants_data)))

    def parse_somatic_variants(self, f):
        if f["fn"].endswith("vcf.gz"):
            fname = "{}/{}".format(f['root'], f['fn'])
            vcf_reader = vcf.VCFReader(open(fname, 'rb'))
            for vrec in vcf_reader:
                for call in vrec.samples:
                    if call.gt_type != 0 and call.gt_type is not None:
                        if not call.sample in self.somatic_variants_data:
                            self.somatic_variants_data[call.sample] = {'n_somatic_variants': 0}
                        self.somatic_variants_data[call.sample]['n_somatic_variants'] += 1
