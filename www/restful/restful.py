import web

urls = {'/.*', 'index',}

class index:
	def GET(self):
		return "hello"

app = web.application(urls, globals())
application = app.wsgifunc()

if __name__ == "__main__":
	app.run()
