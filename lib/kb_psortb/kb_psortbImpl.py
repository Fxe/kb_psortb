# -*- coding: utf-8 -*-
#BEGIN_HEADER
import logging
import os

from installed_clients.KBaseReportClient import KBaseReport
from installed_clients.GenomeFileUtilClient import GenomeFileUtil
from installed_clients.DataFileUtilClient import DataFileUtil
#END_HEADER


class kb_psortb:
    '''
    Module Name:
    kb_psortb

    Module Description:
    A KBase module: kb_psortb
    '''

    ######## WARNING FOR GEVENT USERS ####### noqa
    # Since asynchronous IO can lead to methods - even the same method -
    # interrupting each other, you must be *very* careful when using global
    # state. A method could easily clobber the state set by another while
    # the latter method is running.
    ######################################### noqa
    VERSION = "0.0.1"
    GIT_URL = "git@github.com:Fxe/kb_psortb.git"
    GIT_COMMIT_HASH = "cf1484fab5e0e74efdfeeb3aaeb5f8533960d222"

    #BEGIN_CLASS_HEADER
    #END_CLASS_HEADER

    # config contains contents of config file in a hash or None if it couldn't
    # be found
    def __init__(self, config):
        #BEGIN_CONSTRUCTOR
        self.callback_url = os.environ['SDK_CALLBACK_URL']
        self.shared_folder = config['scratch']
        logging.basicConfig(format='%(created)s %(levelname)s: %(message)s',
                            level=logging.INFO)
        self.gfu = GenomeFileUtil(self.callback_url)
        self.dfu = DataFileUtil(self.callback_url)
        #END_CONSTRUCTOR
        pass


    def run_kb_psortb(self, ctx, params):
        """
        This example function accepts any number of parameters and returns results in a KBaseReport
        :param params: instance of mapping from String to unspecified object
        :returns: instance of type "ReportResults" -> structure: parameter
           "report_name" of String, parameter "report_ref" of String
        """
        # ctx is the context object
        # return variables are: output
        #BEGIN run_kb_psortb

        print(params)
        print(ctx)

        # Build cmd
        cmd = [
            '/usr/local/psortb/bin/psortx',
            #species_type,
            #'-o', 'long',
            #'--outfile', f'{job_dir}/results.tsv',
            #'--seq', f'{job_dir}/protein.faa'
        ]
        print(' '.join(cmd))
        import subprocess
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True
        )
        print(result)

        print(result.returncode)
        print(result.stdout.strip() if result.stdout else '')
        print(result.stderr.strip() if result.stderr else '')

        dfu_get_result = self.dfu.get_objects({'object_refs': [params['input_genome']]})

        print(dfu_get_result)

        report = KBaseReport(self.callback_url)
        report_info = report.create({'report': {'objects_created':[],
                                                'text_message': params['parameter_1']},
                                                'workspace_name': params['workspace_name']})
        output = {
            'report_name': report_info['name'],
            'report_ref': report_info['ref'],
        }
        #END run_kb_psortb

        # At some point might do deeper type checking...
        if not isinstance(output, dict):
            raise ValueError('Method run_kb_psortb return value ' +
                             'output is not type dict as required.')
        # return the results
        return [output]
    def status(self, ctx):
        #BEGIN_STATUS
        returnVal = {'state': "OK",
                     'message': "",
                     'version': self.VERSION,
                     'git_url': self.GIT_URL,
                     'git_commit_hash': self.GIT_COMMIT_HASH}
        #END_STATUS
        return [returnVal]
