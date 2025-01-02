import pygame
import re
from random import randint
try:
	from replit import audio
	repl = True
except:
	repl = False

pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()

def fake_print(text,**args):
	"""Prints text to the fake console. Arguments:
	text: text to print
	end (optional): like in python's print, end print with a different character.
	clr (optional): change the text's color (rgb format)
	snap (optional): bring the scroll to the bottom of the console when print."""
	global fake_console, color_dict,scroll


	if "clr" in args:
		clr = args["clr"]
		if len(text) != 1:
			for x in range(len(text)+1):
				color_dict[len(fake_console)-x-1] = clr
		else:
			color_dict[len(fake_console)-1] = clr
	if "snap" in args:
		if args["snap"] == True:
			scroll = max_scroll
	if "idt" in args:
		idt = args["idt"]
	else:
		idt = 0
	fake_console += "§"+" "*idt
	if "end" in args:
			fake_console += str(text).replace("\n","§"+" "*idt) + args["end"]
	else:
		fake_console += str(text).replace("\n","§"+" "*idt) + "§"+" "*idt


def fake_input(text):
	"""General input text into the console"""
	global fake_console, input_active, input_text
	fake_console += "§" + text + "§" + "> "
	input_active = True
	input_text = ""
	return input_text

def import_sprite(filename):
	"""Reads text sprite from file"""
	with open("sprites/"+filename,"r",encoding="UTF-8") as f:
		return f.read()

def frakenstein(boss,stickman):
	"""Merges boss and stickman sprites into a singular sprite that prints (overlaps)"""
	boss = boss.split("\n")
	stickman = stickman.split("\n")
	boss[13] += stickman[0]
	boss[14] += stickman[1]
	boss[15] += stickman[2]
	boss[16] += stickman[3]
	return "\n".join(boss)

def one_print(text): #Is a dumb workaround because everything in the game is in a while loop. So I use this so stuff only prints once.
	"""Prints only once"""
	global dnp
	if text not in dnp:
		fake_print(text)
		dnp.append(text)
		return True
	else:
		return False

def one_input(text):
	"""Asks for input only once"""
	global dnp
	if text not in dnp:
		fake_input(text)
		dnp.append(text)


def audio_both(filename,volume,loops,channel):
	"""Plays audio through both pygame.mixer and repl audio"""
	pymx_loops = 1
	if repl == True:
		if loops == True:
			source = audio.play_file(filename,volume,True,-1)
		else:
			source = audio.play_file(filename,volume,False)
		rep_aud_sources.append(source)
	else:
		if loops == True:
			pgmx_loops = -1
		if channel == 0:
			chn_mus.play(pygame.mixer.Sound(filename),pymx_loops)
		else:
			chn_sfx.play(pygame.mixer.Sound(filename),pymx_loops)

def stop_sounds():
	"""Stops sounds on both pygame.mixer and repl audio"""
	global rep_aud_sources
	if repl:
		for source in rep_aud_sources:
			try:
			 source.set_paused(True)
			except:
				pass
	else: pygame.mixer.stop()

timers = {}
dnp = []

true_win = pygame.display.set_mode((600,400))
win = true_win.copy()
pygame.display.set_caption("Attack of the One-Handed Stickman")
game = True
fontsize = 12
mono = pygame.font.Font("PressStart2P.ttf",fontsize)
mono_big = pygame.font.Font("PressStart2P.ttf",fontsize*2)
mono_small = pygame.font.Font("PressStart2P.ttf",int(fontsize*0.7))
white = (255,255,255)
fake_console = ""
color_dict = {}
max_scroll = 20
scroll = 0
scroll_rate = 110
random_color = white
bg_clr = (20,20,30)
window_scale = 1
window_loop = 0

tutorial_page = 1
tutorial_pages = 2

speed = 13
input_active = False
fight_active = False
tutorial = False

one_tracker = 0
two_tracker = 0

input_num = 0
progression = 0
progression_list = [0,0,0]

status = ""

rep_aud_sources = []
clock = pygame.time.Clock()

