#!/usr/bin/env python

"""pyScanner.

Usage:
	scanner.py [<ip>]
	scanner.py (-h | --help | --version)

Options:
	-h --help   Show this screen.
	--version   Show version.
	--ip        IP Address of the printer
"""

from docopt import docopt

import xml.etree.ElementTree as ElementTree
import requests
import base64
import sys
import re

job_request = """
<scan:ScanJob xmlns:scan="http://www.hp.com/schemas/imaging/con/cnx/scan/2008/08/19" xmlns:dd="http://www.hp.com/schemas/imaging/con/dictionaries/1.0/">
	<scan:XResolution>300</scan:XResolution>
	<scan:YResolution>300</scan:YResolution>
	<scan:XStart>0</scan:XStart>
	<scan:YStart>0</scan:YStart>
	<scan:Width>2550</scan:Width>
	<scan:Height>3300</scan:Height>
	<scan:Format>Pdf</scan:Format>
	<scan:CompressionQFactor>25</scan:CompressionQFactor>
	<scan:ColorSpace>Gray</scan:ColorSpace>
	<scan:BitDepth>8</scan:BitDepth>
	<scan:InputSource>Platen</scan:InputSource>
	<scan:GrayRendering>NTSC</scan:GrayRendering>
	<scan:ToneMap>
		<scan:Gamma>1000</scan:Gamma>
		<scan:Brightness>1000</scan:Brightness>
		<scan:Contrast>1000</scan:Contrast>
		<scan:Highlite>179</scan:Highlite>
		<scan:Shadow>25</scan:Shadow>
	</scan:ToneMap>
	<scan:ContentType>Document</scan:ContentType>
</scan:ScanJob>
"""

def status(ip):
	url = "http://{0}/Scan/Status".format(ip)
	r = requests.get(url)
	try:
		t = ElementTree.fromstring(r.content)
		return t.getchildren()[0].text
	except Exception as e:
		raise Exception("Could not parse XML")

def recent_job(ip):
	url = "http://{0}/Jobs/JobList".format(ip)
	r = requests.get(url)
	try:
		t = ElementTree.fromstring(r.content)
		elements = [i.getchildren() for i in t.getchildren()]
		job = 0
		for i in elements:
			if i[2].text == "Completed": continue
			numbers = [int(n) for n in re.findall("\d+", i[0].text)]
			if numbers:
				if numbers[0] > job:
					job = numbers[0]
		return job
	except Exception as e:
		raise Exception("Job Not Found")

def start_job(ip):
	url = "http://{0}/Scan/Jobs".format(ip)
	r = requests.post(url, data=job_request)
	if r.status_code == 201:
		job = recent_job(ip)
		return job
	else:
		raise Exception("Job Not Found")

def scan(ip, file='scan.pdf'):
	job = start_job(ip)
	url = "http://{0}/Scan/Jobs/{1}/Pages/1".format(ip, job)
	print("Scanning...")
	r = requests.get(url)
	if r.status_code == 200:
		open(file, 'wb').write(r.content)
		print("Saved pdf to {0}".format(file))
	else:
		print("Error: Response Code {}".format(r.status_code))

if __name__ == "__main__":
	arguments = docopt(__doc__, version='HP Photosmart 6510 B211a WebScan')
	ip = arguments['<ip>'] if arguments['<ip>'] else '10.10.2.5'
	stat = status(ip)
	if stat == "Idle":
		exit_code = scan(ip)
	else:
		print("Sorry, scanner status is '{0}'".format(stat))
		sys.exit(1)
