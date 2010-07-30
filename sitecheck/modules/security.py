# -*- coding: utf-8 -*-
import urlparse, urllib, re
import sc_module

xss = re.compile("<xss>", re.IGNORECASE)
eqs = re.compile("(\w+=)(?:&|$)")
attacks = sc_module.get_arg(__name__, 'attacks', [])

def process(request, response):
	if request.source == __name__:
		if response.status >= 500:
			sc_module.OutputQueue.put(__name__, 'Caused error with request: [%s]' % request.url_string)
			if len(request.postdata) > 0:
				sc_module.OutputQueue.put(__name__, '\tPost data: [%s]' % urllib.urlencode(request.postdata))
		elif xss.search(response.content):
			sc_module.OutputQueue.put(__name__, 'Possible XSS found in: [%s]' % request.url_string)
			if len(request.postdata) > 0:
				sc_module.OutputQueue.put(__name__, '\tPost data: [%s]' % urllib.urlencode(request.postdata))
	elif response.is_html:
		document = sc_module.parse(response.content)
		for atk in attacks:
			inject(request, document, atk)
		#inject(request, document, "1'1\'1")
		#inject(request, document, "'';!--\"<xss>=&{()}")

def inject(request, document, value):
	qs = urlparse.parse_qs(request.url.query)
	for param in qs.iterkeys():
		temp = qs[param]
		qs[param] = value
		url = urlparse.urljoin(request.url_string, '?' + urllib.urlencode(qs, True))
		qs[param] = temp
		req = sc_module.Request(__name__, url, request.referrer)
		req.modules = {__name__[8:]: None}
		sc_module.RequestQueue.put(req)

	#Empty query string parameters are not returned by urlparse.parse_qs
	mtchs = eqs.finditer(request.url.query)
	for mtch in mtchs:
		qs = re.sub(mtch.group(0) + '(?:&|$)', mtch.group(0) + value, request.url.query)
		url = urlparse.urljoin(request.url_string, '?' + qs)
		req = sc_module.Request(__name__, url, request.referrer)
		req.modules = {__name__[8:]: None}
		sc_module.RequestQueue.put(req)

	if document:
		postdata = []
		forms = document('form')
		for f in forms:
			url = request.url_string
			post = False
			if ('action' in dict(f.attrs)):
				url = f['action']
			if ('method' in dict(f.attrs)):
				if f['method'].upper() == 'POST': post = True
			params = {}
			inputs = f({'input': True, 'textarea': True, 'select': True})
			for i in inputs:
				if ('name' in dict(i.attrs)):
					params[i['name']] = value

			#Empty request
			req = sc_module.Request(__name__, url, request.referrer)
			req.modules = {__name__[8:]: None}
			sc_module.RequestQueue.put(req)

			if not post:
				if len(urlparse.urlparse(url).query) > 0:
					url = url + '&' + urllib.urlencode(params)
				else:
					url = url + '?' + urllib.urlencode(params)

			req = sc_module.Request(__name__, url, request.referrer)
			if post: req.postdata = params
			req.modules = {__name__[8:]: None}
			sc_module.RequestQueue.put(req)
