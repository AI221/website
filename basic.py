#!/usr/bin/python2
#---------------------------------------------------------#
# License:						  #
# LIABILITY:						  #
# I'm not liable for any damages caused by this software  #
# USAGE							  #
# Do what you want.					  #
#---------------------------------------------------------#


import sys
import getopt
import sqlite3 as sq


##########################
#--Unchanging variables--#
##########################


helpstr = "basic.py -d" 


#############################
#--Command line arguements--#
#############################

#~~Variable defaults~~#
global port
global debug
global ssl_context 
global start 
global maintainance 


port=80
debug=False
ssl_context = None
start = True
maintainance = False 

#~~Changes to them via args~~#

for arg in sys.argv:
	if arg == "-d":
		print("***DEBUG MODE***")
	        port = 8081
        	debug=True
	elif arg == "-https":
		debug=True
		ssl_context = ('/website/cert', '/website/key')
	elif arg == "-c":
		clrForum()
		start = False
	elif arg == "-m":
		print("***MAINTAINANCE MODE***")
		maintainance = True	
	elif arg == "--debug-nostart":
		start = False	
	else:
		print("No such arguement \""+str(arg)+"\"")
		#start = False


print(port)
print(debug)
print(maintainance)
		






###############
#--Functions--#
###############

if start:


	#~~Extra tasks from above that are only needed if starting flask~~#
	from flask import Flask,request,send_file,render_template,g
	app = Flask(__name__)
	#~~~~#

	if maintainance:
		@app.errorhandler(404)
		def error_404(err):
			return render_template("error.html",head="Maintainance mode",msg="Site is in maintainance mode. It should be back eventually.")



	else:
		#Web safe text
		def webSafeTxt(stringTo):
			stringTo = str(stringTo)
			return str.replace( str.replace( str.replace(stringTo, '<' , '&lt;'),'>' , '&gt;') , '\n' , '<br>' ); #note: string.replace is depreciated
			#note for source-code viewers: the second < or > should be:    & l t ;    with no spaces.


	###########
	#--Pages--#
	###########


		@app.route("/")
		def index():
			return render_template("homepage.html")

		@app.route("/aboutme")
		def aboutme():
			return render_template("aboutme.html")
		@app.route("/opengraphpaper")
		def opengraphpaer():
			return render_template("opengraphpaper.html")

		@app.route("/geterror/")
		def getanerror():
			return "string"-"string"

		#might do away with this
		sources = ["/website/basic.py","/website/site.conf"]
		names = ["the website","the website's site-wide configuration file"]
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


		dbname = "/website/forumdb"
		#SQL:
		def get_db():
			sql = getattr(g, dbname, None)
			if sql is None:
				sql = g._database = sq.connect(dbname)
				return sql


		def clrForum():
			sql=sq.connect(dbname)
			c = sql.cursor()
			c.execute("DROP TABLE IF EXISTS Posts") 
			c.execute("DROP TABLE IF EXISTS Topics")
			c.execute("DROP TABLE IF EXISTS Boards")
			c.execute("DROP TABLE IF EXISTS Meta")
			c.execute("CREATE TABLE Posts (name TEXT , desc TEXT , time INT , topic INT , id INT)")
			c.execute("CREATE TABLE Topics (name TEXT , desc TEXT, lastpost INT, board INT, id INT)")
			c.execute("CREATE TABLE Boards (name TEXT , desc TEXT, id INT)")
			c.execute("CREATE TABLE Meta ( lastboardid INT ,  lasttopicid INT , lastpostid INT , lastuserid INT )")
			c.execute("INSERT INTO Meta VALUES ( 0,0,0,0 )")
			c.close()
			sql.commit()
				


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



		@app.route("/newpost/<parrent>",methods=["GET","POST"])
		def newsomething(parrent,what=2):
			if request.method == "GET":
				return render_template("sinput.html",what="Create a topic",parrent=parrent, items=[["Title","text","title"],["Body","text","body"]],buttontxt="Create")
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
			area = ""
			if what==0: #parrent
				s()
			elif what==1: #topic
				c.executemany("INSERT INTO Topics VALUES( ?, ?, ? ,?, ? )",[(title,body,-1,parrent,meta[1])])
				area = "board" #worse is better. could make it redirect to the topic, but this would require a lot more code.
			elif what==2: #post
				c.executemany("INSERT INTO Posts VALUES( ?, ?, ? ,?, ? )",[(title,body,-1,parrent,meta[2])])
				area = "topic"

			meta=tuple(meta)
			c.execute("INSERT INTO Meta VALUES(?, ?, ?, ?)",meta)
			c.close()
			s.commit()
			return render_template("redirect.html",url="/view"+area+"/"+str(parrent))
			
			
				









		@app.route("/personal")
		def personal():
			return render_template("personal.html")


		##########################
		#--Testing pages/stupid--#
		##########################


		@app.route("/epilepsy")
		def epilepsy():
			return render_template("epilepsy.html")
		
		@app.route("/crash")
		def crash():
			you_shouldnt_see_the_debugger_if_you_do_please_tell_me();
		@app.route("/test")
		def testtttt():
			return render_template("gameSite")

		#################################
		#--School projects and whatnot--#
		#################################
		@app.route("/german")
		def german():
			return render_template("german.html")			

		@app.route("/game")
		def game2222():
			return render_template("videogame.html")
		@app.route("/game/")
		def gameslash():
			return '<!DOCTYPE html><html><head><meta http-equiv="refresh" content="0; url=/game" /></head></html>'
		

		###################
		#--Special Pages--#
		###################


		@app.errorhandler(404)
		def error_404(err):
			return render_template("error.html",head="404",msg="You've tried to look at a page on my site. Luckily, your eyes are spared, as the page does not exist.")



	##############
	#--Run site--#
	##############


	if __name__ == '__main__':
		

		app.run(host='0.0.0.0',port=port,ssl_context=ssl_context,debug=debug)
