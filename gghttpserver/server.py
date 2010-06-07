import CGIHTTPServer
import BaseHTTPServer
import sys
from optparse import OptionParser


__usage__ = "\n  %s -P puerto"%sys.argv[0]
parser = OptionParser( usage = __usage__ )
parser.add_option("-P",dest="port", help="puerto",default=8080, type = int)
(params, args) = parser.parse_args()

class Handler(CGIHTTPServer.CGIHTTPRequestHandler):
  cgi_directories = ["/cgi"]


PORT = 8080
httpd = BaseHTTPServer.HTTPServer(("", params.port), Handler)
print "serving at port", params.port
httpd.serve_forever()

