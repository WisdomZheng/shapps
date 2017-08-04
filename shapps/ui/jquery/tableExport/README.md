sample:
=============================
HTML:
-----------------------------
```
<script src="xlsx.core.js"></script>
<script src="FileSaver.js"></script>
<script src="tableexport.js"></script>
```

JS:
-----------------------------
```
//To use this library, simple call the TableExport constructor:
new TableExport(document.getElementsByTagName("table"));

// OR simply
TableExport(document.getElementsByTagName("table"));

// OR using jQuery
$("table").tableExport();

/* Defaults */
TableExport(document.getElementsByTagName("table"), {
    headers: true, // (Boolean), display table headers (th or td elements) in the <thead>, (default: true)
    footers: true, // (Boolean), display table footers (th or td elements) in the <tfoot>, (default: false)
    formats: ['xls', 'csv', 'txt'], // (String[]), filetype(s) for the export, (default: ['xls', 'csv', 'txt'])
    filename: 'id', // (id, String), filename for the downloaded file, (default: 'id')
    bootstrap: false, // (Boolean), style buttons using bootstrap, (default: true)
    exportButtons: true, // (Boolean), automatically generate the built-in export buttons for each of the 
                         // specified formats (default: true)
    position: 'bottom', // (top, bottom), position of the caption element relative to table, (default: 'bottom')
    ignoreRows: null, // (Number, Number[]), row indices to exclude from the exported file(s) (default: null)
    ignoreCols: null, // (Number, Number[]), column indices to exclude from the exported file(s) (default: null)
    trimWhitespace: true // (Boolean), remove all leading/trailing newlines, spaces, and tabs from cell text in 
                         // the exported file(s) (default: false)
});

// Methods: (getExportData, update, reset, remove)
/* First, call the `TableExport` constructor and save the return instance to a variable */
var table = TableExport(document.getElementById("export-buttons-table"));

/* getExportData */
var exportData = table.getExportData(); 

/*****************
 ** exportData ***
 *****************
{
    "export-buttons-table": {
        xls: {
            data: "...",
            fileExtension: ".xls",
            filename: "export-buttons-table",
            mimeType: "application/vnd.ms-excel"
        },
        ...
    }
};
*/

/* update */
table.update({
    filename: "newFile"     // pass in a new set of properties
});

/* reset */
table.reset(); 

/* remove */
table.remove();
```


DOCS:
-----------------------------
```
Introduction: https://tableexport.v4.travismclarke.com/
```