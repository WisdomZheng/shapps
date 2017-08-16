def call(fork=None):
    '''
    {{use 'tableExport'}}
    '''
    a = []
    if fork == "local":
        a.append('local_TableExport/dist/xlsx.core.min.js')
        a.append('local_TableExport/src/FileSaver.js')
        a.append('local_TableExport/src/stable/js/tableexport.js')
        a.append('local_TableExport/src/stable/css/tableexport.css')
    else:
        a.append('TableExport/dist/xlsx.core.min.js')
        a.append('TableExport/src/FileSaver.js')
        a.append('TableExport/src/stable/js/tableexport.js')
        a.append('TableExport/src/stable/css/tableexport.css')
    return {'toplinks': a}
