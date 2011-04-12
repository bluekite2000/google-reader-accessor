#!/usr/bin/env python
from google.appengine.dist import use_library
use_library('django', '1.1')

from xml.dom import minidom
from xml.dom import EMPTY_NAMESPACE
try:
  import json
except ImportError:
  import simplejson as json
import urllib
import urllib2
from django.utils.encoding import smart_str, smart_unicode


username = 'nguyenhdat@gmail.com'
password = ''
header0='<?xml version="1.0" encoding="utf-8"?>'
header1='<feed xmlns="http://www.w3.org/2005/Atom">'
footer='</feed>'
# Authenticate to obtain Auth
auth_url = 'https://www.google.com/accounts/ClientLogin'
auth_req_data = urllib.urlencode({
    'Email': username,
    'Passwd': password,
    'service': 'reader'
    })
auth_req = urllib2.Request(auth_url, data=auth_req_data)
auth_resp = urllib2.urlopen(auth_req)
auth_resp_content = auth_resp.read()
auth_resp_dict = dict(x.split('=') for x in auth_resp_content.split('\n') if x)
AUTH = auth_resp_dict["Auth"]

# Create a cookie in the header using the Auth
header = {'Authorization': 'GoogleLogin auth=%s' % AUTH}

f = open('xmlout.xml','w')
ATOM_NS = 'http://www.w3.org/2005/Atom'
f.write(header0)
f.write(header1)
#reader_base_url = r'http://www.google.com/reader/atom/user%2F-%2Fstate%2Fcom.google%2freading-list?n=50'
reader_base_url = r'http://www.google.com/reader/atom/user/15637521246069684632/state/com.google/reading-list?n=50'

reader_url = reader_base_url
reader_req = urllib2.Request(reader_url, None, header)
reader_resp = urllib2.urlopen(reader_req)
doc = minidom.parse(reader_resp)
doc.normalize()
  
for entry in doc.getElementsByTagNameNS(ATOM_NS, u'entry'):
	title = entry.getElementsByTagNameNS(ATOM_NS, u'title')[0].firstChild.data
	if [True for cat in entry.getElementsByTagNameNS(ATOM_NS, u'category') if cat.getAttributeNS(EMPTY_NAMESPACE, u'term').endswith('/state/com.google/read')]:
		continue
	xmlstr=smart_str(entry.toxml())

	
	f.write(xmlstr)
	
f.write(footer)

f.close()