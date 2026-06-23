import pygame
import random
import math

pygame.init()
W, H = 800, 500
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("L'Illusionniste : Perception vs Réalité")
font = pygame.font.SysFont("Arial", 20)
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (50, 50, 50)

def draw_tricky_background(surface, rect_area):
    for _ in range(100):
        color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
        x = random.randint(rect_area.left, rect_area.right)
        y = random.randint(rect_area.top, rect_area.bottom)
        w = random.randint(20, 80)
        h = random.randint(20, 80)
        pygame.draw.rect(surface, color, (x, y, w, h))

target_color = [random.randint(50, 200), random.randint(50, 200), random.randint(50, 200)]
player_color = [127, 127, 127]

reveal = False
score = 0

rect_left = pygame.Rect(0, 0, W//2, H)
rect_right = pygame.Rect(W//2, 0, W//2, H)

bg_surface = pygame.Surface((W//2, H))
draw_tricky_background(bg_surface, bg_surface.get_rect())

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if not reveal:
                # Gestion RGB avec min/max pour rester entre 0 et 255
                if event.key == pygame.K_r: player_color[0] = min(255, player_color[0] + 5)
                if event.key == pygame.K_t: player_color[0] = max(0, player_color[0] - 5)
                if event.key == pygame.K_g: player_color[1] = min(255, player_color[1] + 5)
                if event.key == pygame.K_h: player_color[1] = max(0, player_color[1] - 5)
                if event.key == pygame.K_b: player_color[2] = min(255, player_color[2] + 5)
                if event.key == pygame.K_n: player_color[2] = max(0, player_color[2] - 5)
                
                if event.key == pygame.K_SPACE:
                    reveal = True
                    # Utilisation de la distance Euclidienne (3D) pour calculer la précision
                    diff_r = (target_color[0] - player_color[0]) ** 2
                    diff_g = (target_color[1] - player_color[1]) ** 2
                    diff_b = (target_color[2] - player_color[2]) ** 2
                    dist = math.sqrt(diff_r + diff_g + diff_b)
                    score = max(0, 100 - int(dist))
            
            else:
                if event.key == pygame.K_SPACE:
                    reveal = False
                    target_color = [random.randint(50, 200), random.randint(50, 200), random.randint(50, 200)]
                    draw_tricky_background(bg_surface, bg_surface.get_rect())

    screen.fill(GREY)
    
    if not reveal:
        screen.blit(bg_surface, (0, 0))
    else:
        pygame.draw.rect(screen, GREY, rect_left)
    
    pygame.draw.rect(screen, target_color, (W//4 - 50, H//2 - 50, 100, 100))
    
    pygame.draw.rect(screen, GREY, rect_right)
    pygame.draw.rect(screen, player_color, (3*W//4 - 50, H//2 - 50, 100, 100))
    
    if not reveal:
        txt1 = font.render("1. Regarde la couleur à gauche", True, WHITE)
        txt2 = font.render("2. Reproduis-la à droite (Touches R/T, G/H, B/N)", True, WHITE)
        txt3 = font.render("3. ESPACE pour valider", True, WHITE)
        screen.blit(txt1, (20, 20))
        screen.blit(txt2, (20, 50))
        screen.blit(txt3, (20, 80))
        
        rgb_txt = font.render(f"R:{player_color[0]} G:{player_color[1]} B:{player_color[2]}", True, WHITE)
        screen.blit(rgb_txt, (W//2 + 20, H - 50))
    else:
        res_txt = font.render(f"SCORE : {score}/100", True, WHITE)
        real_txt = font.render(f"Réalité: {target_color} vs Toi: {player_color}", True, WHITE)
        screen.blit(res_txt, (W//2 - 50, 50))
        screen.blit(real_txt, (W//2 - 150, 100))
        screen.blit(font.render("ESPACE pour rejouer", True, WHITE), (W//2 - 80, H - 50))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()