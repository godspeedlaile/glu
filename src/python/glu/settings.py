"""
Settings for Glue.

"""

VERSION         = "0.9"

DOCUMENT_ROOT   = "/"
PREFIX_META     = "/meta"
PREFIX_CODE     = "/code"
PREFIX_RESOURCE = "/resource"
PREFIX_STATIC   = "/static"

LISTEN_PORT     = 8001

STATIC_LOCATION     = "static_files/"
RESOURCEDB_LOCATION = "resourceDB/"
STORAGEDB_LOCATION  = "storageDB/"
ROOT_DIR            = None

def set_root_dir(rootdir):
    global ROOT_DIR
    if not rootdir.endswith("/"):
        rootdir += "/"
    ROOT_DIR = rootdir

def get_root_dir():
    return ROOT_DIR

NEVER_HUMAN   = False

HTML_HEADER = """
<html>
    <head>
        <title>MuleSoft Glu</title>

        <style type="text/css"> 
        
            p {
                color:#000;
            }
            
            h1 {
                font-weight:bold;
                font-size:2em;
            }
            
            h2 {
                font-weight:bold;
                font-size:1.5em;;
            }
        
            hr {
                height: 1px;
                background:#bbb;
                margin:20px 0px;
            }
        
            table {
                border: 1px solid #fff;
                color:#222;
            }

            td.dict {
                padding:2px 4px;
                background-color:#e5e6e3;
                border: 1px solid #fff;
                color:#aaa;
            }

            td.key {
                padding:2px 4px;
                background-color:#f3f4f2;
                border: 1px solid #fff;
                color:#334;
            }
            
            td {
                padding:2px 4px;
                background-color:#f3f4f2;
                border: 1px solid #fff;
            }
            
            a { 
                color: #016C96; 
            }

            body {
                font-family:Helvetica, Arial, Verdana, sans-serif;
                color:#222;
                font-size:1em;
            }
                
            a:link, a:visited, a:active {
                text-decoration: none; 
            }
            
            a:hover { 
                text-decoration: underline; 
            }

            span.string {
                font-family:Times, "Times New Roman", serif;
                font-style:italic;
            }
        </style> 

    </head>
    <body>
        <h2>Glu</h2>
        <hr>
"""

HTML_FOOTER = """
<hr>
<center><img src="/static/glu/images/logo-mule-s.png" alt="MuleSoft" /></center>
</body>
</html>
"""
