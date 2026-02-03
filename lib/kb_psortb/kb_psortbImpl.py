# -*- coding: utf-8 -*-
#BEGIN_HEADER
import logging
import os

import subprocess
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
    GIT_COMMIT_HASH = "f01cf7f015c5ec7f2b2eb25d63cf07bca4a69d40"

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

        dfu_get_result = self.dfu.get_objects({'object_refs': [f'{params["workspace_id"]}/{params["input_genome"]}']})

        # print(dfu_get_result['data'][0])
        print(dfu_get_result['data'][0]['data'].keys())

        genome_object = dfu_get_result['data'][0]['data']

        features = {}

        for f in genome_object['features']:
            protein_translation = f.get('protein_translation')
            feature_id = f['id']
            if protein_translation:
                if feature_id not in features:
                    features[feature_id] = protein_translation
                else:
                    raise ValueError('Duplicate feature id:', feature_id)

        with open('/tmp/input_genome.faa', 'w') as fh:
            for i, s in features.items():
                fh.write(f'>{i}\n')
                fh.write(f'{s}\n')

        print('/tmp/input_genome.faa created')

        org_type = '-n'

        # Build cmd
        cmd = [
            '/usr/local/psortb/bin/psortx',
            org_type,
            '-o', 'long',
            '--outfile', '/tmp/results.tsv',
            '--seq', '/tmp/input_genome.faa'
        ]
        print(' '.join(cmd))

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True
        )

        print(result)

        print(result.returncode)
        print(result.stdout.strip() if result.stdout else '')
        print(result.stderr.strip() if result.stderr else '')

        if os.path.exists('/tmp/results.tsv'):
            with open('/tmp/results.tsv', 'r') as fh:
                print(fh.read())

        report = KBaseReport(self.callback_url)
        report_info = report.create({'report': {'objects_created': [],
                                                'text_message': params['input_genome']},
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

    def annotate_proteins(self, ctx, proteins, org_param):
        """
        :param proteins: instance of mapping from String to String
        :param org_param: instance of String
        :returns: instance of String
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN annotate_proteins

        with open('/tmp/input_genome.faa', 'w') as fh:
            for i, s in proteins.items():
                fh.write(f'>{i}\n')
                fh.write(f'{s}\n')

        # Build cmd
        cmd = [
            '/usr/local/psortb/bin/psortx',
            org_param,
            '-o', 'long',
            '--outfile', '/tmp/results.tsv',
            '--seq', '/tmp/input_genome.faa'
        ]
        print(' '.join(cmd))

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True
        )

        print(result)

        print(result.returncode)
        print(result.stdout.strip() if result.stdout else '')
        print(result.stderr.strip() if result.stderr else '')

        returnVal = ""

        if os.path.exists('/tmp/results.tsv'):
            with open('/tmp/results.tsv', 'r') as fh:
                returnVal = fh.read()

        #END annotate_proteins

        # At some point might do deeper type checking...
        if not isinstance(returnVal, str):
            raise ValueError('Method annotate_proteins return value ' +
                             'returnVal is not type str as required.')
        # return the results
        return [returnVal]
    def status(self, ctx):
        #BEGIN_STATUS
        returnVal = {'state': "OK",
                     'message': "",
                     'version': self.VERSION,
                     'git_url': self.GIT_URL,
                     'git_commit_hash': self.GIT_COMMIT_HASH}
        #END_STATUS
        return [returnVal]
