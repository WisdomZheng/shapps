def call(version = None, extensions = []):
    '''
    {{use 'bootstraptable',  version='1.9.0', extensions = ["cookie"]}}
    '''
    a = []
    bversion = ''
    if version:
        bversion = 'bootstraptable-%s' % (version)
    else:
        bversion = 'bootstraptable'
    a.append('%s/bootstrap-table.js' % (bversion))
    a.append('%s/bootstrap-table.css' % (bversion))
    css_extensions = ['group-by', 'reorder-rows']
    for ename in extensions:
        a.append('%s/extensions/%s/bootstrap-table-%s.js'%(bversion, ename, ename))
        if ename in css_extensions:
            a.append('%s/extensions/%s/bootstrap-table-%s.css'%(bversion, ename, ename))
        if ename == 'export':
            a.append('%s/extensions/%s/tableExport.js'%(bversion,ename))
    return {'toplinks': a}
