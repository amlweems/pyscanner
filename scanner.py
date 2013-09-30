import requests
import base64
import re

job_request = base64.b64decode("PHNjYW46U2NhbkpvYiB4bWxuczpzY2FuPSJodHRwOi8vd3d3LmhwLmNvbS9zY2hlbWFzL2ltYWdpbmcvY29uL2NueC9zY2FuLzIwMDgvMDgvMTkiIHhtbG5zOmRkPSJodHRwOi8vd3d3LmhwLmNvbS9zY2hlbWFzL2ltYWdpbmcvY29uL2RpY3Rpb25hcmllcy8xLjAvIj48c2NhbjpYUmVzb2x1dGlvbj4zMDA8L3NjYW46WFJlc29sdXRpb24+PHNjYW46WVJlc29sdXRpb24+MzAwPC9zY2FuOllSZXNvbHV0aW9uPjxzY2FuOlhTdGFydD4wPC9zY2FuOlhTdGFydD48c2NhbjpZU3RhcnQ+MDwvc2NhbjpZU3RhcnQ+PHNjYW46V2lkdGg+MjU1MDwvc2NhbjpXaWR0aD48c2NhbjpIZWlnaHQ+MzMwMDwvc2NhbjpIZWlnaHQ+PHNjYW46Rm9ybWF0PlBkZjwvc2NhbjpGb3JtYXQ+PHNjYW46Q29tcHJlc3Npb25RRmFjdG9yPjI1PC9zY2FuOkNvbXByZXNzaW9uUUZhY3Rvcj48c2NhbjpDb2xvclNwYWNlPkdyYXk8L3NjYW46Q29sb3JTcGFjZT48c2NhbjpCaXREZXB0aD44PC9zY2FuOkJpdERlcHRoPjxzY2FuOklu")

def status(ip='10.10.2.5'):
	url = "http://{0}/Scan/Status".format(ip)
	r = requests.get(url)
	try:
		t = ElementTree.fromstring(r.content)
		return (t.getchildren()[0] == 'Idle')
	except:
		return False

def recent_job(ip='10.10.2.5'):
	url = "http://{0}/Jobs/JobList".format(ip)
	r = requests.get(url)
	try:
		t = ElementTree.fromstring(r.content)
		elements = [i.getchildren() for i in t.getchildren()]
		job = 0
		for i in elements:
			if i[2].text != "Completed":
				numbers = re.findall("\d+", i[0].text)
				if len(numbers):
					if numbers[0] > job:
						job = num
		return num
	except:
		return 0

def start_job(ip='10.10.2.5'):
	url = "http://{0}/Scan/Jobs".format(ip)
	r = requests.post(url, data=job_request)
	job = recent_job(ip)
	return job

def scan(ip='10.10.2.5',file='scan.pdf'):
	job = start_job(ip)
	url = "http://{0}/Scan/Jobs/{1}/Pages/1".format(ip, job)
	r = requests.get(url)
	if r.status_code == 200:
		open(file,'w').write(r.content)

if __name__ == "__main__":
	scan()