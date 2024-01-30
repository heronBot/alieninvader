# Created by : Meyan for Sujan

import pygame,time,random,math,pygame.mixer,customtkinter,pyglet

# initializing music
pygame.init()
pygame.mixer.init()
pygame.display.init()
bg_sound = pygame.mixer.music.load("Assets\\background1.mp3")
pygame.mixer.music.play(-1)
doing = True
while doing:
    doing = False
    # high_score
    file = open("score.sc",'r')
    HIGH_SCORE = int(file.read())
    file.close()
    print(HIGH_SCORE)

    # adding fonts
    pyglet.font.add_file("Assets\\Pacifico.ttf")
    want_to_play = False

    # deltatime
    dt = 1
    # tkinter things
    customtkinter.set_default_color_theme("dark-blue")  
    customtkinter.set_appearance_mode("light")
    root = customtkinter.CTk()
    root.title("Alien Invader - Multiplayer")
    root.geometry("500x400")

    def button_event():
        global want_to_play
        want_to_play=True
        root.destroy()
    def button_event2():
        global doing
        doing=False
        root.destroy()
    label = customtkinter.CTkLabel(root, text="Alien Invader",text_color="purple",font=("Pacifico",40))
    label.pack();
    customtkinter.CTkButton(root, text="Play!!", command=button_event,font=("Times",20)).pack(pady=10)
    customtkinter.CTkButton(root, text="Play-Multiplayer", command=button_event,font=("Times",20)).pack(pady=10)
    customtkinter.CTkButton(root, text="Quit", command=button_event2,font=("Times",20)).pack(pady=10)
    label = customtkinter.CTkLabel(root, text=f"High Score:{HIGH_SCORE}",text_color="green",font=("Elephant",20))
    label.pack(side='bottom')

    root.mainloop()


    if want_to_play:
        # pygame things
        pygame.display.set_caption("Alien Killer- Multiplayer")
        screen = pygame.display.set_mode([800,710])
        running = True
        clock = pygame.time.Clock()

        # Player Stuffs, change according to your wish
        player_img = pygame.image.load("Assets\\player1.gif").convert()
        background_img = pygame.image.load("Assets\\bg.jpg").convert()
        background_img.set_alpha(128)
        enemy_img_path = "Assets\\alien1.gif"
        bullet_img_path = "Assets\\shot.gif"
        shooting_sound = pygame.mixer.Sound("Assets\\punch.wav")
        alien_dying_sound = pygame.mixer.Sound("Assets\\boom.wav")
        
        speed_player =325
        enemy_speed =225
        bullet_speed =400
        collision_distance = 40
        enemy_delay = 2 # time between two enemies spawn
        position = [400,710-player_img.get_height()]

        # some game inbuilt values [don't change]
        SCORE = 0
        enemy_img = pygame.image.load(enemy_img_path)
        pressedL = 0
        pressedR = 0
        enemies = []
        bullets = []
        explosions = []
        time_ = time.time()
        width_enemy = enemy_img.get_width()
        height_enemy = enemy_img.get_height()
        enemy_spawn_points = [i for i in range(0,800,width_enemy)]
        font = pygame.font.Font('Assets\\Pacifico.ttf', 32)

        class Enemy:
            def __init__(self,x):
                self.x = x
                self.img = pygame.image.load(enemy_img_path).convert()
                self.y =0
                
            def update(self):
                global doing
                global running
                self.y += enemy_speed*dt
                screen.blit(self.img,[self.x,self.y])

                # removing unneccasry enemies to save RAM
                if self.y >710:
                    self.remove()
                    if SCORE > HIGH_SCORE:
                        file = open("score.sc",'w')
                        file.write(str(SCORE))
                        file.close()
                    running = False
                    doing = True
            def remove(self):
                    enemies.remove(self)

        class Bullet:
            def __init__(self,x):
                self.img = pygame.image.load(bullet_img_path)
                self.x = x
                self.y = 710 - player_img.get_height()
                shooting_sound.play()
            def update(self):
                
                self.y -= bullet_speed*dt
                screen.blit(self.img,[self.x, self.y])

                # removing unneccasry bullets to save RAM
                if self.y <0:
                    self.remove()
                
            
            def remove(self):
                bullets.remove(self)

        class Explosion:
            def __init__(self,x,y):
                    self.image = pygame.image.load("Assets\\explosion1.gif").convert()
                    self.time = time.time()
                    self.position = [x,y]
            def update(self):
                    if time.time() - self.time > 0.8:
                        explosions.remove(self)
                    screen.blit(self.image,self.position)


        def check_for_collision(enemy,bullet):
            distance = math.sqrt(((enemy.x+width_enemy/2)-bullet.x)**2 + ((enemy.y+height_enemy/2)-bullet.y)**2)
            if distance<collision_distance:
                return True
        while running:
            screen.fill((0,0,0))
            screen.blit(background_img,[-800,710])
            # for controlling the player
            if position[0]>0:
                    position[0] = position[0]+pressedL*dt
            if position[0]<(800-player_img.get_width()):
                    position[0] = position[0] + pressedR*dt

            for events in pygame.event.get():
                if events.type==pygame.QUIT:
                    running = False
                if events.type == pygame.KEYDOWN:
                    if events.key == pygame.K_LEFT:
                        pressedL = -speed_player
                    if events.key == pygame.K_RIGHT:
                        pressedR = speed_player
                    if events.key == pygame.K_SPACE:
                        bullets.append(Bullet(position[0]+player_img.get_width()/2))
            
                if events.type == pygame.KEYUP:
                    if events.key == pygame.K_LEFT:
                        pressedL = 0
                    if events.key == pygame.K_RIGHT:
                        pressedR = 0

            # spanwing a new enemy after a delay
            if time.time() - time_ > enemy_delay:
                enemies.append(Enemy(random.choice(enemy_spawn_points)))
                time_ = time.time()
                
            screen.blit(player_img,position)
            for enemy in enemies:
                enemy.update()
                #  checking for collision
                for bullet in bullets:
                    if check_for_collision(enemy,bullet):
                        enemy.remove();bullet.remove()
                        alien_dying_sound.play()
                        SCORE += 1
                        explosions.append(Explosion(enemy.x,enemy.y))
                        print(SCORE)
            for bullet in bullets:
                bullet.update()
            for exps in explosions:
                exps.update()
            if SCORE>20:
                enemy_delay=1.4
            if SCORE>40:
                enemy_delay=0.8
            if SCORE > 50:
                enemy_delay = 0.55
            text = font.render(f'SCORE:{SCORE}', True,(255,145,132))
            screen.blit(text,[0,20])
            dt = clock.tick(60)/1000
            pygame.display.flip()
        pygame.display.quit()
pygame.quit()