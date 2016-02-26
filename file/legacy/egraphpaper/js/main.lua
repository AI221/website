-- AbstractVehicle 2012-10 ghoulsblade@schattenkind.net
-- note. berlin gamedev facebook.   Richard Wepner   	
-- commandline -nomusic

--[[
notes:

non-moving bunker with multiple independent turrets on top 
non-moving artillery type enemy			 -- WORLD_CASTLE_CHANCE :   wenn mitte zerstört geht zugbruecke rechts auf
auto-scrolling cam, that doesn't allow back-move ?
scenery like binary trees etc
bridge : more spring constant
gate : vll andere tuer 
pendel abgrund : breiter und mehrere pendel
boss: hexagon rotating and spawning smaller stuff
boss: sea-serpent link thing coming out of abyss, not colliding with bridges 
levels : floor color, scenery, sometimes cave ceiling 

DONE:  half-circle  : jump and bomb (frog, arc-bomber)
DONE wenn selten schiessen erster schuss staerker
DONE charged power sniper shot if not firing all the time
DONE enemy death chance to spawn first aid
DONE black floater : hits itself : radius inc 
DONE haengebruecke raender schlecht fuer npcs : bissl tiefer
]]--

checkGLError = function (msg) end
if (love.web and love.web.checkGLError) then checkGLError = love.web.checkGLError end

love.filesystem.load("lib.oop.lua")()
love.filesystem.load("lib.obj.lua")()
love.filesystem.load("lib.particle.lua")()
love.filesystem.load("lib.util.lua")()

love.filesystem.load("obj.box.lua")()
love.filesystem.load("obj.bullet.lua")()
love.filesystem.load("obj.floater.lua")()
love.filesystem.load("obj.player.lua")()
love.filesystem.load("obj.spark.lua")()
love.filesystem.load("obj.tank.lua")()
love.filesystem.load("obj.arcbomber.lua")()

-- ***** ***** ***** ***** ***** constants

if (os.getenv("HOME") == "/home/ghoul") then DEBUG_ENABLED = true end


--~ DEBUG_GATE = DEBUG_ENABLED 
--~ DEBUG_CASTLE = DEBUG_ENABLED
--~ DEBUG_PENDULUM = DEBUG_ENABLED
--~ DEBUG_BRIDGE = DEBUG_ENABLED

--~ DEBUG_CAM_FIX = true

gMusic = true  if (arg and arg[2] == "-nomusic") then gMusic = false end
if (love.web) then gMusic = false end
gSound = true
VOLUME_MUSIC = 0.8
VOLUME_SOUND = 1

DEG_2_RAD = math.pi/180 
MAX_DT = 0.05
GRAVITY = 9.81  * 100
PHYS_METER = 100
CAM_MOVE_FACTOR = 0.05
CAM_SHOCK_MOVE_FACTOR = 0.2
CAM_SHOCK_FADE_FACTOR = 0.05

FIRST_AID_COLLECT_RANGE = 20
FIRST_AID_KIT_HEAL = 4
FIRST_AID_DROP_ON_KILL_CHANCE = 0.2

PLAYER_HP = 20
PLAYER_MOVE_FORCE = 20
PLAYER_JUMP_IMPULSE = -10
PLAYER_BULLET_D = 20
PLAYER_BULLET_V = 6*100 
PLAYER_SHOT_INTERVAL = 0.2
PLAYER_POWER_SHOT_INTERVAL = 0.5

BULLET_EXPLOSION_IMPULSE_RADIUS = 50
BULLET_EXPLOSION_IMPULSE_STR = 5

WORLD_BRIDGE_CHANCE = 0.1
WORLD_BRIDGE_MIN_W = 200
WORLD_BRIDGE_MAX_W = 400

WORLD_PENDULUM_CHANCE = WORLD_BRIDGE_CHANCE / 7
WORLD_PENDULUM_MIN_W = 200
WORLD_PENDULUM_MAX_W = 200

WORLD_CASTLE_CHANCE = 0.1/4