if not repl:
	chn_mus = pygame.mixer.Channel(0)
	chn_sfx = pygame.mixer.Channel(1)
	chn_sfx.set_volume(0.6)
	chn_mus.set_volume(0.4)


while game:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			game = False
			stop_sounds()
		elif event.type == pygame.KEYDOWN:
			if event.key in [pygame.K_RETURN,pygame.K_KP_ENTER]:
				if input_active:
					input_active = False
				if tutorial:
					tutorial_page += 1
					if tutorial_page > tutorial_pages:
						tutorial_page = 1
			elif event.key == pygame.K_ESCAPE:
				if tutorial:
					input_text = "n"
					tutorial = False
					bg_clr = (20,20,30)
				else:
					game = False
					break
			elif event.key == pygame.K_F11:
				window_loop += 1
				if window_loop == 8:
					window_loop = 0
				window_scale = [1,1.25,1.5,2,2.5,3,5,0.75][window_loop] #Different possible window scalings
			elif event.key == pygame.K_m:
				bg_clr = randint(1,255),randint(1,255),randint(1,255)
			elif event.key == pygame.K_k:
				random_color = randint(1,255),randint(1,255),randint(1,255)
			if input_active:
				input_char = event.unicode
				if re.search(r"[A-zÀ-ú1-9.,?' !]",input_char):
					input_text += input_char
					fake_console += input_char
				if input_char == '\x08' and input_text: #\x08 is backspace
					input_text = input_text[:-1]
					fake_console = fake_console[:-1]
			if fight_active:
				if event.key == pygame.K_LEFT:
					if tobor_state != "_dead" and stickman_state != "_dead":
						stickman_state = "_punch"
						timers["stickman_punch"] = int(0.5*speed)
						if not timers["tobor_immunity"]:
							audio_both("sfx/stickman_punch.wav",0.6,False,1)
							combo += 1
							miss_combo = 0
							tobor_state = "_damage"
							timers["tobor_damage"] = int(.5*speed)
							tobor_hp -= 3
							timers["tobor_immunity"] = 2*speed
							timers["player_immunity"]	+= int(stun_delay1*speed)
						else:
							audio_both("sfx/stickman_miss.wav",0.6,False,1)
							combo = 0
							miss_combo += 1
							tobor_state = "_miss"
							timers["tobor_immunity"] = 3*speed
					if combo > 3:
						status = f"C O M B O x{combo}! ! !"
						timers["status_timer"] = 2*speed
					if miss_combo == 1:
						status = "M I S S !"
						timers["status_timer"] = timers["tobor_immunity"]
					elif 1 < miss_combo <= 5:
						status = f"M I S S {miss_combo}x!"
						timers["status_timer"] = timers["tobor_immunity"]
					elif miss_combo > 5:
						if randint(1,10) == 3:
							status = ["YOU CAN DO IT!","DON'T GIVE UP!","FIGHT BACK!"][randint(0,2)]
							timers["status_timer"] = timers["tobor_immunity"]
						else:
							status = f"M I S S {miss_combo}x!"
							timers["status_timer"] = timers["tobor_immunity"]
				elif event.key == pygame.K_RIGHT:
					if timers["stickman_dodge_spam"] == 0:
						audio_both("sfx/dodge.wav",0.6,False,1)
						stickman_state = "_dodge"
						timers["stickman_dodge"] = 3*speed
						timers["stickman_dodge_spam"] = 5*speed
					else:
						audio_both("sfx/not_yet.wav",0.6,False,1)
						status = "N O T  Y E T!"
						timers["status_timer"] = 2*speed
				elif event.key == pygame.K_UP:
					if timers["double_punch_spam"] == 0 and active_boss != "tobor":
						stickman_state = "_punch"
						tobor_hp -= 3
						timers["double_punch_spam"] = int(8*speed)
						timers["stickman_punch"] = int(0.2*speed)
						audio_both("sfx/stickman_punch.wav",0.6,False,1)
						timers["double_punch"] = int(0.8*speed)
						timers["player_immunity"] += int(0.2*speed)
						status = "D O U B L E  P U N C H !"
						timers["status_timer"] = 2*speed
					else:
						status = "T O O   S O O N !"
						timers["status_timer"] = timers["double_punch_spam"]

		elif event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == 4:
				if scroll-scroll_rate >-1:
					scroll -= scroll_rate
				else:
					scroll = 0
			if event.button == 5:
				if scroll+scroll_rate < max_scroll:
					scroll += scroll_rate
				else:
					scroll = max_scroll

	#dialogue

	if not fight_active:
		while 1:

			one_print("Attack of the One-Handed Stickman")
			one_print("Who would you like to fight?")
			boss_list = ["    Lвevel 1: TOBOR","    Lвevel 2: GunMan","    Lвevel 3: TO BE CONTINUED"] #Boss 3 doesn't exist here yet.
			for inc in range(0,len(boss_list)):
				if inc <= progression:
					one_print(boss_list[inc])
				else:
					one_print(f"    Lвevel {inc+1}: LʂOʂCʂKʂEʂDʂ")
			one_input("Please write the level number")
			no_good_input = False
			if input_active:
				break
			try:
				input_num = int(input_text.strip())
			except:
				one_print("That input isn't valid!")
				no_good_input = True
			if input_num > progression+1:
				one_print("That level is locked!")
				no_good_input = True
			elif input_num == 1:
				while True:
					one_print("§§§Welcome to the game.§§You are a SɣTɣIɣCɣKɣMɣAɣNɣ. Without a hand. §§One handed, you FвAвCвEв TвHвEв WвOвRвLвDв without a plan. §§Facing gun-wielding Men that are bad, §§Robots with the inability to be sad, §§and there are even more CʂHʂAʂLʂLʂEʂNʂGʂEʂSʂ that you must face...§§ Don't put your name to a disgrace. §§§ TвOвBвOвRв is a robot with LɹAɹZɹEɹRɹ eyes. The machinery is ancient, so it shouldn't be hard to beat. Even so, SвTвAвYв SвAвFвEв, and GвOвOвDв LвUвCвKв.§") #The wierd symbols allow me to have colour for each character. The § gives a new line.

					one_input("[ɢ?ɣ]ɢ Would you like to view the tutorial (ɢyɢ/ɢnɢ)ɢ")
					input_text = input_text.lower().strip()
					if input_active:
						break
					elif input_text == "y":
						tutorial = True
						input_text = ""
						break
					else:
						fight_active = True
						tobor_hp = 40
						stickman_hp = 20
						combo = 0
						miss_combo = 0
						speed = 13

						stun_delay1 = 3

						input_text = ""
						stickman_state = ""
						tobor_state = ""
						break
				active_boss = "tobor"
			elif input_num == 2:
				while True:
					one_print("§§§GunMan has a gun.§§ He isn't afraid to SɣHɣOɣOɣTɣ you, blast you, open fire, or in other words,§§ pew-pew.§§ Enough punching will suffice.§§ Maybe even some DʂOʂUʂBʂLʂEʂ-PʂUʂNʂCʂHʂIʂNʂGʂ.§§ That said, SвTвAвYв SвAвFвEв, and GвOвOвDв LвUвCвKв.§")
					one_input("[ɢ?ɣ]ɢ Would you like to view the tutorial (ɢyɢ/ɢnɢ)ɢ")
					input_text = input_text.lower().strip()
					if input_active:
						break
					elif input_text == "y":
						tutorial = True
						input_text = ""
					else:
						fight_active = True
						tobor_hp = 120
						stickman_hp = 60
						speed = 20
						stun_delay1 = 0.5
						active_boss = "gunman"
					break
			if 1 <= input_num <= progression+1:
				no_good_input = False
				combo = 0
				miss_combo = 0
				stickman_state = ""
				tobor_state = ""

				timers["player_immunity"] = 10*speed
				timers["tobor_immunity"] = 5*speed
				timers["stickman_dodge_spam"] = 0
				timers["cutscene"] = 0
				timers["double_punch"] = 0
				timers["double_punch_spam"] = 0

			break
	if no_good_input:
		dnp.remove("Please write the level number")

	#tobor fight code:
	if fight_active:
		if two_tracker == 0:
			two_tracker = 1
			audio_both("TOBOR.wav",0.4,True,0)
		fake_console = []
		fake_print(frakenstein(import_sprite(f"{active_boss}/{active_boss}{tobor_state}.txt"),import_sprite(f"stickman/stickman{stickman_state}.txt")),idt=4)
		fake_print(f"   {tobor_hp} ♥ɹ     {stickman_hp} ♥ɹ     {status}",idt=4)

		if stickman_state == "_punch" and timers["stickman_punch"] == 0:
			stickman_state = "_ready"
		if tobor_state == "_damage" and timers["tobor_damage"] == 0:
			tobor_state = "_ready"
		if stickman_state == "_damage":
			stickman_state = "_ready"
		if tobor_state == "_miss" and timers["tobor_immunity"] == 0:
			tobor_state = "_ready"
		if tobor_hp <= 0:
			tobor_state = "_dead"
			status = "Y O U  W I N !"
			if active_boss == "tobor":
				progression_list[0] = 1
			elif active_boss == "gunman":
				progression_list[1] = 1
			timers["status_timer"] = 3*speed
		if stickman_hp <= 0:
			stickman_state = "_dead"
			status = "Y O U  L O S E !"
			timers["status_timer"] = speed
		if stickman_hp <= 0 or tobor_hp <= 0:
			if one_tracker == 0:
				one_tracker = 1
				timers["cutscene"] = 5*speed
			if timers["cutscene"] == 0:
				fight_active = False
				dnp = []
				fake_console = []
				two_tracker = 0
				stop_sounds()
		if timers["double_punch"] == 1:
			audio_both("sfx/stickman_punch.wav",0.6,False,1)
			tobor_hp -= 3
			stickman_state = "_punch"
			timers["stickman_punch"] = int(0.2*speed)

		if tobor_state == "_punch" and timers["tobor_punch"]	== 0:
			tobor_state = "_ready"
		if timers["player_immunity"] == 0 and tobor_state != "_dead" and stickman_state != "_dead":
			if randint(1,3) != 1:
				tobor_state = "_punch"
				timers["tobor_punch"] = speed
				if stickman_state == "_dodge":
					timers["player_immunity"]	= 4*speed
					stickman_state = "_good_dodge"
					status = "G R E A T  D O D G E"
					audio_both("sfx/great_dodge.wav",0.6,False,1)
					timers["status_timer"] = timers["stickman_dodge"]
				else:
					timers["player_immunity"]	= 4*speed
					stickman_hp -= 2
					stickman_state = "_damage"

		elif stickman_state in ["_dodge","_good_dodge"] and timers["stickman_dodge"] == 0:
			stickman_state = "_ready"

		if status and timers["status_timer"] == 0:
			status = ""

	linenum = 0
	charnum = 0
	charindex = 0
	if tutorial:
		bg_clr = (80,80,80)
		pygame.draw.rect(win,(255,255,255),(10,10,580,380),width=5)
		pygame.draw.rect(win,(155,155,155),(20,20,560,360),width=2)
		pygame.draw.rect(win,(65,65,65),(23,23,554,354),width=5)
		win.blit(mono_big.render("Tutorial:",True,(0,0,0)),(55,55))
		win.blit(mono_big.render("Tutorial:",True,(255,255,255)),(50,50))

		win.blit(mono_small.render(f"Page {tutorial_page} of {tutorial_pages}, press ENTER for next page, press ESC to exit.",True,(255,255,255)),(70,30))

		if tutorial_page == 1:
			win.blit(mono.render("Attack of the One-Handed Stickman is a",True,(235,235,235)),(30,100))
			win.blit(mono.render("fighting game, where the goal is to get the ",True,(235,235,235)),(30,120))
			win.blit(mono.render("enemy to 0 HP.",True,(235,235,235)),(30,140))

			win.blit(pygame.image.load("images/l_arrow.png"),(30,170))
			win.blit(mono.render("Press LEFT ARROW to hit the enemy!",True,(255,255,0)),(130,180))
			win.blit(mono.render(" - You cannot spam the key, or else ",True,(235,235,235)),(130,200))
			win.blit(mono.render("you will miss.",True,(235,235,235)),(130,220))
			win.blit(mono.render(" - Wait for the miss text to dissapear",True,(235,235,235)),(130,240))
			win.blit(mono.render("to know when you can hit again!",True,(235,235,235)),(130,260))

			win.blit(pygame.image.load("images/r_arrow.png"),(30,280))
			win.blit(mono.render("Press RIGHT ARROW to dodge!",True,(255,255,0)),(130,280))
			win.blit(mono.render(" - You cannot spam the key, or else ",True,(235,235,235)),(130,300))
			win.blit(mono.render("it won't work.",True,(235,235,235)),(130,320))
			win.blit(mono.render(" - You take no damage if the dodge",True,(235,235,235)),(130,340))
			win.blit(mono.render("works",True,(235,235,235)),(130,360))
		elif tutorial_page == 2:
			win.blit(pygame.image.load("images/l_arrow.png"),(30,80))
			win.blit(mono.render("Press UP ARROW to double punch!",True,(255,255,0)),(130,90))
			win.blit(mono.render(" - Only avalible on level 2 and up.",True,(235,235,235)),(130,110))
			win.blit(mono.render(" - Provides more damage at the cost",True,(235,235,235)),(130,130))
			win.blit(mono.render("of how often you can use it.",True,(235,235,235)),(130,150))

			win.blit(mono.render("Press F11 to resize the window!",True,(235,235,0)),(130,190))
			win.blit(mono.render("Press ESC to quit the game!",True,(235,235,0)),(130,210))
	else:
		for character in fake_console:
			char_clr = white
			if charindex in color_dict:
				char_clr = color_dict[charindex]
			if charnum == 48:
				win.blit(mono.render("—",True,char_clr),(5+fontsize*charnum,linenum*20-scroll))
				linenum += 1
				charnum = 0
			if character == "§":
				linenum += 1
				charnum = 0
				charindex += 1
			elif character in "ɹвɣʂɢ":
				onecolour = [(255,0,0),(66,135,245),(255,255,0),(255,87,51),(120,120,120)][["ɹ","в","ɣ","ʂ","ɢ"].index(character)] #satisfying efficiency...
				win.blit(mono.render(fake_console[charindex-1],True,(onecolour)),(5+fontsize*(charnum-1),linenum*20-scroll))
				charindex += 1
			elif linenum*20-scroll > -100:
				win.blit(mono.render(fake_console[charindex],True,(85,85,85)),(7+fontsize*charnum,linenum*20-scroll+2)) #This gives the text a drop shadow (renders it twice)
				win.blit(mono.render(fake_console[charindex],True,(char_clr)),(5+fontsize*charnum,linenum*20-scroll))

				charnum += 1
				charindex += 1
			else:
				charindex += 1
				charnum += 1

	max_scroll = linenum*20 - 380
	if max_scroll < 0:
		max_scroll = 0
	if scroll > max_scroll:
		scroll = max_scroll
	if max_scroll > 1:
		bar_length = 20/linenum*400
		scroll_rect = pygame.Rect(594,(400-bar_length)*(scroll/max_scroll),5,bar_length)
		pygame.draw.rect(win,white,scroll_rect,0)
	progression = sum(progression_list)

	for timer in timers:
		if timers[timer] != 0:
			timers[timer] -= 1
	true_win = pygame.display.set_mode((600*window_scale,400*window_scale)) #everything is blit'd onto a seperate surface before being blit'd onto the actual window. This allows me to scale it to whatever size I want.
	true_win.blit(pygame.transform.scale(win,(600*window_scale,400*window_scale)),(0,0))

	pygame.display.update()
	win.fill(bg_clr)
	clock.tick(30)
pygame.quit()
