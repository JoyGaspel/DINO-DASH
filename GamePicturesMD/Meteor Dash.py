import pygame
import sys
import random
import json
import os
import math

pygame.init()
pygame.mixer.init()  # Initialize the mixer for music
win = pygame.display.set_mode((1000, 700))  # Create the game window
pygame.display.set_caption("Meteor Dash")  # Set the window title

# Directs kung saan yung textures & leaderboards 
assets_directory = os.path.join(os.path.dirname(__file__), "textures")
leaderboard_file = os.path.join(assets_directory, "leaderboard.json")

# Function to randomly spawn a power-up (either Hyperspeed or Shield) - KEN ANDRE
def spawnPowerUp():
    if random.choice([True, False]):
        print("Hyperspeed Power-Up Spawned!")
        return FallingPowerups()
    else:
        print("Shield Power-Up Spawned!")
        return FallingShield()

# variable to check score to spawn powerup - KEN ANDRE
last_powerup_score = -1

# Textures Loader - loads the an specific image/music when called this function
def load_image(filename): #for image
    return pygame.image.load(os.path.join(assets_directory, "images", filename))
def load_music(filename): #for musics
    return pygame.mixer.music.load(os.path.join(assets_directory, "music", filename))
def load_font(font_name, size):
    return pygame.font.Font(os.path.join(assets_directory, "fonts", font_name), size)

# LEADERBOARDS CODE FUNCTIONS
# Colors settings
White = (255, 255, 255)
Black = (0, 0, 0)
Red = (255, 0, 0)
Gold = (255,191,0)
Blue = (25,25,112)

clock = pygame.time.Clock()  # Allows us to change the fps of the game

# Characters scale and position settings
char_w, char_h = 100, 75
char_x, char_y = 400, 465
player_speed = 10

# Background
bg_w, bg_h = 1000, 900
bg_x, bg_y = 0, -260
leaderboard_bg_x ,leaderboard_bg_y= 0, 0
leaderboard_bg_w ,leaderboard_bg_h= 1000, 700
control_menubg_x ,control_menubg_y= 0, 0
control_menubg_w ,control_menubg_h= 1000, 700
g_o_w, g_o_h = 1000, 700
countdown_w, countdown_h = 1000, 700

# Terrain 
trn_w, trn_h = 1000, 700
trn_x, trn_y = 0, 25

# Start menu
sm_w, sm_h = 1000, 700

# Start menu text
dt_x, dt_y = 275, 150
dt_x2, dt_y2 = 100, 600
dt_x3, dt_y3 = 355, 240
dt_x4, dt_y4 = 20, 645

# Game over text
gt_x, gt_y = 150, 250
gt_x2, gt_y2 = 400, 350
gt_x3, gt_y3 = 200, 600
leaderboard_x ,leaderboard_y = 400, 350
control_menu_x ,control_menu_y = 350, 250
retry_and_menu_x, retry_and_menu_y= 90, 570

# Game variables
gameover = False
left = False
right = False
walkCount = 0
score = 0
is_jumping = False
jump_vel = 15 
gravity = 1
control=True

# Dash Settings
is_dashing = False
dash_speed = 15
dash_duration = 500  # This is in milliseconds
dash_cooldown = 3000  # This is in milliseconds, so 3 seconds
last_dash_time = 0
dash_end_time = 0
dash_direction = 1  # 1 for right, -1 for left

# Power up setthings and invincibility
invincible = False
invincibility_timer = 0
last_invincibility_score = 0

next_powerup = 500
hyperspeed = False
hyperspeed_timer = 0
current_powerup = None  # Initialize current_powerup as None

shield_duration = 900
shield_timer = 0
current_shield = None # List if theres an shield powerup in the game

# Background music ng game
load_music("menu music.mp3") 

# Load sound effects
dash_sound = pygame.mixer.Sound(os.path.join(assets_directory, "music", "Dashsound.wav")) # Load dash sound effect
invincibility_sound = pygame.mixer.Sound(os.path.join(assets_directory, "music", "invincibilitysound.wav"))  # Load invincibility sound effect
parry_sound = pygame.mixer.Sound(os.path.join(assets_directory, "music", "parrysound.wav")) #parry sound 
gameover_sound = pygame.mixer.Sound(os.path.join(assets_directory, "music", "gameoverSound.wav")) # Gameover sound
powerup_sound = pygame.mixer.Sound(os.path.join(assets_directory, "music", "powerupsound.wav")) # powerup sound
shieldbreaking_sound = pygame.mixer.Sound(os.path.join(assets_directory, "music", "shieldbreaksound.wav")) # Shield breaking sound


