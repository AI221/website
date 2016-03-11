#License:
#LIABILITY:
#I'm not liable for any damages caused by this software
#USAGE
#Do what you want.

#import pickle;

#I put semicolins at the end of my lines. Deal with it.(the reason is becuase if I don't, I'll forget to do it while programming c++)
from flask import Flask,request,send_file,render_template
app = Flask(__name__)
import sys
import sqlite3 as sq

#cherrypy.config.update({'server.socket_port': 80});
#cherrypy.config.update({"log.access_file":"/tmp/cherrylog"});
#cherrypy.config.update({"log.access_file":"/tmp/cherryerror"});
#cherrypy.config.update({{'/file' : { 'tools.staticdir.on': True , 'tools.staticdir.dir': 'file'} });





#cherrypy.config.update({'log.screen': False,
#                        'log.access_file': '',
#                        'log.error_file': ''})
#^ enable to disable logging

#-----------------------------------------------#
#~~~~~~Website starts, ends, and optionals~~~~~~#
#-----------------------------------------------#
# These are chached and are reset every few seconds




#print(basicSiteHead);


#Functions


def webSafeTxt(stringTo):
	stringTo = str(stringTo);
	return str.replace( str.replace( str.replace(stringTo, '<' , '&lt;'),'>' , '&gt;') , '\n' , '<br>' ); #note: string.replace is depreciated
	#note for source-code viewers: the second < or > should be:    & l t ;    with no spaces.



@app.route("/")
def index():
	return render_template("homepage.html")

@app.route("/aboutme")
def aboutme():
	return render_template("aboutme.html")
@app.route("/geterror/")
def getanerror():
	return "string"-"string"
	










#TO: UNCLEANED CODE
#- - -#
#- - -#
#- | -#
#- - -#
#- - -#
#- | -#
#- - -#
#- - -#
#- | -#
#- - -#
#- - -#
#- | -#
#- - -#
#- - -#




































sources = ["/home/pi/website/basic.py","/home/pi/website/site.conf"];
names = ["the website","the website's site-wide configuration file"];
@app.route('/source',methods=['GET'])
def srcindex(): 
	f=request.args.get('f')

	name = names[int(f)]
	nameC = name[0:1].upper()+name[1:]
	return render_template("sources.html",name=nameC,f=f)
@app.route('/source/htmlr/', methods=['GET'])
def srchtmlr():
	f=request.args.get('f')
	return webSafeTxt(open(sources[int(f)]).read()) 
@app.route('/source/html/', methods=['GET'])
def srchtml():
	f=request.args.get('f')
	return render_template("shtml.html",htmllines = open(sources[int(f)]).read().splitlines()) 

@app.route('/source/file/', methods=['GET'])
def srcfile():
	f=request.args.get('f')
	return send_file(sources[int(f)]) 
@app.route('/source/all/')
def srcall():
	return render_template("allSource.html",names=names)





boards=["Dumb","Dumber","Dumbest"]
cont = [ [], [],[] ]
@app.route('/forum/')
def forumindex():
	#assemble boards
	s = "<h1>Forums</h1><h2>Anyone can post here and there's no cap on the ammount of posts per second. What could go wrong?</h2>"
	i = 0;
	while True:
		s = s+"<h2><a href=\"/forum/viewboard?b=" + str(i) +"\">"+boards[i]+"</a></h2><hr>"
		i = i+1
		if len(boards) == i:
			break;	
	return s
@app.route('/forum/viewboard/',methods=['GET'])
def viewboard():
	b=request.args.get('b')
	#assemble boards
	b=int(b);
	s = "<h1>"+boards[b]+"</h1><p><br><a href=\"/forum/uisubmittopic?b="+str(b)+"\">Submit topic</a></p><hr><br><br>"
	i = -1;
	if len(cont) > b:
		while True:
			i = i+1
			print(i);
			if len(cont[b]) == i:
				break;	
			s = s+"<h2><a href=\"/forum/viewtopic?b=" + str(b) + "&t=" + str(i) +"\">"+webSafeTxt(cont[b][i][0][0])+"</a></h2><hr>"
	
	return s