WORLD_GATE_CHANCE = 0.1/4
WORLD_GATE_NUM_BOXES = 3
WORLD_GATE_HEIGHT = 500
WORLD_GATE_HP = 20

TIER2_ENEMY_MINX = 4 * 1000
TIER3_ENEMY_MINX = 8 * 1000

SCORE_HP_FACTOR = 1000

ENEMY_SPAWN_MIN_X = 500*2


ENEMY_ARCBOMBER = {}
ENEMY_ARCBOMBER.R = 15
ENEMY_ARCBOMBER.HP = 4
ENEMY_ARCBOMBER.OFF_Y = -150
ENEMY_ARCBOMBER.FORCE_X = 1*15
ENEMY_ARCBOMBER.FORCE_Y = 2*15
ENEMY_ARCBOMBER.CHANCE = 0.15
ENEMY_ARCBOMBER.FIRE_INTERVAL = 0.4
ENEMY_ARCBOMBER.BULLET_D = 20
ENEMY_ARCBOMBER.BULLET_V = 6*100 
ENEMY_ARCBOMBER.MAX_RANGE = 300
ENEMY_ARCBOMBER.BULLET_RANDANG = 20*DEG_2_RAD
ENEMY_ARCBOMBER.col_line = MkCol( 0x0012ff )
ENEMY_ARCBOMBER.col_fill = MkCol( 0x000088 )
ENEMY_ARCBOMBER.SCORE_MULTI = 2
cObjEnemyArcBomber.template = ENEMY_FLOATER

ENEMY_FLOATER = {}
ENEMY_FLOATER.R = 15
ENEMY_FLOATER.HP = 4
ENEMY_FLOATER.OFF_Y = -150
ENEMY_FLOATER.FORCE_X = 1*15
ENEMY_FLOATER.FORCE_Y = 2*15
ENEMY_FLOATER.CHANCE = 0.25
ENEMY_FLOATER.FIRE_INTERVAL = 1
ENEMY_FLOATER.BULLET_D = 20
ENEMY_FLOATER.BULLET_V = 6*100 
ENEMY_FLOATER.MAX_RANGE = 300
ENEMY_FLOATER.BULLET_RANDANG = 10*DEG_2_RAD
ENEMY_FLOATER.col_line = MkCol( 0xff4400 )
ENEMY_FLOATER.col_fill = MkCol( 0x882200 )
ENEMY_FLOATER.SCORE_MULTI = 1
cObjEnemyFloater.template = ENEMY_FLOATER

ENEMY_FLOATER2 = copyarr(ENEMY_FLOATER)
ENEMY_FLOATER2.CHANCE = ENEMY_FLOATER.CHANCE / 3
ENEMY_FLOATER2.OFF_Y = -200
ENEMY_FLOATER2.FORCE_X = 2*15
ENEMY_FLOATER2.FORCE_Y = 4*15
ENEMY_FLOATER2.R = 20
ENEMY_FLOATER2.HP = 12
ENEMY_FLOATER2.FIRE_INTERVAL = 0.8
ENEMY_FLOATER2.MAX_RANGE = 400
ENEMY_FLOATER2.BULLET_D = 25
ENEMY_FLOATER2.BULLET_RANDANG = 10*DEG_2_RAD
ENEMY_FLOATER2.col_line = MkCol( 0x0088ff )
ENEMY_FLOATER2.col_fill = MkCol( 0x004488 )
ENEMY_FLOATER2.SCORE_MULTI = 2

ENEMY_FLOATER3 = copyarr(ENEMY_FLOATER2)
ENEMY_FLOATER3.CHANCE = ENEMY_FLOATER2.CHANCE / 3
ENEMY_FLOATER3.OFF_Y = -250
ENEMY_FLOATER3.FORCE_X = 3*15
ENEMY_FLOATER3.FORCE_Y = 6*15
ENEMY_FLOATER3.R = 25
ENEMY_FLOATER3.HP = 32
ENEMY_FLOATER3.FIRE_INTERVAL = 0.6
ENEMY_FLOATER3.MAX_RANGE = 500
ENEMY_FLOATER3.BULLET_D = 30
ENEMY_FLOATER3.BULLET_RANDANG = 10*DEG_2_RAD
ENEMY_FLOATER3.col_line = MkCol( 0x888888 )
ENEMY_FLOATER3.col_fill = MkCol( 0x444444 )
ENEMY_FLOATER3.SCORE_MULTI = 5