# Load images
bg = load_image("bg.png")
bg = pygame.transform.scale(bg, (bg_w, bg_h))

sm = load_image("startmenubg.png")
sm = pygame.transform.scale(sm, (sm_w, sm_h))

trn = load_image("new terrain.png")
trn = pygame.transform.scale(trn, (trn_w, trn_h - 25))

cm = load_image("LB_2.png")
cm = pygame.transform.scale(cm, (control_menubg_w, control_menubg_h))

lb = load_image("LEADERBOARD.png")
lb = pygame.transform.scale(lb, (leaderboard_bg_w, leaderboard_bg_h))

g_o= load_image("GAMEOVER.png")
g_o= pygame.transform.scale(g_o, (g_o_w, g_o_h))

countdown_bg=load_image("GAMEOVER.png")
countdown_bg=pygame.transform.scale(countdown_bg,(countdown_w,countdown_h))

# Animation walking
walkRight = [load_image("r1.png"), load_image("r2.png"), load_image("r3.png"),
             load_image("r4.png"), load_image("r1.png"), load_image("r5.png"),
             load_image("r6.png"), load_image("r7.png"), load_image("r8.png"),
             load_image("r9.png"), load_image("r1.png")]
walkLeft = [load_image("l1.png"), load_image("l2.png"), load_image("l3.png"),
            load_image("l4.png"), load_image("l1.png"), load_image("l5.png"), 
            load_image("l6.png"), load_image("l7.png"), load_image("l8.png"),
            load_image("l9.png"), load_image("l1.png")]
stand = load_image("standing.png")

walkRighthyper = [load_image("rh1.png"), load_image("rh2.png"), load_image("rh3.png"),
             load_image("rh4.png"), load_image("rh1.png"), load_image("rh5.png"),
             load_image("rh6.png"), load_image("rh7.png"), load_image("rh8.png"),
             load_image("rh9.png"), load_image("rh1.png")]
walkLefthyper = [load_image("lh1.png"), load_image("l2.png"), load_image("lh3.png"),
            load_image("lh4.png"), load_image("lh1.png"), load_image("lh5.png"), 
            load_image("lh6.png"), load_image("lh7.png"), load_image("lh8.png"),
            load_image("lh9.png"), load_image("lh1.png")]
standhyper = load_image("standinghyper.png")

# Meteors and Powerup images
falling_object = load_image("meteor.png")
falling_object2 = load_image("hyperspeed.png")
falling_shield = load_image("shield.png")
shieldeffect = load_image("shieldeffect.png")
star_images = [load_image("bigstar.png"), load_image("midstar.png"), load_image("smalstar.png")]

# Font settings
game_name_font = load_font('04b_30.ttf', 90)
font2 = load_font('04b_30.ttf', 25)
font3 = load_font('SuperShiny.ttf', 25)
control_font = load_font('04b_30.ttf', 45)
warning_text = load_font('SuperShiny.ttf', 15)
menu_font = load_font('SuperShiny.ttf', 25)
name_box_font = load_font('SuperShiny.ttf', 25)
button_font = load_font('TyposterROCK-ONDemo.otf', 25)
game_over_font = load_font('04b_30.ttf', 90)
leaderboard_font = load_font('SuperShiny.ttf', 90)
leaderboard_font2 = load_font('SuperShiny.ttf', 45)

# Visual Effects VFXs for Powers and invincibility - MARK ANGELO
# Invincibility VFX - Stars and glitterings on dino when invincible. 
class InvincibleVFX:
    def __init__(self, x, y):
        self.stars = [
            {"x": x + random.randint(0, char_w), "y": y + random.randint(0, char_h  + 100), "stage": 0, "delay": 0}
            for _ in range(random.randint(3, 4))
        ]

    def update(self):
        for star in self.stars:
            if star["delay"] > 50:  # Delay factor, adjust to control speed
                star["stage"] += 1
                star["delay"] = 0
            else:
                star["delay"] += 1
            
            if star["stage"] >= 3:
                self.stars.remove(star)

    def draw(self, surface):
        for star in self.stars:
            surface.blit(star_images[star["stage"]], (star["x"], star["y"]))