@app.route('/forum/uisubmittopic/',methods=['GET'])
def uisubmittopic():
	b=request.args.get('b')
	d=request.args.get('d')
	if not d:
		d = "-1";
	postortopic = "post";
	postvars = "<input type=\"text\" name=\"d\" value=\""+d+"\"hidden>";
	if d=="-1":
		postortopic="topic";
		postvars="";

	return "<form method=POST action=\"/forum/submit"+postortopic+"?b="+b+"\"><input type=\"text\" name=\"b\" value=\""+b+"\"hidden>"+postvars+"Topic name:<br><input type=\"text\" name=\"t\"><br>Post contents:<br><input type=\"text\" name=\"p\"><br><input type=\"submit\" value=\"Submit\">"	

	


@app.route('/forum/submitpost',methods=['POST'])
def submitpost():
	b=request.form.get('b')
	t=request.form.get('t')
	p=request.form.get('p')
	d=request.form.get('d')
	if t == "":
		t = "Anyone got some spare change?(Title auto-picked based on position in life)";
	if p == "":
		p = "I'm on the streets and could really use some change, anyone?(Body auto-picked based on position in life)";
	b = int(b);
	d = int(d);
	cont[b][d].append([webSafeTxt(t),webSafeTxt(p)])
	#cont[b][len(cont[b])+1][0][1] = p
	print(cont)
	return "<head><meta http-equiv=\"refresh\" content=\"0; url=viewtopic?b="+str(b)+"&t="+str(d)+"\"/></head>"+bodyStart+"<p>You're somehow still able to use an ancient browser that doesn't support redirecting. I highly recommend you upgrade, but for now, you can sue the back button.</p>" #apparrently they're going to have to take the back button to court

@app.route('/forum/submittopic',methods=['POST'])
def submittopic():
	b=request.form.get('b')
	t=request.form.get('t')
	p=request.form.get('p')
	if t == "":
		t = "Anyone got some spare change?(Title auto-picked based on position in life)";
	if p == "":
		p = "I'm on the streets and could really use some change, anyone?(Body auto-picked based on position in life)";
	b = int(b);
	cont[b].append([[webSafeTxt(t),webSafeTxt(p)]])
	#cont[b][len(cont[b])+1][0][1] = p
	print(cont)
	return "<head><meta http-equiv=\"refresh\" content=\"0; url=viewtopic?b="+str(b)+"&t="+str(len(cont[b])-1)+"\"/></head><p>You're somehow still able to use an ancient browser that doesn't support redirecting. I highly recommend you upgrade, but for now, you can sue the back button.</p>"#apparrently they're going to have to take the back button to court

@app.route('/forum/viewtopic/',methods=['GET'])
def viewtopic():
	t=request.args.get('t')
	#assemble topic
	b=int(b);
	t=int(t);
	s = "<h1>"+webSafeTxt(cont[b][t][0][0])+"</h1><p>"+webSafeTxt(cont[b][t][0][1])+"</p><br><br><a href=/forum/uisubmittopic?b="+str(b)+"&d="+str(t)+">Submit post</a><hr><br><br>"
	if len(cont[b][t]) > 1:
		
		i = 1;
		while True:
			s = s+"<h2><a href=\"/forum/viewtopic?b=" + str(i) +"\">"+webSafeTxt(cont[b][t][i][0])+"</a></h2>"
			s = s+"<p>"+webSafeTxt(cont[b][t][i][1])+"</p><hr"
			i = i+1
			if len(cont[b][t]) == i:
				break;	

	return s 

'''
def error_page_500(status, message, traceback, version):
	return webStart + basicSiteHead + bodyStart + basicSiteNav + "+ bodyEnd + webEnd;
'''
@app.errorhandler(404)
def error_404(err):
	return render_template("error.html",head="404",msg="You've tried to look at a page on my site. Luckily, your eyes are spared, as the page does not exist.")


if __name__ == '__main__':
	port=80
	app.debug=False
	print(sys.argv)
	if len(sys.argv) > 1 and sys.argv[1] == "-d":
		print("***DEBUG MODE***")
		port = 81
		app.debug=True

	app.run(host='0.0.0.0',port=port)