ENEMY_TANK = {}
ENEMY_TANK.HP = 4
ENEMY_TANK.OFF_Y = -100
ENEMY_TANK.FORCE_X = 20
ENEMY_TANK.CHANCE = 0.3
ENEMY_TANK.FIRE_INTERVAL = 1
ENEMY_TANK.BULLET_D = 20
ENEMY_TANK.BULLET_V = 6*100 
ENEMY_TANK.MAX_RANGE = 500
ENEMY_TANK.NEAR_RANGE = 200
ENEMY_TANK.FAV_RANGE = 100
ENEMY_TANK.BULLET_RANDANG = 10*DEG_2_RAD
ENEMY_TANK.col_line = MkCol( 0xff00ff )
ENEMY_TANK.col_fill = MkCol( 0x880088 )
ENEMY_TANK.scale_size = 1
ENEMY_TANK.SCORE_MULTI = 1
cObjEnemyTank.template = ENEMY_TANK

ENEMY_TANK2 = copyarr(ENEMY_TANK)
ENEMY_TANK2.HP = 12
ENEMY_TANK2.CHANCE = ENEMY_TANK.CHANCE / 3
ENEMY_TANK2.col_line = MkCol( 0x0000ff )
ENEMY_TANK2.col_fill = MkCol( 0x000088 )
ENEMY_TANK2.scale_size = 1.5
ENEMY_TANK2.FORCE_X = 40
ENEMY_TANK2.FIRE_INTERVAL = 0.5
ENEMY_TANK2.SCORE_MULTI = 2


ENEMY_TANK3 = copyarr(ENEMY_TANK2)
ENEMY_TANK3.HP = 32
ENEMY_TANK3.CHANCE = ENEMY_TANK2.CHANCE / 3
ENEMY_TANK3.col_line = MkCol( 0x888888 )
ENEMY_TANK3.col_fill = MkCol( 0x444444 )
ENEMY_TANK3.scale_size = 1.8
ENEMY_TANK3.FORCE_X = 60
ENEMY_TANK3.FIRE_INTERVAL = 0.5
ENEMY_TANK3.SCORE_MULTI = 5



RAISE_TEXT_COL_SCORE	= MkCol( 0x00FF00 )
RAISE_TEXT_SPEED_Y		= -200
RAISE_TEXT_SPEED_FACTOR = 0.95
RAISE_TEXT_TTL			= 0.8


ENEMY_BOX_SCORE_MULTI = 0.5

ENEMY_BOX_HP = 2
ENEMY_BOX_OFF_Y = -100
ENEMY_BOX_MINNUM = 2
ENEMY_BOX_MAXNUM = 6
ENEMY_BOX_PER_ROW = 3
ENEMY_BOX_CHANCE = 0.3
ENEMY_BOX_FIRST_AID_CHANCE = 0.1

ENEMY_METALBOX_CHANCE = 0.1
ENEMY_METALBOX_HP = 5
ENEMY_METALBOX_SCALE = 1.2

SPARK_MIN_NUM,SPARK_MAX_NUM = 5,10
SPARK_MIN_D,SPARK_MAX_D = 0,10
SPARK_MIN_V,SPARK_MAX_V = 100,500
SPARK_MIN_TTL,SPARK_MAX_TTL = 0.2,0.8

PHYS_CATEGORY_GROUND	= 1
PHYS_CATEGORY_PLAYER	= 2
PHYS_CATEGORY_ENEMY		= 3
PHYS_CATEGORY_BULLET	= 4
PHYS_CATEGORY_EFFECT	= 5
--~ self.fixture:setGroupIndex( group )
--~ self.fixture:setCategory( category1, category2, ... )
--~ self.fixture:setMask( mask1, mask2, ... )