# Function to display text
def draw_text(surface, text, position, font, color):
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, position)
# Start menu settings
def start_menu():
    global player_name, show_controls
    menu = True
    player_name = ""     # PLAYER NAME VARIABLE
    input_active = False  #UWU: Track if input box is active
    name_box_rect = pygame.Rect(350, 430, 200, 40)  # Name input box area
    check_button_rect = pygame.Rect(540, 430, 80, 40)  # Check button position
    show_controls = False 
    no_input_name_warning=False
    max_input_length = 15  # Maximum characters for player name
    pygame.mixer.music.play(-1)

    while menu:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if input_active and event.key == pygame.K_BACKSPACE:  #UWU: Allow backspace
                    player_name = player_name[:-1]

                elif input_active and len(player_name) < max_input_length:
                     player_name += event.unicode  #UWU: Add character to player name
                if event.key == pygame.K_e and not input_active:
                    if player_name:
                        menu = False  
                        load_music("bgmusicV2.mp3")
                        pygame.mixer.music.play(score)
                    else:
                        no_input_name_warning=True #need to enter name first        
                    
                if event.key == pygame.K_c and not input_active:  # Open control menu when "2" is pressed
                    show_controls= not show_controls 
                    no_input_name_warning= not no_input_name_warning
                    no_input_name_warning=False
               
                

            # Activate input box with left-click
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # left-click
                    if name_box_rect.collidepoint(event.pos):
                        input_active = True  # Activate input box
                       
        
                # Save player name with check button
                if check_button_rect.collidepoint(event.pos):
                    input_active = False  # Deactivate input after checkinhg
                    print(f"Player name saved as: {player_name}")  # For debugging 

               


        # Draw menu elements
        win.blit(sm, (0, 0))
        draw_text(win, "Meteor", (dt_x, dt_y), game_name_font, Black)
        draw_text(win, "Dash", (dt_x3, dt_y3), game_name_font, Black)
        draw_text(win, "Press '[E]' to Start", (dt_x2 - 80, dt_y2), menu_font, Black)
        draw_text(win, "Enter Your Name:", (350, 410), menu_font, Black)
        draw_text(win, "Press '[C]' to show Controls", (dt_x4, dt_y4), menu_font, Black)

        #: Draw name input box
        pygame.draw.rect(win, White if input_active else (211,211,211), name_box_rect, 0)
        draw_text(win, player_name, (name_box_rect.x + 5, name_box_rect.y + 5), name_box_font, Black)

        # Draw check button
        # Get mouse position and button state
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()[0]  # Left mouse button
        is_hovering = check_button_rect.collidepoint(mouse_pos)
        button_color_clicked=(Red)
        button_color_default=(White)
        button_color=button_color_clicked if is_hovering and mouse_click else button_color_default
        pygame.draw.rect(win, button_color, check_button_rect)
        draw_text(win, "Enter", (check_button_rect.x + 4, check_button_rect.y + 10), button_font, Black)

        if no_input_name_warning:
            draw_text(win, "Please enter your name to start", (350, 475), warning_text, Red)

        if show_controls:
            win.blit(cm, (control_menubg_x, control_menubg_y, control_menubg_w, control_menubg_h))

            draw_text(win, "CONTROLS:", (control_menu_x-13 , control_menu_y-80), control_font, Black)
            draw_text(win, "< >: Left and Right Movement", (control_menu_x, control_menu_y+50), font3, Black)
            draw_text(win, " ^ : Jump Movement", (control_menu_x, control_menu_y+100), font3, Black)
            draw_text(win, " SPACE : Dash Skill ", (control_menu_x, control_menu_y+150), font3, Black)

        pygame.display.update()

# ditoo po ilalagay cpuntdown
def countdown(screen):
    font = pygame.font.Font(None, 120)  # Choose font and size for countdown text
    for i in range(3, 0, -1):
        screen.blit(bg, (0, 0))  # Draw the background image
        text = font.render(str(i), True, (255, 255, 255))  # Render countdown number
        text_rect = text.get_rect(center=(500, 350))  # Center text on screen
        screen.blit(text, text_rect)
        pygame.display.update()
        pygame.time.delay(1000)  # Wait 1 second

    # Display "Go!" before starting the game
    screen.blit(bg, (0, 0))  # Draw the background image
    text = font.render("Dash it,\nSurvive it. \nAvoid the meteors.", True, (255, 255, 255))
    text_rect = text.get_rect(center=(500, 350))
    screen.blit(text, text_rect)
    pygame.display.update()
    pygame.time.delay(1500)  # Wait 1.5 seconds before game starts

