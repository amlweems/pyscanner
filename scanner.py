import requests
import base64
import re
import xml.etree.ElementTree as ElementTree

job_request = """<scan:ScanJob xmlns:scan="http://www.hp.com/schemas/imaging/con/cnx/scan/2008/08/19" xmlns:dd="http://www.hp.com/schemas/imaging/con/dictionaries/1.0/">
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
</scan:ScanJob>"""

def status(ip='10.10.2.5'):
	url = "http://{0}/Scan/Status".format(ip)
	r = requests.get(url)
	try:
		t = ElementTree.fromstring(r.content)
		return (t.getchildren()[0].text == 'Idle')
	except Exception as e:
		print e
		return False

def recent_job(ip='10.10.2.5'):
	url = "http://{0}/Jobs/JobList".format(ip)
	r = requests.get(url)
	try:
		t = ElementTree.fromstring(r.content)
		elements = [i.getchildren() for i in t.getchildren()]
		job = 0
		for i in elements:
			print i[0].text, i[2].text
			if i[2].text != "Completed":
				numbers = re.findall("\d+", i[0].text)
				if len(numbers):
					if numbers[0] > job:
						job = numbers[0]
		return job
	except Exception as e:
		print e
		return 0

def start_job(ip='10.10.2.5'):
	url = "http://{0}/Scan/Jobs".format(ip)
	r = requests.post(url, data=job_request)
	job = recent_job(ip)
	return job

def scan(ip='10.10.2.5',file='scan.pdf'):
	job = start_job(ip)
	print job
	url = "http://{0}/Scan/Jobs/{1}/Pages/1".format(ip, job)
	r = requests.get(url)
	if r.status_code == 200:
		open(file,'w').write(r.content)

if __name__ == "__main__":
	print status()
	scan()