HALF_SCREEN						= 500
GAME_KILL_BEHIND_PLAYER_X		= 3*500+HALF_SCREEN
GAME_SPAWN_AHEAD_OF_PLAYER_X	= 500+HALF_SCREEN

GAMY_LIMIT_KILL_Y				= 1000

GROUND_GAP_MINX = 0


gColHealthBar_LINE = MkCol( 0xFFFFFF )
gColHealthBar_FILL = MkCol( 0xAAAAAA )



-- ***** ***** ***** ***** ***** vars


gCamX = 0
gCamY = 0
gCamAddX = 0
gCamAddY = 0
gCamShockX = 0
gCamShockY = 0
gCamShockStrRemaining = 0
gKeyPressed = {}
gMyTime = 0
gPlayerFarX = 0

gStateTitle = {}
gStateGame = {}
gState = gStateTitle

-- ***** ***** ***** ***** ***** spawn

function SpawnCastle (cx,cy,aL,aR)
	--~ print("SpawnCastle",cx,cy)
	cy = cy - 10
	local w,h = 50,20
	local hp_structure = 4
	local x,y
	local density = 0.8
	
	-- towers
	local ftemp = ENEMY_FLOATER2
	local col = MkCol(0x888888)
	local e = w + 5
	
	cObjEnemyArcBomber:New(cx-e,cy,ENEMY_ARCBOMBER)
	
	for i = 1,4 do x,y = cx+e*0,cy-h*i cStructure:New(x,y,w,h,nil,hp_structure,density,col) end cObjEnemyFloater:New(x,y-ftemp.OFF_Y-60,ftemp)
		x,y = cx+e*1,cy-h*0 				  cStructure:New(x,y,w,h,nil,hp_structure,density,col)	cObjBox:New(x,y-h-30,BOXTYPE_FIRSTAID) 
		x,y = cx+e*2,cy-h*1 local switchT	= cStructure:New(x,y,w,h,nil,hp_structure,density,col)
		x,y = cx+e*2,cy-h*0 local switch	= cObjBox:New(x,y,BOXTYPE_SWITCH) 
		x,y = cx+e*3,cy-h*0 				  cStructure:New(x,y,w,h,nil,hp_structure,density,col)	cObjBox:New(x,y-h-30,BOXTYPE_FIRSTAID) 
	for i = 1,4 do x,y = cx+e*4,cy-h*i cStructure:New(x,y,w,h,nil,hp_structure,density,col) end cObjEnemyFloater:New(x,y-ftemp.OFF_Y-60,ftemp)
	
	love.physics.newWeldJoint( switchT.body, switch.body, switch.x, switch.y)
	
	-- drawbridge
	local ax,ay = aL.body:getPosition()
	local bx,by = aR.body:getPosition()
	local bridgew = bx-ax
	aR.body:setPosition(ax+50,ay-bridgew+30)
	
	
	switch.OnDie = function () aR.body:setPosition(bx,by) end
end

-- ***** ***** ***** ***** ***** spawn

