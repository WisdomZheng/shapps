def call(*args, **kwargs):
    '''
    {{use 'tableExport'}}
    '''
    a = []
    a.append('TableExport/dist/xlsx.core.min.js')
    a.append('TableExport/src/FileSaver.js')
    a.append('TableExport/src/stable/js/tableexport.js')
    a.append('TableExport/src/stable/css/tableexport.css')
    return {'toplinks': a}
