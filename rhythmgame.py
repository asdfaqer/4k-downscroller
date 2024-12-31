# todo
# add song select
# add home screen with buttons
import pygame 


# initializing imported module 
pygame.init() 


# displaying a window of height 
# default resulotion
default_x=600
default_y=800

window = pygame.display.set_mode((default_x, default_y),pygame.RESIZABLE) 
  
window.fill((255, 255, 255))
# creating a bool value which checks 
# if game is running 
running = True

clock = pygame.time.Clock() 
# keep game running till running is true 
start = False
create_map = False
scroll_direction = "down"

key_channel = [
    [[2609, "n"], [3178, "n"], [3540, ["ln", 4359]]]
,   [[3981, "n"], [5072, "n"]]
,   [[4250, "n"], [4778, "n"]] 
,   [[4223, "n"], [4784, "n"]]
]

key_inx = [0, 0, 0, 0]

channel_to_key = {
    0: pygame.K_d,
    1: pygame.K_f,
    2: pygame.K_j,
    3: pygame.K_k
}

time_until_note_expires = 400
score = 0
total_hits = 0
font = pygame.font.Font('freesansbold.ttf', 32)
hit_judgement_text = font.render('', True, (0,255,0) , (0,0,128) )
hit_judgement = hit_judgement_text.get_rect()
hit_judgement.center = (default_x // 2, default_y // 2)
accarcy_text = font.render('100.00%', True, (0,255,0) )
accarcy_display = accarcy_text.get_rect()
accarcy_display.center = (default_x // 2, default_y // 2 + 50)
combo = 0
combo_text = font.render('0x', True, (0,255,0) )
combo_display = combo_text.get_rect()
combo_display.center = (50, default_y-50)
frame_counter_text = font.render('60fps', True, (0,255,0))
frame_counter_display = frame_counter_text.get_rect()
frame_counter_display.center = (default_x - 50, default_y - 50)
time_elapsed = None
hit_releases = 0

channel_release_expected = [False, False, False, False]

def determine_hit_judgement(channel, time_desired, note_type):
    global channel_release_expected, key_inx

    # note_type is a list when its a long note
    if isinstance(note_type, list):
        channel_release_expected[channel] = note_type[1]
        key_inx[channel] -= 1

    if abs(time_desired - time_elapsed) < 350:
        # time_elapsed within 300 ms of desired is a hit
        if abs(time_desired - time_elapsed) < 300:

            if abs(time_desired - time_elapsed) < 100:

                if abs(time_desired - time_elapsed) < 50:
                    return "perfect"
                
                return "good"
            
            return "okay"
        
        return "miss"
    
    return "not hit or miss"

def determine_release_judgement(channel, time_desired):
    global channel_release_expected, key_inx, hit_releases

    key_inx[channel] += 1
    channel_release_expected[channel] = False
    # if within 300 ms of expected release perfect otherwise miss
    if abs(time_desired - time_elapsed) < 300:
        hit_releases += 1
        return "perfect"
    return "miss"
    
def display_game_elements():
    global accarcy_text, combo_text
    clock.tick(120)
    window.fill((255, 255, 255))
    if scroll_direction == "up":
        pygame.draw.rect(window, (0, 0, 255), 
        [100, 0, 400, 90], 1)
    elif scroll_direction == "down":
        pygame.draw.rect(window, (0, 0, 255), 
        [100, default_y - 90, 400, default_y], 1)
    hit_judgement = hit_judgement_text.get_rect()
    hit_judgement.center = (default_x // 2, default_y // 2)
    accarcy_display = accarcy_text.get_rect()
    accarcy_display.center = (default_x // 2, default_y // 2 + 50)
    combo_display = combo_text.get_rect()
    combo_display.center = (50, default_y-50)
    window.blit(hit_judgement_text, hit_judgement)
    frame_counter_text = font.render(str(round(clock.get_fps())) + "fps", True, (0,255,0))
    frame_counter_display = frame_counter_text.get_rect()
    frame_counter_display.center = (default_x - 50, default_y - 50)
    window.blit(frame_counter_text, frame_counter_display)
    if total_hits != 0:
        accarcy_text = font.render(str(round(score/((total_hits + hit_releases)*3) * 10000)/100)+"%", True, (0,255,0) )
        combo_text = font.render(str(combo) + "x", True, (0,255,0) )
        window.blit(accarcy_text, accarcy_display)
        window.blit(combo_text,combo_display)

def check_key_channel_hit(event):
    global score, key_inx, total_hits, hit_judgement_text, combo, channel_to_key

    for channel, key in channel_to_key.items():
        if event.key == key:

            # check if the key_channel is completed if not proceed
            if key_inx[channel] >= len(key_channel[channel]):
                continue

            time_elapsed = pygame.time.get_ticks() - start_time
            time_desired = key_channel[channel][key_inx[channel]][0]
            note_type = key_channel[channel][key_inx[channel]][1]

            print(time_elapsed - time_desired)

            type_of_hit = determine_hit_judgement(channel, time_desired, note_type)

            print("hit key 1 and type of hit " + type_of_hit)
            if type_of_hit != "not hit or miss":
                key_inx[channel] += 1
                total_hits += 1

            if type_of_hit == "perfect":
                
                hit_judgement_text = font.render('perfect', True, (0,128,255))

                #change the score and combo
                score += 3 
                combo += 1

            elif type_of_hit == "good":

                hit_judgement_text = font.render('good', True, (0,255,0) )
                score += 2
                combo += 1

            elif type_of_hit == "okay":

                hit_judgement_text = font.render('okay', True, (128,128,0) )
                score += 1
                combo += 1

            elif type_of_hit == "miss":

                hit_judgement_text = font.render('miss', True, (255,0,0) )
                score += 0
                combo = 0

def check_key_channel_release(event):
    global channel_release_expected, channel_to_key, hit_judgement_text, total_hits, combo, score
    for channel, key in channel_to_key.items():
        if event.key == key:

            if channel_release_expected[channel] == False:
                continue

            time_elapsed = pygame.time.get_ticks() - start_time

            print(channel_release_expected[channel])
            print(time_elapsed - channel_release_expected[channel])

            type_of_release = determine_release_judgement(channel, channel_release_expected[channel])

            print("release key 1 and type of release " + type_of_release)

            if type_of_release == "perfect":

                hit_judgement_text = font.render('perfect', True, (0,128,255))

                score += 3 
                combo += 1

            elif type_of_release == "miss":

                hit_judgement_text = font.render('miss', True, (255,0,0) )

                score += 0
                combo = 0
            

while running: 
    
    if start == True:

        #display game
        display_game_elements()

        #game logic
        time_elapsed = pygame.time.get_ticks() - start_time

        if scroll_direction == "up":

            for i in channel_to_key.keys():
                for j in range(key_inx[i], len(key_channel[i])):
                    note_distance = (key_channel[i][j][0] - time_elapsed) / 2 # time_until_note * scroll_distance_per_unit
                    note_type = key_channel[i][j][1]
                    if note_distance <= 1090:
                        # note_type is a list when its a long note
                        if isinstance(note_type, list):
                            note_length = (note_type[1] - key_channel[i][j][0]) / 2
                            pygame.draw.rect(window, (0, 0, 255), 
                                [100*(i + 1), note_distance, 90, note_length], 0)
                        else:
                            pygame.draw.rect(window, (0, 0, 255), 
                                [100*(i + 1), note_distance, 90, 90], 0)
                    else:
                        break

        elif scroll_direction == "down":

            for i in channel_to_key.keys():
                for j in range(key_inx[i], len(key_channel[i])):
                    note_distance = (key_channel[i][j][0] - time_elapsed) / 2 # time_until_note * scroll_distance_per_unit
                    note_type = key_channel[i][j][1]
                    if note_distance <= 1090:
                        # note_type is a list when its a long note
                        if isinstance(note_type, list):
                            note_length = (note_type[1] - key_channel[i][j][0]) / 2
                            pygame.draw.rect(window, (0, 0, 255), 
                                [100*(i + 1), default_y - note_distance - note_length, 90, note_length], 0)
                        else:
                            pygame.draw.rect(window, (0, 0, 255), 
                                [100*(i + 1), default_y - note_distance - 90, 90, 90], 0)
                    else:
                        break

        for i in channel_to_key.keys():
            if len(key_channel[i]) > key_inx[i]:
                note_type = key_channel[i][key_inx[i]][1]
                # note_type is a list when its a long note
                if isinstance(note_type, list):
                    if(time_elapsed > note_type[1] + time_until_note_expires):
                        combo = 0
                        total_hits += 1
                        key_inx[i] += 1
                        hit_judgement_text = font.render('miss', True, (255,0,0) )

                elif (time_elapsed > key_channel[i][key_inx[i]][0] + time_until_note_expires):
                    combo = 0
                    total_hits += 1
                    key_inx[i] += 1
                    hit_judgement_text = font.render('miss', True, (255,0,0) )

        if combo == len(key_channel[0]) + len(key_channel[1]) + len(key_channel[2]) + len(key_channel[3]) + hit_releases:
            hit_judgement_text = font.render('full combo', True, (0,128,255))

    # Check for event if user has pushed 
    # any event in queue 
    for event in pygame.event.get(): 
          
        # if event is of type quit then  
        # set running bool to false 
        if event.type == pygame.QUIT: 
            running = False
        
        if start == True:

            if event.type == pygame.KEYDOWN:

                #check if key_channel hit
                check_key_channel_hit(event)
                
                if event.key == pygame.K_r:
                    key_inx[0] = 0
                    key_inx[1] = 0
                    key_inx[2] = 0
                    key_inx[3] = 0
                    score = 0
                    total_hits = 0
                    combo = 0   
                    start = False
            
            if event.type == pygame.KEYUP:

                #check if key_channel release
                check_key_channel_release(event)

        elif create_map:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    time_elapsed = pygame.time.get_ticks() - start_time
                    key_channel[0].append(time_elapsed)
                if event.key == pygame.K_f:
                    time_elapsed = pygame.time.get_ticks() - start_time
                    key_channel[1].append(time_elapsed)
                if event.key == pygame.K_j:
                    time_elapsed = pygame.time.get_ticks() - start_time
                    key_channel[2].append(time_elapsed)
                if event.key == pygame.K_k:
                    time_elapsed = pygame.time.get_ticks() - start_time
                    key_channel[3].append(time_elapsed)
                if event.key == pygame.K_m:
                    print(key_channel[0])
                    print(key_channel[1])
                    print(key_channel[2])
                    print(key_channel[3])
                    create_map = False
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    print("starting")
                    pygame.mixer.music.load('default_music.mp3')
                    pygame.mixer.music.play(0)
                    start_time = pygame.time.get_ticks()
                    start = True
                if event.key == pygame.K_m:
                    print("maping")
                    pygame.mixer.music.load('default_music.mp3')
                    pygame.mixer.music.play(0)
                    key_channel[0] = []
                    key_channel[1] = []
                    key_channel[2] = []
                    key_channel[3] = []
                    start_time = pygame.time.get_ticks()
                    create_map = True
                   
    pygame.display.flip()

