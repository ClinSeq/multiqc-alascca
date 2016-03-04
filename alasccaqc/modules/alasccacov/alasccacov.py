#!/usr/bin/env python

""" MultiQC module visualize coverage of core regions in ALASCCA """

from __future__ import print_function
import os
from collections import OrderedDict
import logging
import re
import copy
from multiqc import config, BaseMultiqcModule

# Initialise the logger
log = logging.getLogger('multiqc')


class MultiqcModule(BaseMultiqcModule):
    """ Alascca Coverage """

    def __init__(self):
        # Initialise the parent object
        super(MultiqcModule, self).__init__(name='AlasccaCov', anchor='alasccacov',
                                            href="",
                                            info="is a plugin to visualize coverage and sample identity in the ALASCCA study")

        self.sections = list()
        self.alasccacov_data_dens = dict()
        self.alasccacov_data_count = dict()

        conf_sp = {'contents': '# target_coverage_histogram'}
        for f in self.find_log_files(conf_sp, filehandles=True):
            self.parse_coverage_file(f)

        if len(self.alasccacov_data_dens) == 0:
            log.debug("Could not find any data in {}".format(config.analysis_dir))
            raise UserWarning

        data = {}
        for s_name in self.alasccacov_data_dens:
            pct = 100 * sum([y for x, y in self.alasccacov_data_dens[s_name].items() if x >= 100])
            data[s_name] = {'pct_bases_over_100x': pct}

        # Write parsed report data to a file
        self.write_data_file(self.alasccacov_data_dens, 'multiqc_alascca_coverage_histogram')

        headers = OrderedDict()
        headers['pct_bases_over_100x'] = {
            'title': '% > 100x',
            'description': 'Percent of target bases over 100x',
            'scale': 'RdYlGn',
            'format': '{:.1f}%',
            'max': 100,
            'min': 0
        }
        self.general_stats_addcols(data, headers)

        headers = OrderedDict()
        headers['pct_bases_over_100x'] = {
            'title': '% > 100x',
            'description': 'Percent of target bases over 100x',
            'scale': 'RdYlGn',
            'format': '{:.1f}%',
            'max': 100,
            'min': 0
        }
        self.general_stats_addcols(data, headers)

        self.add_plots()

        log.info("Found {} reports".format(len(self.alasccacov_data_dens)))

    def add_plots(self):
        normalized_cov = copy.deepcopy(self.alasccacov_data_dens)
        for s_name in normalized_cov:
            max_dens = max(y for x, y in normalized_cov[s_name].items())
            for x, y in normalized_cov[s_name].items():
                normalized_cov[s_name][x] = y / max_dens

        pconfig = {
            'id': 'coverage_histogram',
            'title': 'Normalized Coverage Density',
            'xDecimals': False,
            'ylab': 'Normalized Density',
            'xlab': 'Coverage',
            'xmin': 0,
            'ymax': 1,
            'ymin': 0,
            'tt_label': '<b>{point.x}</b>',
        }

        html_content = self.plot_xy_data(normalized_cov, pconfig)

        self.sections.append({
            'name': 'Alascca Targets Coverage Histogram',
            'anchor': 'alascca_bedtools_hist',
            'content': html_content
        })

        barplot_data = {}
        for s_name in self.alasccacov_data_dens:
            bases_under_100x = sum([y for x, y in self.alasccacov_data_count[s_name].items() if x < 100])
            bases_over_100x = sum([y for x, y in self.alasccacov_data_count[s_name].items() if x >= 100])
            barplot_data[s_name] = {'bases_over_100x': bases_over_100x,
                                    'bases_under_100x': bases_under_100x}
        cats = OrderedDict()
        cats['bases_over_100x'] = {'name': 'Number of Bases Over 100x coverage'}
        cats['bases_under_100x'] = {'name': 'Number of Bases Under 100x coverage'}
        pconfig = {
            'title': 'Bases over 100x Coverage',
        }

        self.sections.append({
            'name': 'Alascca Bases Over 100x',
            'anchor': 'alascca_bases_over_100x',
            'content': self.plot_bargraph(barplot_data, cats, pconfig)
        })

        # Only one section, so add to the intro
        # self.intro += html_content

    def parse_coverage_file(self, f):
        fh = f['f']
        name_regex = "#\starget_coverage_histogram,\sbam:\s(\S+)"
        hist_regex = "(\d+)\s+(\d+)\s+(\d+)\s+(\d+\.\d+)"
        s_name = None
        dat_dens = {}
        dat_count = {}
        for l in fh:
            match = re.search(name_regex, l)
            if match:
                s_name = os.path.basename(match.group(1)).replace(".bam", "")
            else:
                match = re.search(hist_regex, l)
                if match:
                    cov = int(match.group(1))
                    count_at_cov = int(match.group(2))
                    dens_at_cov = float(match.group(4))
                    dat_dens[cov] = dens_at_cov
                    dat_count[cov] = count_at_cov

        if s_name is not None:
            self.add_data_source(f, s_name)
            self.alasccacov_data_dens[s_name] = dat_dens
            self.alasccacov_data_count[s_name] = dat_count