gWorldSpecialBlocker = 0
function SpawnAroundPlayer (playerx)
	
	local x = gGameSpawnedX
	local y = gGameSpawnedY
	local w = 100
	local h = 60
	local ec = 0
	local minx = playerx + GAME_SPAWN_AHEAD_OF_PLAYER_X
	if (x < minx) then
		Obj_DespawnLeftOf(playerx - GAME_KILL_BEHIND_PLAYER_X)
	end
	while (x < minx) do 
		local ang = 20*DEG_2_RAD*rand_in_range(-1,1)
		local terminate_left = false
		local bAllowEnemies = (x > ENEMY_SPAWN_MIN_X)
		
		local function SpawnGroundPlate (ang,bAllowEnemies) 
			x = x + 0.5*w*cos(ang)
			y = y + 0.5*w*sin(ang)
			local ax = -0.5*h*sin(ang)
			local ay =  0.5*h*cos(ang)
			local o = cGround:New(x+ax,y+ay,w,h,ang)
			if (terminate_left) then o.terminate_left = true end
			
					--~ ec = ec + 1 
			if (bAllowEnemies) then 
					if ( 							randf() < ENEMY_ARCBOMBER.CHANCE) then 	cObjEnemyArcBomber:New(x+ax,y+ay,ENEMY_ARCBOMBER)
				elseif ( 							randf() < ENEMY_FLOATER.CHANCE) then 	cObjEnemyFloater:New(x+ax,y+ay,ENEMY_FLOATER)
				elseif ( x >= TIER2_ENEMY_MINX and	randf() < ENEMY_FLOATER2.CHANCE) then 	cObjEnemyFloater:New(x+ax,y+ay,ENEMY_FLOATER2)
				elseif ( x >= TIER3_ENEMY_MINX and	randf() < ENEMY_FLOATER3.CHANCE) then 	cObjEnemyFloater:New(x+ax,y+ay,ENEMY_FLOATER3)
				elseif ( 							randf() < ENEMY_TANK.CHANCE) then		cObjEnemyTank:New(x+ax,y+ay,ENEMY_TANK)
				elseif ( x >= TIER2_ENEMY_MINX and	randf() < ENEMY_TANK2.CHANCE) then		cObjEnemyTank:New(x+ax,y+ay,ENEMY_TANK2)
				elseif ( x >= TIER3_ENEMY_MINX and	randf() < ENEMY_TANK3.CHANCE) then		cObjEnemyTank:New(x+ax,y+ay,ENEMY_TANK3)
				elseif ( 							randf() < ENEMY_BOX_CHANCE) then 		SpawnBoxes(x+ax,y+ay+ENEMY_BOX_OFF_Y)
				end
			end
		
			x = x + 0.5*w*cos(ang)
			y = y + 0.5*w*sin(ang)
			return o
		end
		
		
		if (gWorldSpecialBlocker > 0) then gWorldSpecialBlocker = gWorldSpecialBlocker - 1 end
		if (gWorldSpecialBlocker <= 0 and x > GROUND_GAP_MINX) then 
			gWorldSpecialBlocker = 3
	
			local gapw
			if (randf() < WORLD_CASTLE_CHANCE or DEBUG_CASTLE) then 
				ang = 0
				gapw = rand_in_range(WORLD_PENDULUM_MIN_W,WORLD_PENDULUM_MAX_W) * 3
				local cx,cy = x+w*1+gapw,y
				SpawnBridge(x,y,x+gapw,y) x = x + gapw
				SpawnGroundPlate(0).terminate_left = true
				SpawnGroundPlate(0)
				SpawnGroundPlate(0)
				SpawnGroundPlate(0)
				local aL,aR = SpawnBridge(x,y,x+gapw,y) x = x + gapw
				SpawnCastle(cx,cy,aL,aR)
				terminate_left = true
				bAllowEnemies = false
			else
					
				if (randf() < WORLD_PENDULUM_CHANCE or DEBUG_PENDULUM) then 
					gapw = rand_in_range(WORLD_PENDULUM_MIN_W,WORLD_PENDULUM_MAX_W)
					SpawnPendulum(x,y,x+gapw,y)
				elseif (randf() < WORLD_BRIDGE_CHANCE or DEBUG_BRIDGE) then 
					gapw = rand_in_range(WORLD_BRIDGE_MIN_W,WORLD_BRIDGE_MAX_W)
					SpawnBridge(x,y,x+gapw,y)
				elseif ((randf() < WORLD_GATE_CHANCE) and (x >= TIER2_ENEMY_MINX)) or DEBUG_GATE then 
					gWorldSpecialBlocker = 5
					gMapGenNextFlat = 3
					SpawnGate(x+1.5*w,y)
				end
				
				if (gapw) then 
					x = x + gapw
					ang = 0
					terminate_left = true
				end
			end
		end
		
		if (gMapGenNextFlat and gMapGenNextFlat > 0) then 
			gMapGenNextFlat = gMapGenNextFlat - 1
			ang = 0
		end
		
		SpawnGroundPlate(ang,bAllowEnemies)
		
		gGameSpawnedX = x
		gGameSpawnedY = y
	end
