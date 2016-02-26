
--[[
This work has been released as public domain by Jackson Reed McNeill.
eGraphpaper prototype
A prototype, things may not nessisarily be done in the most effecient well-readable, or sane whatsoever way.

]]

function writeToConsole(text)
	print(text)
end
function love.load()
	--console system instant print out
	--io.stdout:setvbuf("no")
	--love.window.setTitle("eGraphpaper prototype")
	--load images
	tile = love.graphics.newImage("grid.png")
	arrow = love.graphics.newImage("menu.png")
	--cheaterbanner= love.graphics.newImage("cheater.png")--note: 400x200
	--globals
	texty = {}
	scrollx = 0
	scrolly = 0
	test = false
	menuOpen = false
	--font
	font = love.graphics.newFont(25)
	pushCursor = true
	lines = {}
end
function _draw()

--set font
	love.graphics.setFont(font)
	--Cahnged from love.window.getMod e() for web port
	--winwith, winhieght = love.graphics.getMode()
	winwith=640
	winhieght=480
	--love.graphics.print("test",5,5)
	--[[local a,b = winwith/25
	for x=0,math.max(a) do 
		 b= winhieght/25
		for y=0,math.max(b) do
			love.graphics.draw(tile,x*25,y*25)
			--love.graphics.print("test",x*25,y*25)
		end
	end]]
	--set color for printing:
    love.graphics.setColor(0,0,0)
	for i=0,table.maxn(lines) do
		if lines[i] then
			for o=0,table.maxn(lines[i]) do
				if lines[i][o] == "x" then 
					love.graphics.rectangle("fill",(o-scrollx)*25,(i-scrolly)*25+12,25,4)
				elseif lines[i][o] == "y" then 
					love.graphics.rectangle("fill",(o-scrollx)*25+12,(i-scrolly)*25,4,25)end --This looks bad, I know. The webport does not like the enter.
			end 
		end 
	end 

	for i=0,table.maxn(texty) do
		if texty[i] then
			for o=0,table.maxn(texty[i]) do
				if type(texty[i][o]) == "string" then 
					love.graphics.print(texty[i][o],(o-scrollx)*25+2,(i-scrolly)*25,0,1,1) --12, 12 if we give each box its own grid
				end 
			end 
		end 
	end 
	--]]
	--set back

	love.graphics.setColor(255,255,255)
	love.graphics.setColor(255,0,255)
	love.graphics.print("hidfgsdfgsdfgsdfsdfgsdgsdgsdgsdgsdgsdgsdsdgse",1,1)
	--

	--we left out 1,1 so,
	--love.graphics.draw(tile,1,1)
	--draw the arrow
	love.graphics.draw(arrow,winwith-12,0)
	love.graphics.setColor(0,255,255)
	if menuOpen then 

		love.graphics.rectangle("fill",winwith-250,0,250,winhieght)
		drawButton("Mono-digit calculator",winwith-200,10,150,50,255,0,0)
		drawButton("Clear sheet",winwith-200,80,150,50,255,0,0) --40 space inbetween


		love.graphics.setColor(255,255,255)
		love.graphics.draw(arrow,winwith-250,12,math.pi)
	else 
		love.graphics.setColor(255,255,255)
	end--]]

end 
function love.draw()
	_draw()
end
function drawButton(text,x,y,sizex,sizey,r,g,b)
	love.graphics.setColor(r, g, b)
	love.graphics.rectangle("fill",x,y,sizex,sizey)
	love.graphics.setColor( 0,0,0)
	love.graphics.print(text,x,y)
end
function checkButton(x,y,sizex,sizey,mousex,mousey)
	if mousex>=x and mousey>=y and mousex<=(x+sizex) and mousey <=(y+sizey) then 
		return true 
	else
		return false
	end
end

function love.textinput(key,faked)
	if not menuOpen then
		writeToConsole(love.mouse.getY())
		writeToConsole(love.mouse.getX())
		texty[math.floor(love.mouse.getY()/25)+scrolly] = texty[math.floor(love.mouse.getY()/25)+scrolly] or {}
		texty[math.floor(love.mouse.getY()/25)+scrolly][math.floor(love.mouse.getX()/25)+scrollx] = key
		if love.window.getMode() >= love.mouse.getX()+25 and pushCursor then 
			if key==" " and 0<=love.mouse.getX()-25 and faked then 
				love.mouse.setX(love.mouse.getX()-25)
			elseif key~=" " or not faked then
				love.mouse.setX(love.mouse.getX()+25)
			end
		end
		--clear whatever line is in the same space
		if lines[math.floor(love.mouse.getY()/25+scrolly)] then 
			lines[math.floor(love.mouse.getY()/25+scrolly)][math.floor(love.mouse.getX()/25+scrollx)] = nil 
		end
	end
end
function love.mousepressed(x,y,button)
	love.web.showPreCompiledJS("main.lua")
	if menuOpen then
		if checkButton(winwith-200,10,150,50,x,y)  then 
		elseif checkButton(winwith-262,0,12,12,x,y) then
			menuOpen = false
		elseif checkButton(winwith-200,80,150,50,x,y) then 
			lines = {}
			texty = {}
		end 
	else 
		if checkButton(winwith-12,0,winwith,12,x,y) then 
			menuOpen = true 
		end
	end 
end 
function love.keypressed(key,repeated)
	if key=="backspace" then 
		love.textinput(" ",true)
	elseif key =="down" then 
		scrolly = scrolly+1
	elseif key =="up" and scrolly>0 then 
		scrolly = scrolly-1
	elseif key=="right" then 
		scrollx = scrollx+1 
	elseif key=="left"and scrollx>0 then 
		scrollx=scrollx-1
	elseif key =="return" then
 		love.mouse.setPosition(12,love.mouse.getY()+25)
	end 
end 
function love.update(d)
	if test then
		--[[if not love.window.hasFocus() then 
			love.mouse.setX(10)
			love.mouse.setY(10)
			love.mouse.setVisible(false)
			cheater = true
		else
			love.mouse.setVisible(true)
			cheater = false
		end ]]
		--love.mouse.setGrabbed(true)
	else
	    --love.mouse.setGrabbed(false)
	end
	if not menuOpen then 
		if love.mouse.isDown"l" then
			if mousex and mousey then
				local x,y=love.mouse.getPosition()
				--find if the position has changed
				if math.floor(x/25)~=math.floor(mousex/25) then 
					--bugfix for a line being created after closing the menu
					local b1 = math.max(math.floor(x/25),math.floor(mousex/25))
					local b2 = math.min(math.floor(x/25),math.floor(mousex/25))
					if b1-b2>1 then --if they've moved more than 1 tile
						return
					end
					lines[math.floor(mousey/25+scrolly)] = lines[math.floor(mousey/25+scrolly)] or {}
					lines[math.floor(mousey/25+scrolly)][math.floor(mousex/25+scrollx)] = "x"
					--local changed = true
				elseif math.floor(y/25)~= math.floor(mousey/25) then
					lines[math.floor(mousey/25+scrolly)] = lines[math.floor(mousey/25+scrolly)] or {}
					lines[math.floor(mousey/25+scrolly)][math.floor(mousex/25+scrollx)] = "y"
					--local changed = true 
				end
				--if changed then 
					--texty[math.floor(mousey/25+scrolly)][math.floor(mousex/25+scrollx)] = nil 
				--end
				--we don't remove the text so you can cross out stuff
			end
		end
		mousex, mousey = love.mouse.getPosition()
	end
end 
