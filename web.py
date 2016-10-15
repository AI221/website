#License:
#LIABILITY:
#I'm not liable for any damages caused by this software
#USAGE
#Do what you want.

import cherrypy;
#from cherrypy.process.plugins import Daemonizer
#d = Daemonizer(cherrypy.engine)
#d.subscribe()
import mimetypes
from cherrypy.lib.static import serve_file

from cherrypy.process import wspbus, plugins
import pickle;

#I put semicolins at the end of my lines. Deal with it.(the reason is becuase if I don't, I'll forget to do it while programming c++)


#cherrypy.config.update({'server.socket_port': 80});
#cherrypy.config.update({"log.access_file":"/tmp/cherrylog"});
#cherrypy.config.update({"log.access_file":"/tmp/cherryerror"});
#cherrypy.config.update({{'/file' : { 'tools.staticdir.on': True , 'tools.staticdir.dir': 'file'} });


cherrypy.config.update('server.conf');



#cherrypy.config.update({'log.screen': False,
#                        'log.access_file': '',
#                        'log.error_file': ''})
#^ enable to disable logging

#-----------------------------------------------#
#~~~~~~Website starts, ends, and optionals~~~~~~#
#-----------------------------------------------#
# These are chached and are reset every few seconds




def refrshChache():
	#starts
	global webStart
	global webEnd
	global bodyStart
	global bodyEnd
	global basicSiteHead
	global basicSiteNav
	global invSiteHead

	print("Refreshing database...");
	webStart = (r'<!DOCTYPE html>'
	r'<html>'
	r'<!--Server-sided Source code availiable on /source, running on CherryPy-->'
	);
	webEnd = (r'</html>');
	bodyStart = r'<body>'
	bodyEnd = r'</body>'
	
	#optionals
	basicSiteHead = r'<head>' + open('/home/pi/website/file/heads/basicSite').read() + r'</head>';
	basicSiteNav = open('/home/pi/website/file/heads/basicSiteNav').read()
	invSiteHead = r'<head>' + open('/home/pi/website/file/heads/inv').read() + r'</head>';
	print(basicSiteHead);


refrshChache();
print(basicSiteHead);

def refrshd():
	refrshChache();	




#Functions


def webSafeTxt(stringTo):
	stringTo = str(stringTo);
	return str.replace( str.replace( str.replace(stringTo, '<' , '&lt;'),'>' , '&gt;') , '\n' , '<br>' ); #note: string.replace is depreciated
	#note for source-code viewers: the second < or > should be:    & l t ;    with no spaces.
class Root(object):
    @cherrypy.expose
    def index(self):
	#cherrypy.log("hello there")
	site = open("/home/pi/website/homepage.html","r").read();
	#refrshChache();
	return webStart + basicSiteHead + bodyStart + basicSiteNav + site + bodyEnd + webEnd;
    @cherrypy.expose
    def test(self,d="<p>test</p>"):
	return webStart + basicSiteHead + bodyStart + basicSiteNav + d + bodyEnd + webEnd;
	
        #return "<p>Hello World!</p>"
	


class SrcCode(object): 
	sources = ["/home/pi/website/basic.py","/home/pi/website/site.conf"];
	names = ["the website","the website's site-wide configuration file"];
	@cherrypy.expose
	def index(self,f="0"): 
		return webStart + basicSiteHead + bodyStart + basicSiteNav + "<p>This a hosting for " + self.names[int(f)] + ". <a href=\"/source/html?f="+str(f)+"\">View</a> <a href=\"/source/htmlr?f="+str(f)+"\">(raw)</a> or <a href=\"/source/file?f="+str(f)+"\">download</a>" + bodyEnd + webEnd;
	@cherrypy.expose
	def htmlr(self,f="0"):
		return webSafeTxt(open(self.sources[int(f)]).read()) #This displays the content on a web page and doesn't work very well	
	@cherrypy.expose
	def html(self,f="0"):
		return webStart + basicSiteHead + bodyStart + basicSiteNav + webSafeTxt(open(self.sources[int(f)]).read()) + bodyEnd + webEnd;

	@cherrypy.expose
	def file(self,f="0"):
		return serve_file(self.sources[int(f)],"application/x-download", "attachment") #This DLs the source code and workls well
	@cherrypy.expose
	def all(self):
		s = "<h1>Files hosted here</h1><p>";
		i = 0;
		while True:
			s = s + "<a href=\"/source?f=" + str(i) + "\">" + self.names[i] + "</a><br>"
			print(i);
			i=i+1;
			if len(self.sources) == i:
				break;
		s = s + "</p>";
		return webStart + basicSiteHead + bodyStart + basicSiteNav + s + bodyEnd + webEnd;





