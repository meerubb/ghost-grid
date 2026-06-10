import pygame
import random
import sys

pygame.init()

WIDTH, HEIGHT = 960, 640
CELL = 40
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()


BG_COLOR = (28, 33, 22)         
WALL_COLOR = (230, 164, 168)    
PLAYER_COLOR = (255, 245, 238)  
SUIT_COLOR = (242, 137, 102)     
GHOST_A_COLOR = (143, 151, 121) 
GHOST_B_COLOR = (244, 204, 204) 
EXIT_COLOR = (229, 184, 135)    

state = "play"
current_level = 0  


MAZES = [
    
    [
        "########################",
        "#P         #           #",
        "# #### ### # ####### # #",
        "# #    #   # #     # # #",
        "# # #### ### # ### # # #",
        "# # #        # #   # # #",
        "# # # ######## # ### # #",
        "#   #          #     # #",
        "##### ########## ##### #",
        "#     #          #     #",
        "# ##### ######## # #####",
        "# #     #      # # #   #",
        "# # ##### #### # # #   #",
        "# #            #      E#",
        "########################"
    ],
    
    [
        "########################",
        "#P     #               #",
        "###### # ############# #",
        "#      # #           # #",
        "# ###### # ######### # #",
        "# #      # #       # # #",
        "# # ###### ####### # # #",
        "# # #            # # # #",
        "# # # ########## # # # #",
        "# # # #        # # # # #",
        "# # # # ###### # # # # #",
        "#   # # #    # #   # # #",
        "##### # # ## # ##### # #",
        "#     #   #  #       #E#",
        "text************************" 
    ],
   
    [
        "########################",
        "#P   #        #       E#",
        "# ## # ###### # ###### #",
        "# #  # #    # # #    # #",
        "# #  # # ## # # # ## # #",
        "#    #   #    #   #    #",
        "#### # ### ###### ### ##", 
        "#    #   #    #   #    #",
        "# ## # # ## # # # ## # #", 
        "# #  # #    # # #    # #",
        "# ## # ###### # ###### #",
        "#    #                 #", 
        "#### ######## ######## #",
        "#                      #",
        "########################"
    ],
   
    [
        "########################",
        "#P         ##          #",
        "# ######## ## ######## #",
        "# #      # ## #      # #",
        "# # #### # ## # #### # #",
        "#   #    #    #    #   #",
        "###   ####    ####   ###", 
        "###   ####    ####   ###", 
        "#   #    #    #    #   #",
        "# # #### # ## # #### # #",
        "# #      # ## #      # #",
        "# ######## ## ######## #",
        "#          ##          #",
        "#############         E#",
        "grid########################"
    ],
   
    [
        "########################",
        "#P                     #",
        "# #################### #",
        "# #   #              # #",
        "# # # # ############ # #",
        "# # # # #          # # #",
        "# # # # #   ###### # # #", 
        "# # # #     # E  # # # #", 
        "# # # #     #### # # # #", 
        "# # # # # #      # # # #",
        "# # # # # ######## # # #",
        "# # # # #            # #",  
        "# # # # ############ # #",
        "#   #                # #",  
        "########################"
    ]
]


for m in range(len(MAZES)):
    for r in range(len(MAZES[m])):
        MAZES[m][r] = MAZES[m][r].replace("text", "").replace("grid", "")

walls = []
player_pos = [0, 0]
exit_pos = [0, 0]
ghosts = []


