/*
A KBase module: kb_psortb
*/

module kb_psortb {
    typedef structure {
        string report_name;
        string report_ref;
    } ReportResults;

    /*
        This example function accepts any number of parameters and returns results in a KBaseReport
    */
    funcdef run_kb_psortb(mapping<string,UnspecifiedObject> params) returns (ReportResults output) authentication required;

    funcdef annotate_proteins(mapping<string,string> proteins, string org_param) returns (string) authentication required;
};
