#!/usr/bin/env python

""" HeterozygoteConcordance """

from __future__ import print_function
from collections import OrderedDict
import logging
from multiqc import config
from multiqc.modules.base_module import BaseMultiqcModule

# Initialise the logger
log = logging.getLogger('multiqc')


class MultiqcModule(BaseMultiqcModule):
    """ HeterozygoteConcordance """

    def __init__(self):
        # Initialise the parent object
        super(MultiqcModule, self).__init__(name='HeterozygoteConcordance', anchor='hzconcordance',
                                            href="",
                                            info="is a tools to monitor tumor/normal identity")

        self.sections = list()
        self.hzconc_data = dict()
        conf_sp = {'contents': 'VARIANTSSAMPLE\tREADSSAMPLE'}
        for f in self.find_log_files(conf_sp, filehandles=True):
            self.parse_hzconcordance_file(f)

        # Write parsed report data to a file
        self.write_data_file(self.hzconc_data, 'multiqc_hzconcordance')

        headers = OrderedDict()
        headers['pct_hz_snp_frac'] = {
            'title': '% conc hzSNPs',
            'description': 'Fraction of Heterozygote SNPs concordant between tumor and normal',
            'scale': 'RdYlGn',
            'format': '{:.1f}%',
            'max': 100,
            'min': 0
        }
        self.general_stats_addcols(self.hzconc_data, headers)
        #self.add_sections()

        if len(self.hzconc_data) == 0:
            log.debug("Could not find any data in {}".format(config.analysis_dir))
            raise UserWarning

        log.info("Found {} reports".format(len(self.hzconc_data)))

    def add_sections(self):
        cats = OrderedDict()
        cats['conc_hz_snps'] = {'name': 'Concordant Hz-SNPs'}
        cats['disco_hz_snps'] = {'name': 'Discordant Hz-SNPs'}
        pconfig = {
            'title': 'Concordant SNPs in between T and N',
        }
        self.sections.append({
            'name': 'Concordant SNPs in between T and N',
            'anchor': 'hzconcordance_num_snps',
            'content': self.plot_bargraph(self.hzconc_data, cats, pconfig)
        })
        #
        # cats = OrderedDict()
        # cats['num_regions_over_target_cov'] = {'name': 'Number of regions over 100x coverage'}
        # cats['num_regions_under_target_cov'] = {'name': 'Number of regions under 100x coverage'}
        # pconfig = {
        #     'title': 'Regions over minimum coverage',
        # }
        # self.sections.append({
        #     'name': 'Number of target regions over minimum coverage (100x)',
        #     'anchor': 'alascca_num_regions_over_min_cov',
        #     'content': self.plot_bargraph(self.hzconc_data, cats, pconfig)
        # })

    def parse_hzconcordance_file(self, f):
        fh = f['f']
        for l in fh:
            if "VARIANTSSAMPLE" in l.strip():
                header = l.replace("#", "").strip().split("\t")
            else:
                # VARIANTSSAMPLE
                # READSSAMPLE
                # TOTAL_SNPS
                # HZ_SNP_COUNT
                # CONCORDANT_HZ_SNP_COUNT
                # CONCORDANT_HZ_SNP_FRACTION
                elements = l.strip().split("\t")
                variants_s_name = elements[0]
                reads_s_name = elements[1]
                s_name = "{}-{}".format(reads_s_name, variants_s_name)
                self.hzconc_data[s_name] = {}
                self.hzconc_data[s_name]["total_snps"] = int(elements[2])
                self.hzconc_data[s_name]["hz_snps"] = int(elements[3])
                self.hzconc_data[s_name]["conc_hz_snps"] = int(elements[4])
                self.hzconc_data[s_name]["disco_hz_snps"] = self.hzconc_data[s_name]["hz_snps"] - \
                                                            self.hzconc_data[s_name]["conc_hz_snps"]
                try:
                    self.hzconc_data[s_name]["conc_hz_snp_frac"] = float(elements[5])
                    self.hzconc_data[s_name]["pct_hz_snp_frac"] = 100*float(elements[5])
                except ValueError:
                    self.hzconc_data[s_name]["conc_hz_snp_frac"] = 0
                    self.hzconc_data[s_name]["pct_hz_snp_frac"] = 0

                if s_name is not None:
                    self.add_data_source(f, s_name)