class invObj(object):
	areas = [["A"],["B"]];
	areas[0].append(["Mark's Hair Dirt", "A pickle", "Max Traps"]);
	areas[0].append([1,1,27]);
	areas[1].append(["Golden Carrots", "My free time", "Hax","Ideas","Your IQ",]);
	areas[1].append([24,0,1337,0,2]);
	def areaWebsite(self,area):
		asmStr = "<table><tr><td>Name of Item</td><td>Quantity of Item</td></tr>";
		i = 0;
		while len(self.areas[area][1]) > i:
			#return self.areas[area][1][i]
			asmStr = asmStr +  "<tr><td>"+self.areas[area][1][i]+"</td><td>"+str(self.areas[area][2][i])+"</td></tr>";
			i = i+1
		
		asmStr = asmStr + "</table>"
		

		return webStart + invSiteHead + bodyStart + asmStr + bodyEnd + webEnd;
		

objects =[["test",invObj()],["Brain damblig4",invObj()]]



class InvMan(object):
	@cherrypy.expose
	def index(self):
		area="/home/pi/website/file/inv/pilot"
		
		invSite = open("/home/pi/website/inv.html","r").read();
		return webStart + invSiteHead  + bodyStart +  invSite + bodyEnd + webEnd;
	#	return 						str(objects[0][1].areas[0])# + str(t.getAreas()[1]);
	@cherrypy.expose
	def showClass(self,c=0,s=False):
		if s:
			#return  str(objects[int(c)][1].areas[int(s)])
			return objects[int(c)][1].areaWebsite(int(s));
		else:
			return "yup" + str(objects[int(c)][1].areas)




class DatabasePlugin(plugins.SimplePlugin):
    def __init__(self, bus, db_klass):
        plugins.SimplePlugin.__init__(self, bus)
        self.db = db_klass();

    def start(self):
        self.bus.log('Starting up DB access');
        self.bus.subscribe("db-save", self.save_it);

    def stop(self):
        self.bus.log('Stopping down DB access');
        self.bus.unsubscribe("db-save", self.save_it);

    def save_it(self, entity):
        self.db.save(entity);


class thefile(object):
	@cherrypy.expose
	def index(self):
		return

