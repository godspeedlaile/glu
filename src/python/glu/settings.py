"""
Settings for Glue.

"""


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
                font-size:14px;
            }
            
            h1 {
                font-weight:bold;
                font-size:18px;
            }
            
            h2 {
                font-weight:bold;
                font-size:16px;
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

            td {
                padding:4px;
            }

            td.dict {
                padding:2px 4px;
                background-color:#e5e6e3;
                border: 1px solid #fff;
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
            }
                
            a:link, a:visited, a:active {
                text-decoration: none; 
            }
            
            a:hover { 
                text-decoration: underline; 
            }
        </style> 

    </head>
    <body>
        <h2><img src="/static/glu/images/logo-glu.png" alt="Glu <small>(by MuleSoft)" /></h2>
        <hr>
"""

HTML_FOOTER = """
<hr>
<center><small>(c) 2010 by MuleSoft</small></center>
</body>
</html>
"""