def build_maze():
    global player_pos, exit_pos, ghosts
    walls.clear()
    ghosts.clear()
    
    pygame.display.set_caption(f"Ghost Grid- Level {current_level + 1}/5")
    
    current_maze_layout = MAZES[current_level]
    ghost_spawn_slots = []

    for r, row in enumerate(current_maze_layout):
        for c, cell in enumerate(row):
            x, y = c * CELL, r * CELL
            if cell == "#":
                walls.append(pygame.Rect(x, y, CELL, CELL))
            elif cell == "P":
                player_pos = [x + 5, y + 5]
            elif cell == "E":
                exit_pos = [x, y]
            elif cell == " ":
                if c > 6 or r > 6:
                    ghost_spawn_slots.append([x + 5, y + 5])

    if len(ghost_spawn_slots) < 2:
        ghost_spawn_slots = [[400, 200], [500, 400]]

    spawns = random.sample(ghost_spawn_slots, 2)
    ghosts = [
        {"pos": spawns[0], "type": "chaser", "color": GHOST_A_COLOR},
        {"pos": spawns[1], "type": "patrol", "color": GHOST_B_COLOR, "dir": [1, 0]}
    ]


def check_collision(rect):
    for w in walls:
        if rect.colliderect(w):
            return True
    return False

def move_player(dx, dy):
    speed = 4
    player_pos[0] += dx * speed
    player_rect = pygame.Rect(player_pos[0], player_pos[1], 30, 30)
    if check_collision(player_rect):
        if dx > 0:
            player_pos[0] = (player_pos[0] // CELL) * CELL + (CELL - 30) - 1
        elif dx < 0:
            player_pos[0] = (player_pos[0] // CELL + 1) * CELL + 1

    player_pos[1] += dy * speed
    player_rect = pygame.Rect(player_pos[0], player_pos[1], 30, 30)
    if check_collision(player_rect):
        if dy > 0:
            player_pos[1] = (player_pos[1] // CELL) * CELL + (CELL - 30) - 1
        elif dy < 0:
            player_pos[1] = (player_pos[1] // CELL + 1) * CELL + 1


def move_ghosts():
    speed = 2
    for g in ghosts:
        gx, gy = g["pos"]

        if g["type"] == "chaser":
            dx = 1 if player_pos[0] > gx else -1 if player_pos[0] < gx else 0
            dy = 1 if player_pos[1] > gy else -1 if player_pos[1] < gy else 0
            
            if dx != 0:
                test_rect = pygame.Rect(gx + dx * speed, gy, 30, 30)
                if not check_collision(test_rect):
                    g["pos"][0] += dx * speed
                    continue
            if dy != 0:
                test_rect = pygame.Rect(gx, gy + dy * speed, 30, 30)
                if not check_collision(test_rect):
                    g["pos"][1] += dy * speed

        elif g["type"] == "patrol":
            nx = gx + g["dir"][0] * speed
            ny = gy + g["dir"][1] * speed
            test_rect = pygame.Rect(nx, ny, 30, 30)

            if not check_collision(test_rect):
                g["pos"] = [nx, ny]
            else:
                directions = [[1, 0], [-1, 0], [0, 1], [0, -1]]
                random.shuffle(directions)
                for d in directions:
                    test_turn = pygame.Rect(gx + d[0]*speed, gy + d[1]*speed, 30, 30)
                    if not check_collision(test_turn):
                        g["dir"] = d
                        break


def draw_player(surface, pos):
    x, y = int(pos[0]), int(pos[1])
    
    
    pygame.draw.ellipse(surface, SUIT_COLOR, (x + 2, y + 4, 26, 24))
    pygame.draw.rect(surface, SUIT_COLOR, (x + 4, y + 16, 22, 11), border_radius=4)
    
    
    pygame.draw.circle(surface, (15, 15, 20), (x + 9, y + 12), 4)        
    pygame.draw.circle(surface, (255, 255, 255), (x + 8, y + 11), 1.5)   
    
    pygame.draw.circle(surface, (15, 15, 20), (x + 21, y + 12), 4)       
    pygame.draw.circle(surface, (255, 255, 255), (x + 20, y + 11), 1.5)  
    
    
    pygame.draw.arc(surface, (15, 15, 20), (x + 12, y + 13, 6, 5), 3.14, 0, 2)
    
    
    pygame.draw.circle(surface, (240, 145, 145), (x + 5, y + 16), 2)
    pygame.draw.circle(surface, (240, 145, 145), (x + 25, y + 16), 2)
    
    pygame.draw.circle(surface, SUIT_COLOR, (x + 15, y + 3), 4)

def draw_ghost(surface, g):
    x, y = int(g["pos"][0]), int(g["pos"][1])
    pygame.draw.circle(surface, g["color"], (x + 15, y + 14), 14)
    pygame.draw.rect(surface, g["color"], (x + 1, y + 14, 28, 12))
    pygame.draw.circle(surface, BG_COLOR, (x + 5, y + 26), 4)
    pygame.draw.circle(surface, BG_COLOR, (x + 15, y + 26), 4)
    pygame.draw.circle(surface, BG_COLOR, (x + 25, y + 26), 4)
    pygame.draw.circle(surface, (255, 255, 255), (x + 9, y + 10), 4)
    pygame.draw.circle(surface, (255, 255, 255), (x + 21, y + 10), 4)
    pygame.draw.circle(surface, (40, 50, 90), (x + 10, y + 10), 2)
    pygame.draw.circle(surface, (40, 50, 90), (x + 22, y + 10), 2)

def draw_game_screens(text, subtext):
    screen.fill(BG_COLOR)
    font = pygame.font.SysFont("Arial", 50, bold=True)
    sub_font = pygame.font.SysFont("Arial", 22)
    
    render_text = font.render(text, True, WALL_COLOR)
    render_sub = sub_font.render(subtext, True, (200, 200, 190))
    
    screen.blit(render_text, (WIDTH//2 - render_text.get_width()//2, HEIGHT//2 - 50))
    screen.blit(render_sub, (WIDTH//2 - render_sub.get_width()//2, HEIGHT//2 + 20))
    pygame.display.update()

def draw():
    screen.fill(BG_COLOR)

    for w in walls:
        pygame.draw.rect(screen, (40, 48, 32), w) 
        pygame.draw.rect(screen, WALL_COLOR, w, 2, border_radius=3)

    pygame.draw.rect(screen, EXIT_COLOR, (exit_pos[0]+2, exit_pos[1]+2, CELL-4, CELL-4), border_radius=5)
    
    draw_player(screen, player_pos)
    for g in ghosts:
        draw_ghost(screen, g)

    pygame.display.update()


def main():
    global state, current_level
    build_maze()

    while True:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN and state != "play":
                if event.key == pygame.K_r:
                    if state == "campaign_win":
                        current_level = 0  
                    build_maze()
                    state = "play"

        if state == "play":
            keys = pygame.key.get_pressed()
            dx, dy = 0, 0
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:  dx = -1
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]: dx = 1
            if keys[pygame.K_UP] or keys[pygame.K_w]:    dy = -1
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:  dy = 1

            if dx != 0 or dy != 0:
                move_player(dx, dy)

            move_ghosts()

            p_rect = pygame.Rect(player_pos[0], player_pos[1], 30, 30)
            e_rect = pygame.Rect(exit_pos[0], exit_pos[1], CELL, CELL)
            
            if p_rect.colliderect(e_rect):
                if current_level < len(MAZES) - 1:
                    current_level += 1
                    state = "next_level"
                else:
                    state = "campaign_win"

            for g in ghosts:
                g_rect = pygame.Rect(g["pos"][0], g["pos"][1], 30, 30)
                if p_rect.colliderect(g_rect):
                    state = "lose"

            draw()

        elif state == "next_level":
            draw_game_screens(f"LEVEL {current_level} CLEAR!", "Press 'R' to Start Next Level")
        elif state == "campaign_win":
            draw_game_screens(" GRAND CAMPAIGN VICTORY!", "You Beat All 5 Mazes! Press 'R' to Restart")
        elif state == "lose":
            draw_game_screens(f" CAUGHT ON LEVEL {current_level + 1}", "Press 'R' to Retry This Level")

if __name__ == "__main__":
    main()