class forum(object):
	boards=["Dumb","Dumber","Dumbest"]
	cont = [ [], [],[] ]
	@cherrypy.expose
	def index(self):
		#assemble boards
		s = "<h1>Forums</h1><h2>Anyone can post here and there's no cap on the ammount of posts per second. What could go wrong?</h2>"
		i = 0;
		while True:
			s = s+"<h2><a href=\"/forum/viewboard?b=" + str(i) +"\">"+self.boards[i]+"</a></h2><hr>"
			i = i+1
			if len(self.boards) == i:
				break;	
		return webStart + basicSiteHead + bodyStart + basicSiteNav+ s  + bodyEnd + webEnd;
	@cherrypy.expose
	def viewboard(self,b="0"):
		#assemble boards
		b=int(b);
		s = "<h1>"+self.boards[b]+"</h1><p><br><a href=\"uisubmittopic?b="+str(b)+"\">Submit topic</a></p><hr><br><br>"
		i = -1;
		if len(self.cont) > b:
			while True:
				i = i+1
				print(i);
				if len(self.cont[b]) == i:
					break;	
				s = s+"<h2><a href=\"/forum/viewtopic?b=" + str(b) + "&t=" + str(i) +"\">"+webSafeTxt(self.cont[b][i][0][0])+"</a></h2><hr>"
		
		return webStart + basicSiteHead + bodyStart + basicSiteNav+ s  + bodyEnd + webEnd;	



	@cherrypy.expose
	def uisubmittopic(self,b="1",d="-1"):
		postortopic = "post";
		postvars = "<input type=\"text\" name=\"d\" value=\""+d+"\"hidden>";
		if d=="-1":
			postortopic="topic";
			postvars="";

		return webStart + basicSiteHead + bodyStart + basicSiteNav+ "<form action=\"submit"+postortopic+"?b="+b+"\"><input type=\"text\" name=\"b\" value=\""+b+"\"hidden>"+postvars+"Topic name:<br><input type=\"text\" name=\"t\"><br>Post contents:<br><input type=\"text\" name=\"p\"><br><input type=\"submit\" value=\"Submit\">"+ bodyEnd + webEnd;	
		


	@cherrypy.expose
	def submitpost(self,b="0",t="I forgot to put a title because I'm bad",p="I forgot to put a post here cuz i cant grammer",d="0"):
		if t == "":
			t = "Anyone got some spare change?(Title auto-picked based on position in life)";
		if p == "":
			p = "I'm on the streets and could really use some change, anyone?(Body auto-picked based on position in life)";
		b = int(b);
		d = int(d);
		self.cont[b][d].append([webSafeTxt(t),webSafeTxt(p)])
		#self.cont[b][len(self.cont[b])+1][0][1] = p
		print(self.cont)
		return webStart + "<head><meta http-equiv=\"refresh\" content=\"0; url=viewtopic?b="+str(b)+"&t="+str(d)+"\"/></head>"+bodyStart+"<p>You're somehow still able to use an ancient browser that doesn't support redirecting. I highly recommend you upgrade, but for now, you can sue the back button.</p>"+bodyEnd+webEnd; #apparrently they're going to have to take the back button to court
	@cherrypy.expose
	def submittopic(self,b="0",t="I forgot to put a title because I'm bad",p="I forgot to put a post here cuz i cant grammer"):
		if t == "":
			t = "Anyone got some spare change?(Title auto-picked based on position in life)";
		if p == "":
			p = "I'm on the streets and could really use some change, anyone?(Body auto-picked based on position in life)";
		b = int(b);
		self.cont[b].append([[webSafeTxt(t),webSafeTxt(p)]])
		#self.cont[b][len(self.cont[b])+1][0][1] = p
		print(self.cont)
		return webStart + "<head><meta http-equiv=\"refresh\" content=\"0; url=viewtopic?b="+str(b)+"&t="+str(len(self.cont[b])-1)+"\"/></head>"+bodyStart+"<p>You're somehow still able to use an ancient browser that doesn't support redirecting. I highly recommend you upgrade, but for now, you can sue the back button.</p>"+bodyEnd+webEnd; #apparrently they're going to have to take the back button to court
	@cherrypy.expose
	def viewtopic(self,b="0",t="0"):
		#assemble topic
		b=int(b);
		t=int(t);
		s = "<h1>"+webSafeTxt(self.cont[b][t][0][0])+"</h1><p>"+webSafeTxt(self.cont[b][t][0][1])+"</p><br><br><a href=uisubmittopic?b="+str(b)+"&d="+str(t)+">Submit post</a><hr><br><br>"
		if len(self.cont[b][t]) > 1:
			
			i = 1;
			while True:
				s = s+"<h2><a href=\"/forum/viewtopic?b=" + str(i) +"\">"+webSafeTxt(self.cont[b][t][i][0])+"</a></h2>"
				s = s+"<p>"+webSafeTxt(self.cont[b][t][i][1])+"</p><hr>"
				i = i+1
				if len(self.cont[b][t]) == i:
					break;	

		return webStart + basicSiteHead + bodyStart + basicSiteNav+ s  + bodyEnd + webEnd;	

@cherrypy.expose
def error_page_404(status, message, traceback, version):
	return webStart + basicSiteHead + bodyStart + basicSiteNav + "<h1>404</h1><p>You've tried to look at a page on my site. Luckily, your eyes are spared, as the page does not exist.</p>" + bodyEnd + webEnd;

cherrypy.config.update({'error_page.404': error_page_404})

@cherrypy.expose
def error_page_500(status, message, traceback, version):
	return webStart + basicSiteHead + bodyStart + basicSiteNav + "<h1>I dun goofed</h1><p>For once, this isn't your fault, it's mine. Unless you are me. Then it's both of our fault.<br>If you're not sure what to do, try going back, or to the homepage.<br><br><br><hr>Cherrpy version " + version+"<br>Error traceback: "+traceback + bodyEnd + webEnd;

cherrypy.config.update({'error_page.500': error_page_500})





if __name__ == '__main__':
	cherrypy.server.socket_host = '0.0.0.0';
	cherrypy.tree.mount(Root(), '/','site.conf');         #, blog_conf)
	cherrypy.tree.mount(SrcCode(), '/source','site.conf');        #, forum_conf)
	cherrypy.tree.mount(InvMan(), '/inv','site.conf');
	cherrypy.tree.mount(forum(), '/forum','site.conf');
	#cherrypy.process.plugins.BackgroundTask(5,refrshd).run(); #causes this to run in this procsess, not a seperate one
	#cherrypy.tree.mount(thefile(),'/file',
	#cherrypy.tree.mount(thefile(),'/file','site.conf');
	cherrypy.engine.start();
	cherrypy.engine.block();