end


-- ***** ***** ***** ***** ***** score and respawn

gScore = 0
gMaxScore = 0

function ScoreAdd (val,obj) 
	if (not gPlayer) then return end
	gScore = gScore + val
	gMaxScore = max(gMaxScore,gScore)
	
	if (obj) then SpawnRaiseText(TausenderTrenner(val),RAISE_TEXT_COL_SCORE,obj) end
end

function SpawnRaiseText (txt,col,o)
	--~ print("SpawnRaiseText",txt,o.x,o.y)
	cObjRaiseText:New(o.x,o.y,txt,RAISE_TEXT_SPEED_Y,RAISE_TEXT_TTL,col) 
end

function RespawnPlayer()
	Obj_Clear()
	gPlayerFarX = 0
	gWorldSpecialBlocker = 0
	gScore = 0
	gPlayer = cPlayer:New(0,0)
	gGameSpawnedX = -HALF_SCREEN-200
	gGameSpawnedY = 200
	SpawnAroundPlayer(gPlayer.x)
end

-- ***** ***** ***** ***** ***** load

function love.load ()
	gMyTime = love.timer.getTime()
	StartGameWorld()
	gStateTitle:Start()
end
	
-- ***** ***** ***** ***** ***** phys callbacks

function Phys_OnCollision (fixA,fixB,contact)
	local a = fixA:getUserData()
	local b = fixB:getUserData()
	InvokeNext(function ()
		if (a and a.OnCollision) then a:OnCollision(b) end
		if (b and b.OnCollision) then b:OnCollision(a) end
	end)
end


-- ***** ***** ***** ***** ***** CamShock

function CamShock (str) 
	gCamShockStrRemaining = gCamShockStrRemaining + str
end

function CamShock_PlayerHurt ()
	CamShock(80)
end
function CamShock_Death ()
	CamShock(40)
end
function CamShock_BulletBoom ()
	CamShock(5)
end

-- ***** ***** ***** ***** ***** key + mouse

function love.mousereleased( x, y, button  )
	gKeyPressed["m"..button] = nil
end	

function love.mousepressed( x, y, button )
	gKeyPressed["m"..button] = true
	if (gState ~= gStateGame) then StartGameState() return end
	
	local gx,gy = x-gCamAddX,y-gCamAddY
	--~ if (button == "r") then SpawnExplosion(gx,gy) end
	if (button == "r" and DEBUG_ENABLED) then SpawnBoxes(gx,gy) end
	if (button == "l") then 
		if (not gPlayer) then RespawnPlayer() return end
		if (gPlayer) then gPlayer:OnClick(x,y) end
	end
end

function StartGameState ()
	gState = gStateGame
	gState:Start()
end

function love.keypressed( key, unicode )
    if (key == "escape") then os.exit(0) end
    if (key == "f12") then love.graphics.toggleFullscreen() end
	
	if (gState ~= gStateGame) then StartGameState() return end
    if (key == "1" and DEBUG_ENABLED) then CamShock(5) end
    if (key == "2" and DEBUG_ENABLED) then CamShock(10) end
    if (key == "3" and DEBUG_ENABLED) then CamShock(20) end
    if (key == "4" and DEBUG_ENABLED) then CamShock(40) end
    if (key == "5" and DEBUG_ENABLED) then CamShock(200) end
	--~ MySndKey(key)
	gKeyPressed[key] = true
	if (not gPlayer) then RespawnPlayer() end
end
function love.keyreleased( key ) gKeyPressed[key] = nil end


-- ***** ***** ***** ***** ***** update

function love.update (dt)
	gScreenW = love.graphics.getWidth( )	
	gScreenH = love.graphics.getHeight( )	
	gState:update(dt)
