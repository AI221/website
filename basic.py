#License:
#LIABILITY:
#I'm not liable for any damages caused by this software
#USAGE
#Do what you want.

#import pickle;

#I put semicolins at the end of my lines. Deal with it.(the reason is becuase if I don't, I'll forget to do it while programming c++)
from flask import Flask,request,send_file,render_template,g
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



#New forums
#These will work by having unique post nums and board nums.

#SQL:
def get_db():
	sql = getattr(g, 'forumdb', None)
	if sql is None:
		sql = g._database = sq.connect("forumdb")
		return sql


def clrForum():
	sql=get_db()
	c = sql.cursor()
	c.execute("DROP TABLE Posts") 
	c.execute("DROP TABLE Topics")
	c.execute("DROP TABLE Boards")
	c.execute("DROP TABLE Meta")
	c.execute("CREATE TABLE Posts (name TEXT , desc TEXT , time INT , topic INT , id INT)")
	c.execute("CREATE TABLE Topics (name TEXT , desc TEXT, lastpost INT, board INT, id INT)")
	c.execute("CREATE TABLE Boards (name TEXT , desc TEXT, id INT)")
	c.execute("CREATE TABLE Meta ( lastboardid INT ,  lasttopicid INT , lastpostid INT , lastuserid INT )")
	c.close()
	s.commit()
		


@app.route("/forum")
def markisafeegit():
	sql=get_db()
	c = sql.cursor()
	alls = c.execute("SELECT * FROM Boards").fetchall() #SQL STATEMENTS ARE IN CAPITALS TO MAKE THE DATABASE SENSE THE URGENCY AND GO FASTER
	c.close()
	return render_template("forum.html",alls=alls,what="Boards",linkprefix="/viewboard/",linked=True)

@app.route("/viewboard/<board>")
def viewboard(board):
	try:
		board=str(int(board))
	except:
		return render_template("error.html",head="Input error",msg="Board number must be number!")
	sql=get_db()
	c = sql.cursor()
	try:
		alls = c.execute("SELECT * FROM Topics WHERE board = "+board+" ORDER BY lastpost" ).fetchall() #Select from topics where their board number is the corect board number, and order them by time(lastpost should be a unix timestamp of the last post)

	except: #board is empty
		alls = []	
	#get board name
	try:
		boardt = c.execute("SELECT * FROM Boards WHERE Id = "+board).fetchall()[0] #Select the board of the correct ID, which returns a table with a table with the board in it--go to the first thing in that table.
		name = boardt[0] #name is the first thing in the table
		desc = boardt[1] #description is the second
	except:
		name="(failed fetch board name)"
		desc="(failed to fetch board description)"
	c.close()
	return render_template("forum.html",alls=alls,what="Topics for "+name,whatsdesc=desc, linkprefix="/viewtopic/",linked=True,newlink="/newtopic/"+board)

#^ V MERGE


@app.route("/viewtopic/<topic>")
def viewtopic(topic):
	try:
		topic=str(int(topic))	
	except:
		return render_template("error.html",head="Input error",msg="Topic number must be number!")
	sql=get_db()
	c = sql.cursor()
	try:
		alls = c.execute("SELECT * FROM Posts WHERE topic = "+topic+" ORDER BY time" ).fetchall() #Select from posts where their topic number is the corect topic number, and order them by time(time should be a unix timestamp of the last post)

	except: #board is empty
		alls = []	
	#get board name
	try:
		boardt = c.execute("SELECT * FROM Topics WHERE id = "+topic).fetchall()[0] #Select the board of the correct ID, which returns a table with a table with the board in it--go to the first thing in that table.
		name = boardt[0] #name is the first thing in the table
		desc = boardt[1] #description is the second
	except:
		name="(failed fetch topic name)"
		desc="(failed to fetch topic description)"
	c.close()
	return render_template("forum.html",alls=alls,what="Posts for "+name,whatsdesc=desc,linkprefix="/viewtopic/",linked=False,newlink="/newpost/"+topic)

@app.route("/newtopic/<board>",methods=["GET","POST"])
def nTopic(board):
	return newsomething(board,1)



def newsomething(parrent,what):
	if request.method == "GET":
		return render_template("submitforum.html",what="topic",parrent=parrent)
	#if it's post
	title = request.form.get("title")
	body = request.form.get("body")
	try:
		parrent = int(parrent)
	except:
		return render_template("error.html",head="Input error",msg="Parrent number must be number!")

	s=get_db()
	c = s.cursor()
	meta = c.execute("SELECT * FROM Meta").fetchall()[0]
	meta=list(meta)
	c.execute("DELETE FROM Meta")
	meta[what]=meta[what]+1
	if what==0: #parrent
		s()
	elif what==1: #topic
		c.executemany("INSERT INTO Topics VALUES( ?, ?, ? ,?, ? )",[(title,body,-1,parrent,meta[1])])
	elif what==2: #post
		c.executemany("INSERT INTO Posts VALUES( ?, ?, ? ,?, ? )",[(title,body,-1,parrent,meta[2])])

	meta=tuple(meta)
	c.execute("INSERT INTO Meta VALUES(?, ?, ?, ?)",meta)
	c.close()
	s.commit()
	return "dun"
	
	
		
	







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