# Function to redraw the game window
# Define player_speed and normal_speed for clarity

normal_speed = player_speed  # Store the player's normal speed for easy reset

def redrawGameWindow():
    global walkCount, player_speed, score, hitbox, invincible, invincibility_timer, last_invincibility_score, next_powerup, current_powerup
    global dash_cooldown, hyperspeed, hyperspeed_timer, shield, shield_timer, shield_duration, current_shield

    win.blit(bg, (bg_x, bg_y - 10))  # Draw background
    win.blit(trn, (trn_x, trn_y))  # Draw terrain
    win.blit(g_o, (g_o_w, g_o_h)) #game over

    # Character animation
    if hyperspeed:                                               # Hyperspeed animation
        if left:
            win.blit(walkLefthyper[walkCount // 2], (char_x, char_y+20))
        elif right:
            win.blit(walkRighthyper[walkCount // 2], (char_x, char_y+20))
        else:
            win.blit(standhyper, (char_x, char_y+20))
    else:                                                       # Default Character animation
        if left:
            win.blit(walkLeft[walkCount // 2], (char_x, char_y))
        elif right:
            win.blit(walkRight[walkCount // 2], (char_x, char_y))
        else:
            win.blit(stand, (char_x, char_y))

    if shield_timer:
        win.blit(shieldeffect, (char_x, char_y))

    hitbox = (char_x + 25, char_y + 20, char_w - 5, char_h + 60)  # Hitbox
    # pygame.draw.rect(win, (255, 0, 0), hitbox, 3)

    # Draw meteors and check for collisions
    for meteor in meteors:
        meteor.fall()
        meteor.draw()
        # Check if hit only if not invincible
        if meteor.hit(char_x, char_y, char_w, char_h):
            if invincible:
                parry_sound.play()
                score += 20
                distances = [meteor.distance_to(char_x, char_y) for meteor in meteors]
                closest_meteor_index = distances.index(min(distances))
                meteors.pop(closest_meteor_index)
                if len(meteors) < 3:
                    meteors.append(FallingObject())
            elif shield_timer:
                shieldbreaking_sound.play()
                shield_timer = 0
                distances = [meteor.distance_to(char_x, char_y) for meteor in meteors]
                closest_meteor_index = distances.index(min(distances))
                meteors.pop(closest_meteor_index)
                if len(meteors) < 3:
                    meteors.append(FallingObject())
            else:
                global gameover
                gameover = True
                break  # Exit the loop once a hit is detected

    # Score and display updates
    if not gameover:
        score += 1  # Increment score if the game is not over
        draw_text(win, f"Score: {score}", (10, 10), font2, Black)
        if hyperspeed:
                draw_text(win, f"Hyperspeed! : {hyperspeed_timer // 60}", (680, 40), font2, Red)
        if invincible:
                draw_text(win, f"INVINCIBLE! : {invincibility_timer // 60}", (680, 10), font2, Gold)
        if shield_timer:
                draw_text(win, f"Shield : {shield_timer // 60}", (730, 70), font2, Blue)

        # PowerUP Spawning Code
        # Check if it's time to spawn a new random power-up
        if score >= next_powerup and not current_powerup and not current_shield:
            new_powerup = spawnPowerUp()
            if isinstance(new_powerup, FallingShield):
                current_shield = new_powerup
            else:
                current_powerup = new_powerup # Create and store new power-up
            next_powerup += 500  # Set the next spawn threshold

        # Shield Features
        # If a power-up is active, update its position and draw it
        if current_shield:
            current_shield.fall()
            current_shield.draw()

            # Check for collision with the player
            if current_shield.hit(char_x, char_y, char_w, char_h):
                powerup_sound.play()
                current_shield = None  # Remove power-up after collection
                shield_timer = shield_duration  # Set the timer for shield duration (10 seconds)

            # Check if the power-up goes off the screen (e.g., falls past the bottom of the screen)
            elif current_shield.y > 700:  # Adjust this value based on screen height
                current_shield = None  # Remove power-up if it goes off the screen
        
        if shield_timer:
            shield_timer -= 1

        # Hyperspeed Features
        # If a power-up is active, update its position and draw it
        if current_powerup:
            current_powerup.fall()
            current_powerup.draw()

            # Check for collision with the player
            if current_powerup.hit(char_x, char_y, char_w, char_h):
                powerup_sound.play()
                player_speed += 18  # Apply speed boost to player
                current_powerup = None  # Remove power-up after collection
                hyperspeed_timer = 300  # Set the timer for hyperspeed duration (e.g., 5 seconds at 60 FPS)
                hyperspeed = True  # Activate hyperspeed

            # Check if the power-up goes off the screen (e.g., falls past the bottom of the screen)
            elif current_powerup.y > 700:  # Adjust this value based on screen height
                current_powerup = None  # Remove power-up if it goes off the screen

        # If hyperspeed is active, show the timer and update the speed
        if hyperspeed:
            hyperspeed_timer -= 1  # Decrease the timer each frame
            if hyperspeed_timer <= 0:  # If the timer reaches 0
                hyperspeed = False  # Turn off hyperspeed
                player_speed = normal_speed  # Reset player speed to normal

        # Invincible features
        invincible_effect = InvincibleVFX(char_x, char_y)
        if score == last_invincibility_score + 1000:
            invincibility_sound.play()
            parry_display_time = 60
            invincible = True
            invincibility_timer = 5 * 60  # Set invincibility duration
            last_invincibility_score = score
        if invincible:
            invincibility_timer -= 1  # Reduce timer by 1 each frame
            parry_position = (char_x, char_y - 20)
            draw_text(win, "PARRY!!", parry_position, font2, Gold)
            invincible_effect.update()
            invincible_effect.draw(win)
            if invincibility_timer <= 0:
                invincible = False  # Turn off invincibility when timer runs out

    walkCount += 1  # Increment walkCount for animation
    if walkCount >= 18:  # Reset walkCount for animation
        walkCount = 0

    # Dash and hyperspeed cooldown display
    if pygame.time.get_ticks() - last_dash_time < dash_cooldown:
        remaining = dash_cooldown - (pygame.time.get_ticks() - last_dash_time)
        remaining_s = remaining / 1000
        draw_text(win, f"Dash Cooldown: {remaining_s:.1f}s", (10, 40), font2, Red)

    pygame.display.update()  # Update the display  

# Meteor settings
class FallingObject():
    def __init__(self):
        self.x = random.randint(0, 1000 - 50)  # Random position 
        self.y = -50  # Start above the screen
        self.speed = 10  # Random falling speed
        self.size=random.randint(50, 120)
       
    def fall(self):
        self.y += self.speed  # Move the meteor down by speed
        if self.y > 600:  
            self.y = -50
            self.x = random.randint(0, 1000 - 50)
            self.speed=10 + score//500 #speed increase every 500 points
            self.size=random.randint(50, 120)
           
    def draw(self):
        scaled_image = pygame.transform.scale(falling_object, (self.size, self.size))
        win.blit(scaled_image, (self.x, self.y))

    def hit(self, player_x, player_y, player_w, player_h):
        return (self.x < player_x + player_w and self.x + 50 > player_x and
                self.y + 50 >= player_y and self.y <= player_y + player_h)  
    
    def distance_to(self, player_x, player_y):
        # Calculate Euclidean distance to character
        return math.sqrt((self.x - player_x) ** 2 + (self.y - player_y) ** 2)
last_size_change = pygame.time.get_ticks()   

# Hyperspeed settings
class FallingPowerups:
    def __init__(self):
        # Initialize x, y, and size attributes
        self.x = random.randint(0, 1000 - 50)  # Random starting x-position
        self.y = -50  # Start above the screen
        self.size = 80 
        self.speed = 5  # Falling speed

    def fall(self):
        # Make the power-up fall down
        self.y += self.speed  # Update y position based on speed

        # Reset position if it falls below the screen
        if self.y > 600:  
            self.y = -50  # Reset to above the screen
            self.x = random.randint(0, 1000 - 50)  # New random x-position
            self.size = 80  

    def draw(self):
        # Draw the power-up on the screen with the updated size
        scaled_image = pygame.transform.scale(falling_object2, (self.size, self.size))
        win.blit(scaled_image, (self.x, self.y))

    def hit(self, player_x, player_y, player_w, player_h):
        # Check if the power-up collides with the player
        return (self.x < player_x + player_w and self.x + self.size > player_x and
                self.y + self.size >= player_y and self.y <= player_y + player_h)

    def distance_to(self, player_x, player_y):
        # Calculate Euclidean distance to the player character
        return math.sqrt((self.x - player_x) ** 2 + (self.y - player_y) ** 2)
    
#powerup shield - ANGELO
class FallingShield:
    def __init__(self):
        # Initialize x, y, and size attributes
        self.x = random.randint(0, 1000 - 50)  # Random starting x-position
        self.y = -50  # Start above the screen
        self.size = 80 
        self.speed = 5  # Falling speed

    def fall(self):
        # Make the power-up fall down
        self.y += self.speed  # Update y position based on speed

    def draw(self):
        # Draw the power-up on the screen with the updated size
        scaled_image = pygame.transform.scale(falling_shield, (self.size, self.size))
        win.blit(scaled_image, (self.x, self.y))

    def hit(self, player_x, player_y, player_w, player_h):
        # Check if the power-up collides with the player
        return (self.x < player_x + player_w and self.x + self.size > player_x and
                self.y + self.size >= player_y and self.y <= player_y + player_h)

    def distance_to(self, player_x, player_y):
        # Calculate Euclidean distance to the player character
        return math.sqrt((self.x - player_x) ** 2 + (self.y - player_y) ** 2)

# Create meteors aand powerups
meteors = [FallingObject() for i in range(3)]  # Customize the number of meteors
powerups = [FallingPowerups() for i in range(1)] 
shield = [FallingShield() for i in range(1)] 
    

# Game over settings
# Initialize toggle for leaderboard visibility
# Save and Load Leaderboard - Loading and saving player names in leaderboard
def load_leaderboard():
    if os.path.exists(leaderboard_file):
        with open(leaderboard_file, 'r') as f:
            return json.load(f)
    else:
        return []
def save_leaderboard(leaderboard):
    with open(leaderboard_file, 'w') as f:
        json.dump(leaderboard, f)

# Updating function - function to call to update leaderboard to check kung mayroon bagong highscore
def update_leaderboard(player_name, score):
    leaderboard = load_leaderboard()
    player_found=False
    for entry in leaderboard:
        if entry["name"] == player_name:
            if score>entry["score"]:
                entry["score"]=score
            player_found=True
            break   
        
    # Add new score and sort the leaderboard by score in descending order
    if not player_found:
        leaderboard.append({"name": player_name, "score": score})   
    leaderboard = sorted(leaderboard, key=lambda x: x["score"], reverse=True)[:5]
    
    save_leaderboard(leaderboard)

    # Check if the player achieved a high score
    is_high_score = leaderboard[0]["name"] == player_name and leaderboard[0]["score"] == score
    return is_high_score

# Display Leaderboard
def show_leaderboard(surface, font):
    leaderboard = load_leaderboard()
    # Display title
    title = font.render("Leaderboard", True, (0, 0, 0))
    surface.blit(title, (leaderboard_x, leaderboard_y))

    # Display the top 5 scores
    for i, entry in enumerate(leaderboard):
        text = f"{i+1}. {entry['name']} - {entry['score']}"
        entry_text = font.render(text, True, (0, 0, 0))
        surface.blit(entry_text, (350, 200+i*40))

    pygame.display.update()
show_leaderboard = False

def game_over_screen():
    global gameover, char_x, score, show_leaderboard, score, player_name
    pygame.mixer.music.stop()
    gameover_sound.play()
    if update_leaderboard(player_name,score):#update leaderboard
        print(f"New High Score for {player_name} with score{score}")
    # Game over loop
    while gameover:
        win.blit(g_o, (0, 0))
        draw_text(win, "Game Over", (gt_x, gt_y), game_over_font, (255, 0, 0))
        draw_text(win, f"Score: {score}", (gt_x2, gt_y2), font2, Black)
        draw_text(win, "R - Retry", (retry_and_menu_x+175, retry_and_menu_y+10), font2, Black)
        draw_text(win, "M - Menu", (retry_and_menu_x+475, retry_and_menu_y+10), font2, Black)
        draw_text(win, "L - Toggle Leaderboard", (gt_x3+70, gt_y3+40), font2, Black)  # Toggle message

        # Display leaderboard if toggled on
        if show_leaderboard:
            win.blit(lb, (leaderboard_bg_x, leaderboard_bg_y))

            leaderboard = load_leaderboard()
            draw_text(win, "LEADERBOARDS", (leaderboard_x-150, leaderboard_y-150),leaderboard_font, Black)
            for i, entry in enumerate(leaderboard):
                entry_text = f"{i + 1}. {entry['name']} - {entry['score']}"
                draw_text(win, entry_text, (leaderboard_x-40, leaderboard_y -30 + i * 50), leaderboard_font2, Black)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Retry game
                    reset_game()
                    pygame.mixer.music.play()
                    countdown(win)
                elif event.key == pygame.K_m:  # back to start menu and play another game
                    load_music("menu music.mp3")
                    pygame.mixer.music.play(-1)
                    start_menu()
                    reset_game()
                    countdown(win)
                elif event.key == pygame.K_l:  # Toggle leaderboard visibility
                    show_leaderboard = not show_leaderboard
                


        pygame.display.update()  # Update the display

# Reset game settings
def reset_game():
    global char_x, current_powerup, next_powerup, char_y, score, gameover, left, right, walkCount, is_dashing, last_dash_time, invincible, is_jumping, jump_vel, meteors,powerups, hyperspeed, hyperspeed_timer, player_speed, shield, shield_timer, current_shield
    
    score = 0  # Reset score
    gameover = False  # Reset gameover state
    left = False
    right = False
    walkCount = 0

    hyperspeed= False
    hyperspeed_timer = 0
    player_speed=normal_speed
    current_powerup=None
    current_shield=None
    next_powerup=500

    is_dashing = False
    last_dash_time = 0  # Reset dash time

    invincible = False  # Reset invincibility
    invincibility_timer = 0
    last_invincibility_score = 0

    is_jumping = False  # Reset jumping state
    jump_vel = 15
    char_x, char_y= 400, 465 #reset ng position

    meteors=[FallingObject() for i in range(3)]#reset ng meteor
    powerups=[FallingPowerups() for i in range(1)] #reset ng meteor
    shield = [FallingShield() for i in range(1)] 

# Start the game
start_menu()  # Show start menu
countdown(win)  # Show countdown once before the main loop starts
while True:
    clock.tick(60)
    for event in pygame.event.get():  
            
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()  # Get the state of keys

    # Movement controls
    if keys[pygame.K_LEFT] and char_x > player_speed:
        left = True
        right = False
        char_x -= player_speed  # Move left
        dash_direction=-1

    elif keys[pygame.K_RIGHT] and char_x < 1000 - char_w - player_speed:
        right = True
        left = False
        char_x += player_speed  # Move right
        dash_direction=1
 
    else:
        left = False
        right = False

    if not is_jumping:
        if keys[pygame.K_UP]:  # Start jump
            is_jumping = True
    else:
        char_y -= jump_vel 
        jump_vel -= gravity  
        if jump_vel < -15: 
            is_jumping = False
            jump_vel = 15
            char_y = 465 
     # Call the function to redraw the game window
    redrawGameWindow()
    pygame.display.update()

    # Check if score is a multiple of 500 and not already spawned - KEN ANDRE
    if score % 500 == 0 and score != last_powerup_score:
        spawnPowerUp()
        last_powerup_score = score
    
    # Dash functionality
    if (keys[pygame.K_SPACE] and (left or right)) and not is_dashing:
        if pygame.time.get_ticks()-last_dash_time>=dash_cooldown:
            is_dashing = True
            dash_sound.play()  # Play dash sound
            last_dash_time = pygame.time.get_ticks()
            dash_direction = 1 if right else -1  # Set dash direction based on movement (right or left)

    if is_dashing:
        if pygame.time.get_ticks() - last_dash_time < dash_duration:
            char_x += dash_direction * dash_speed
        else: 
            is_dashing=False
        
    if char_x < 0:
        char_x = 0
    elif char_x > 1000 - char_w:
        char_x = 1000 - char_w     
    
    redrawGameWindow()  # Redraw the game window
    if gameover:
        game_over_screen()  # Show game over screen