end 

-- ***** ***** ***** ***** ***** draw

gNoDrawCounter = 10
function love.draw ()
	if (gNoDrawCounter > 0) then gNoDrawCounter = gNoDrawCounter - 1 return end
	
	checkGLError("love.draw start")
	gScreenW = love.graphics.getWidth( )	
	gScreenH = love.graphics.getHeight( )	
	checkGLError("love.draw getWidth/getHeight")
	gState:draw()
	checkGLError("love.draw gState:draw")
end


-- ***** ***** ***** ***** ***** gStateTitle


function gStateTitle:Start ()
	gGameSpawnedX = -HALF_SCREEN-200
	gGameSpawnedY = 200
	self.scrollx = 0
	SpawnAroundPlayer(self.scrollx)
	
	self.next_explosion = 0
end

function gStateTitle:update (dt)
	UpdateGameWorld(dt)
	self.scrollx = self.scrollx + dt*200
	SpawnAroundPlayer(self.scrollx)
	
	if (self.next_explosion < gMyTime) then
		self.next_explosion = gMyTime + rand_in_range(1,2) 
		for i=1,floor(rand_in_range(1,3)) do 
			local gx,gy = rand_in_range(0,gScreenW)-gCamAddX,rand_in_range(0,128)-gCamAddY
			SpawnExplosion(gx,gy)
		end
	end
end

function gStateTitle:draw ()
	checkGLError("gStateTitle:draw start")
	DrawGameWorld()
	checkGLError("gStateTitle:draw DrawGameWorld")
	
	SetCol({255,255,255,255})
	--~ love.graphics.print("AbstractCombat",100,100)
	local x,y = 0,64
	y = y + 32 * sin(360 * DEG_2_RAD * gMyTime / 3)
	love.graphics.draw(gImgTitle,x,y)
	checkGLError("gStateTitle:draw gImgTitle")
	
	love.graphics.print([[
W-A-D or Arrow Keys to move and jump
mouse for target (aim high for range)
left mousebutton to shoot
F12 to toggle fullscreen]],100,gScreenH - 100)
	checkGLError("gStateTitle:draw text")

end


-- ***** ***** ***** ***** ***** gStateGame

function gStateGame:Start ()
	RespawnPlayer()
end

function gStateGame:update (dt)
	UpdateGameWorld(dt)
end 

function gStateGame:draw ()
	DrawGameWorld()
	
	SetCol(gColHealthBar_LINE)
	love.graphics.print(TausenderTrenner(gScore),0,0)
	if (gMaxScore > gScore) then 
		love.graphics.print(TausenderTrenner(gMaxScore),0,20)
	end
	
	-- healthbar
	local vw = gScreenW
	local vh = gScreenH
	local x = vw/4
	local y = 5
	local w = vw/2
	local h = 20
	local b = 2
	local f = gPlayer and (gPlayer.hp / PLAYER_HP) or 0
	SetCol(gColHealthBar_LINE) love.graphics.rectangle( "line", x  , y  , w      , h     )
	SetCol(gColHealthBar_FILL) love.graphics.rectangle( "fill", x+b, y+b, w*f-2*b, h-2*b )
end

-- ***** ***** ***** ***** ***** GameWorld

