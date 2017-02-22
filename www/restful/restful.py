import web
import lan
urls = ('/api/userdata/.*', 'userdata')


#class weekdata:
#	def GET(self):
		
class userdata:
	def GET(self):
		user = web.ctx.path.split('/')[-1]
		return lan.getweek('304', user, 1) 

app = web.application(urls, globals())
application = app.wsgifunc()

if __name__ == "__main__":
	app.run()
