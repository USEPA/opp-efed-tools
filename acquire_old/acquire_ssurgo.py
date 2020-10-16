import pycurl, json

c = pycurl.Curl()
c.setopt(pycurl.URL, 'https://api.box.com/2.0/shared_items')
c.setopt(pycurl.HTTPHEADER, ['Accept: application/json'])
data = json.dumps({"name": "abc", "path": "def", "target": "ghi"})
c.setopt(pycurl.POST, 1)
c.setopt(pycurl.POSTFIELDS, data)
c.setopt(pycurl.VERBOSE, 1)
c.perform()
print curl_agent.getinfo(pycurl.RESPONSE_CODE)
c.close()