function StartGameWorld()
	local xg = 0
	local yg = GRAVITY
	
	ParticleInit()
	
	love.physics.setMeter( PHYS_METER )
	gWorld = love.physics.newWorld( xg, yg )
	
	gWorld:setCallbacks( Phys_OnCollision, nil, nil, nil )
	
	local function myimg (path) return love.graphics.newImage(path) end
	gImgTitle = myimg("data/title.png")
	
	local function mysnd (path) 
		local snd = {}
		if (gSound) then 
			snd.src = love.audio.newSource(path,"static") 
			snd.src:setVolume(VOLUME_SOUND) 
		end
		function snd:play ()
			if (self.next_play_t > gMyTime) then return end
			self.next_play_t = gMyTime + self.play_interval
			if (gSound) then 
				--~ love.audio.play(self.src)
				self.src:stop()
				self.src:rewind()
				self.src:play() -- Starts playing the Source.
			end
			--~ print("snd:play()",self.path)
		end
		snd.path = path 
		snd.next_play_t = 0
		snd.play_interval = 0.1 -- seconds
		return snd
	end
	
	gSnd_Shot		= mysnd("data/boom06.wav")
	gSnd_Hit		= mysnd("data/hit02.wav")
	gSnd_DeathHi	= mysnd("data/boom03.wav")
	gSnd_DeathLo	= mysnd("data/boom01.wav")
	gSnd_Heal		= mysnd("data/powerup02.wav")
	
	gSounds = {
		--~ mysnd("data/boom06.wav"),		-- shot
		--~ mysnd("data/hit02.wav"),		-- hit
		--~ mysnd("data/boom03.wav"),		-- death
		--~ mysnd("data/boom01.wav"),		-- death
		--~ mysnd("data/powerup02.wav"),	-- heal
		}
		
		function MySndKey (key)
			--~ print("MySndKey",key,tonumber(key))
			for k,v in pairs(gSounds) do 
				if (tonumber(key) == k) then v:play() end
			end
		end
	
	if (gMusic) then
		local musicpath = "data/loop01.ogg"
		gMusicSrc = love.audio.newSource(musicpath)
		gMusicSrc:setLooping(true)
		gMusicSrc:setVolume(VOLUME_MUSIC)
		gMusicSrc:play()
	end
end




function UpdateGameWorld(dt)
	dt = min(MAX_DT,dt)
	gMyTime = love.timer.getTime()
	gWorld:update(dt)
	Obj_Step(dt)
	local f = CAM_MOVE_FACTOR
	if (gPlayer) then 
		if (not DEBUG_CAM_FIX) then 
			gCamX = (1-f)*gCamX + f*gPlayer.x 
			gCamY = (1-f)*gCamY + f*gPlayer.y
		end
	elseif (gState == gStateTitle) then
		local cam_target_x = gStateTitle.scrollx
		local cam_target_y = 0
		gCamX = (1-f)*gCamX + f*cam_target_x
		gCamY = (1-f)*gCamY + f*cam_target_y
	end
	
	gCamShockStrRemaining = (1-CAM_SHOCK_FADE_FACTOR)*gCamShockStrRemaining
	local shock_targetX = gCamShockStrRemaining*rand_in_range(-1,1)
	local shock_targetY = gCamShockStrRemaining*rand_in_range(-1,1)
	local f = CAM_SHOCK_MOVE_FACTOR
	gCamShockX = (1-f)*gCamShockX + f*shock_targetX
	gCamShockY = (1-f)*gCamShockY + f*shock_targetY
	--~ print("camshock",floor(gCamShockX*10),floor(gCamShockY*10))
	
	local vw = love.graphics.getWidth( )
	local vh = love.graphics.getHeight( )
	gCamAddX = gCamShockX+vw/2-gCamX
	gCamAddY = gCamShockY+vh/2-gCamY
	
	if (gPlayer) then SpawnAroundPlayer(gPlayer.x) end
	
	-- score for x movement (just a little)
	if (gPlayer) then 
		local curx = floor(gPlayer.x/20)
		if (gPlayerFarX < curx) then
			ScoreAdd(curx - gPlayerFarX)
			gPlayerFarX = curx
		end
	end
end




function DrawGameWorld ()
	checkGLError("gltest 00 start")
	
	local col_ground2 = MkCol( 0x00ff44 , 0.1*255 )
	
	checkGLError("gltest 01 MkCol")
	
	SetCol(col_ground2)
	
	checkGLError("gltest 02 SetCol")
	
	love.graphics.line(0,0,100,100)
	
	checkGLError("gltest 03 line")
	
	checkGLError("DrawGameWorld start")
	Obj_DrawBack()
	Obj_Draw()
end

-- ***** ***** ***** ***** ***** rest
