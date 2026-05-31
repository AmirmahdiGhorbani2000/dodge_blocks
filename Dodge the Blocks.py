import pygame
import random
import sys
import math

pygame.init()
font_large = pygame.font.Font(None, 48)
font_medium = pygame.font.Font(None, 32)
font_small = pygame.font.Font(None, 22)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PLAYER_COLOR = (240, 240, 240)
SIZE1_COLOR = (50, 200, 50)
SIZE2_COLOR = (255, 220, 50)
SIZE3_COLOR = (255, 150, 30)
SIZE4_COLOR = (255, 40, 40)
SIZE5_COLOR = (200, 150, 255)
SIZE6_COLOR = (120, 60, 180)
SIZE7_COLOR = (50, 100, 255)
SIZE8_COLOR = (20, 40, 160)
SIZE9_COLOR = (140, 100, 60)
BULLET_COLOR = (255, 150, 200)
BOSS_COLOR = (180, 20, 20)
BOSS_VEIN = (20, 0, 0)
ULTRA_BROWN = (100, 70, 40)

DAY_SKY = (135, 200, 235)
EVENING_SKY = (255, 140, 60)
NIGHT_SKY = (15, 20, 50)
SUN_COLOR = (255, 240, 100)
MOON_COLOR = (220, 220, 255)
STAR_COLOR = (255, 255, 200)
CLOUD_COLOR = (255, 255, 255)
GROUND_COLOR = (80, 140, 60)
EVENING_GROUND = (100, 80, 50)
NIGHT_GROUND = (30, 50, 30)

def get_block_color(size):
    if size <= 0:
        return ULTRA_BROWN
    colors = {1: SIZE1_COLOR, 2: SIZE2_COLOR, 3: SIZE3_COLOR, 4: SIZE4_COLOR,
              5: SIZE5_COLOR, 6: SIZE6_COLOR, 7: SIZE7_COLOR, 8: SIZE8_COLOR, 9: SIZE9_COLOR}
    return colors.get(size, SIZE1_COLOR)

def get_device_size(device):
    if device == "phone":
        return (360, 640)
    elif device == "tablet":
        return (790, 1330)
    else:
        return (480, 720)

def select_device():
    screen = pygame.display.set_mode((400, 500))
    pygame.display.set_caption("Select Device")
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                phone_btn = pygame.Rect(50, 120, 300, 80)
                tablet_btn = pygame.Rect(50, 230, 300, 80)
                desktop_btn = pygame.Rect(50, 340, 300, 80)
                if phone_btn.collidepoint(mx, my):
                    return "phone"
                if tablet_btn.collidepoint(mx, my):
                    return "tablet"
                if desktop_btn.collidepoint(mx, my):
                    return "desktop"
        screen.fill((30, 30, 60))
        title = font_medium.render("Select Your Device", True, WHITE)
        screen.blit(title, (200 - title.get_width()//2, 40))
        for i, (label, y) in enumerate([("Phone", 120), ("Tablet", 230), ("Desktop", 340)]):
            btn = pygame.Rect(50, y, 300, 80)
            pygame.draw.rect(screen, (50, 100, 200), btn, border_radius=15)
            pygame.draw.rect(screen, WHITE, btn, 2, border_radius=15)
            txt = font_medium.render(label, True, WHITE)
            screen.blit(txt, (200 - txt.get_width()//2, y + 25))
        pygame.display.flip()
        clock.tick(30)

device = select_device()
W, H = get_device_size(device)
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Dodge the Blocks")
clock = pygame.time.Clock()

player_w = W // 13
player_h = W // 13
player_x = W // 2 - player_w // 2
player_y = H - H // 6
player_speed = W // 60

blocks = []
bullets = []
base_block_size = W // 14
block_speed = W // 110
spawn_timer = 0
score = 0
best_score = 0
game_state = "menu"
difficulty = 1
stars = [(random.randint(0, W), random.randint(0, H//2)) for _ in range(60)]
boss_active = False
boss_defeated = False

try:
    with open("dodge_best.txt", "r") as f:
        best_score = int(f.read())
except:
    best_score = 0

def save_best():
    with open("dodge_best.txt", "w") as f:
        f.write(str(best_score))

def get_block_size(score):
    dodged = score
    sizes = [1]
    if dodged > 25:
        if random.random() < 0.25:
            sizes.append(2)
    if dodged > 65:
        if random.random() < 0.60:
            sizes.append(2)
        if random.random() < 0.25:
            sizes.append(3)
    if dodged > 75:
        if random.random() < 0.25:
            sizes.append(4)
    if dodged > 100:
        if random.random() < 0.20:
            sizes.append(5)
    if dodged > 125:
        if random.random() < 0.20:
            sizes.append(6)
    if dodged > 150:
        if random.random() < 0.15:
            sizes.append(7)
    if dodged > 175:
        if random.random() < 0.15:
            sizes.append(8)
    if dodged > 200:
        if random.random() < 0.10:
            sizes.append(9)
    return random.choice(sizes)

def spawn_block():
    global boss_active
    if boss_active:
        return
    size_mult = get_block_size(score)
    if score >= 250:
        size_mult = 0
        block_w = base_block_size
    else:
        block_w = base_block_size * size_mult
    x = random.randint(0, max(0, W - block_w))
    blocks.append({"x": x, "y": -block_w, "size": size_mult, "w": block_w, "shoot_timer": 0})

def spawn_boss():
    global boss_active
    boss_active = True
    blocks.clear()
    bullets.clear()
    bw = base_block_size * 8
    x = random.randint(0, max(0, W - bw))
    blocks.append({"x": x, "y": -bw, "size": 8, "w": bw, "shoot_timer": 0, "boss": True})

def reset_game():
    global player_x, blocks, bullets, score, spawn_timer, difficulty, boss_active, boss_defeated
    player_x = W // 2 - player_w // 2
    blocks.clear()
    bullets.clear()
    score = 0
    spawn_timer = 0
    difficulty = 1
    boss_active = False
    boss_defeated = False

def draw_background(dodged):
    if dodged > 65:
        sky = NIGHT_SKY
        ground = NIGHT_GROUND
        for sx, sy in stars:
            twinkle = random.random() < 0.3
            if twinkle:
                pygame.draw.circle(screen, STAR_COLOR, (sx, sy), random.randint(1, 2))
        moon_x = W - W//6
        moon_y = H//8
        pygame.draw.circle(screen, MOON_COLOR, (moon_x, moon_y), W//18)
        pygame.draw.circle(screen, sky, (moon_x + W//40, moon_y - W//40), W//18)
        for _ in range(6):
            bx = random.randint(0, W)
            by = random.randint(H//2, H)
            pygame.draw.rect(screen, (25, 45, 25), (bx, by, 3, H//20))
    elif dodged > 25:
        sky = EVENING_SKY
        ground = EVENING_GROUND
        sun_x = W - W//5
        sun_y = H//5
        pygame.draw.circle(screen, SUN_COLOR, (sun_x, sun_y), W//14)
        for i in range(3):
            cx = random.randint(50, W-50)
            cy = random.randint(30, H//3)
            pygame.draw.ellipse(screen, (255, 180, 100), (cx, cy, W//6, H//20))
    else:
        sky = DAY_SKY
        ground = GROUND_COLOR
        for i in range(4):
            cx = (pygame.time.get_ticks() * 0.05 + i * W//4) % (W + W//3) - W//6
            cy = random.randint(20, H//4)
            pygame.draw.ellipse(screen, CLOUD_COLOR, (cx, cy, W//5, H//12))
            pygame.draw.ellipse(screen, (240, 240, 250), (cx + W//20, cy + H//40, W//7, H//15))
    screen.fill(sky)
    ground_y = H - H//7
    pygame.draw.rect(screen, ground, (0, ground_y, W, H//7))
    pygame.draw.line(screen, (min(255, ground[0]+30), min(255, ground[1]+30), min(255, ground[2]+30)), (0, ground_y), (W, ground_y), 3)
    for _ in range(10):
        gx = random.randint(0, W)
        gy = random.randint(ground_y, H)
        pygame.draw.rect(screen, (ground[0]-20, ground[1]-20, ground[2]-20), (gx, gy, 2, H//30))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save_best()
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if game_state == "menu":
                game_state = "playing"
                reset_game()
            elif game_state == "dead":
                game_state = "menu"
            elif game_state == "win":
                game_state = "menu"
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if game_state == "menu":
                    game_state = "playing"
                    reset_game()
                elif game_state == "dead":
                    game_state = "menu"
                elif game_state == "win":
                    game_state = "menu"
    if game_state == "playing":
        mouse_x, _ = pygame.mouse.get_pos()
        target_x = mouse_x - player_w // 2
        if abs(target_x - player_x) > 1:
            player_x += (target_x - player_x) * 0.3
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player_x += player_speed
        player_x = max(0, min(W - player_w, player_x))
        if score >= 500 and not boss_active and not boss_defeated:
            spawn_boss()
        if not boss_active:
            spawn_timer += 1
            spawn_rate = max(20, 45 - difficulty * 2)
            if spawn_timer >= spawn_rate:
                spawn_block()
                spawn_timer = 0
        for block in blocks[:]:
            speed_mult = 0.25 if score >= 250 else 1
            block_speed_current = (block_speed + difficulty * 0.2) * speed_mult
            if block.get("boss"):
                block_speed_current = block_speed + difficulty * 0.15
            block["y"] += block_speed_current
            if block["y"] > H:
                blocks.remove(block)
                if block.get("boss"):
                    boss_defeated = True
                    boss_active = False
                    game_state = "win"
                    if score > best_score:
                        best_score = score
                        save_best()
                else:
                    if score < 225:
                        size_val = block["size"] if block["size"] > 0 else 1
                        score += size_val
                    else:
                        score += 1
                continue
            if score >= 250 or block.get("boss"):
                block["shoot_timer"] += 1
                shoot_rate = 60 if block.get("boss") else 75
                if block["shoot_timer"] >= shoot_rate:
                    block["shoot_timer"] = 0
                    bullet_size = max(2, (score - 250) // 50 + 3)
                    bullets.append({
                        "x": block["x"] + block["w"] // 2,
                        "y": block["y"] + block["w"] // 2,
                        "vx": random.choice([-3, -2, -1, 0, 1, 2, 3]),
                        "vy": 3 if not block.get("boss") else 0,
                        "size": bullet_size,
                        "target_player": block.get("boss", False)
                    })
                    if block.get("boss"):
                        for _ in range(3):
                            bullets.append({
                                "x": block["x"] + block["w"] // 2,
                                "y": block["y"] + block["w"] // 2,
                                "vx": random.uniform(-5, 5),
                                "vy": random.uniform(-5, 5),
                                "size": bullet_size + 2,
                                "target_player": True
                            })
            bw = block["w"]
            by = block["y"]
            bx = block["x"]
            if (by + bw > player_y and
                by < player_y + player_h and
                bx + bw > player_x and
                bx < player_x + player_w):
                game_state = "dead"
                if score > best_score:
                    best_score = score
                    save_best()
        for bullet in bullets[:]:
            if bullet.get("target_player"):
                dx = player_x + player_w//2 - bullet["x"]
                dy = player_y + player_h//2 - bullet["y"]
                dist = math.sqrt(dx*dx + dy*dy)
                if dist > 0:
                    bullet["vx"] = dx / dist * 4
                    bullet["vy"] = dy / dist * 4
            bullet["x"] += bullet.get("vx", 0)
            bullet["y"] += bullet.get("vy", 3)
            if bullet["y"] > H or bullet["y"] < 0 or bullet["x"] > W or bullet["x"] < 0:
                bullets.remove(bullet)
                continue
            br = pygame.Rect(bullet["x"] - bullet["size"], bullet["y"] - bullet["size"], bullet["size"]*2, bullet["size"]*2)
            pr = pygame.Rect(player_x, player_y, player_w, player_h)
            if br.colliderect(pr):
                game_state = "dead"
                if score > best_score:
                    best_score = score
                    save_best()
        if score < 250:
            difficulty = 1 + score // 25
    draw_background(score if game_state == "playing" else 0)
    if game_state == "menu":
        title = font_large.render("Dodge the Blocks", True, WHITE)
        sub = font_medium.render("Tap or SPACE to Start", True, WHITE)
        best = font_small.render(f"Best: {best_score}", True, (255, 255, 100))
        screen.blit(title, (W//2 - title.get_width()//2, H//2 - 80))
        screen.blit(sub, (W//2 - sub.get_width()//2, H//2))
        screen.blit(best, (W//2 - best.get_width()//2, H//2 + 60))
        info = font_small.render("Mouse or Arrow Keys to Move", True, (180, 180, 180))
        screen.blit(info, (W//2 - info.get_width()//2, H - 100))
    elif game_state == "playing":
        shadow = pygame.Rect(player_x + 3, player_y + 3, player_w, player_h)
        pygame.draw.rect(screen, (30, 30, 30, 100), shadow, border_radius=10)
        pygame.draw.rect(screen, PLAYER_COLOR, (player_x, player_y, player_w, player_h), border_radius=10)
        pygame.draw.rect(screen, WHITE, (player_x, player_y, player_w, player_h), 2, border_radius=10)
        inner = pygame.Rect(player_x + player_w//4, player_y + player_h//4, player_w//2, player_h//2)
        pygame.draw.rect(screen, (220, 220, 230), inner, border_radius=5)
        for block in blocks:
            bw = block["w"]
            if block.get("boss"):
                bc = BOSS_COLOR
                pygame.draw.rect(screen, bc, (block["x"], block["y"], bw, bw), border_radius=6)
                for i in range(4):
                    vx = random.randint(block["x"], block["x"] + bw)
                    vy = random.randint(block["y"], block["y"] + bw)
                    vx2 = random.randint(block["x"], block["x"] + bw)
                    vy2 = random.randint(block["y"], block["y"] + bw)
                    pygame.draw.line(screen, BOSS_VEIN, (vx, vy), (vx2, vy2), 2)
                pygame.draw.rect(screen, WHITE, (block["x"], block["y"], bw, bw), 3, border_radius=6)
            else:
                bc = get_block_color(block["size"]) if block["size"] > 0 else ULTRA_BROWN
                shadow_r = pygame.Rect(block["x"] + 2, block["y"] + 2, bw, bw)
                pygame.draw.rect(screen, (20, 20, 20, 100), shadow_r, border_radius=6)
                pygame.draw.rect(screen, bc, (block["x"], block["y"], bw, bw), border_radius=6)
                pygame.draw.rect(screen, WHITE, (block["x"], block["y"], bw, bw), 1, border_radius=6)
        for bullet in bullets:
            pygame.draw.circle(screen, BULLET_COLOR, (int(bullet["x"]), int(bullet["y"])), bullet["size"])
        score_text = font_large.render(str(score), True, WHITE)
        screen.blit(score_text, (W//2 - score_text.get_width()//2, 15))
        diff_text = font_small.render(f"Level {difficulty}", True, (200, 200, 200))
        screen.blit(diff_text, (10, 10))
        if boss_active:
            boss_text = font_medium.render("BOSS FIGHT!", True, (255, 50, 50))
            screen.blit(boss_text, (W//2 - boss_text.get_width()//2, 55))
    elif game_state == "dead":
        over = font_large.render("Game Over", True, (255, 60, 60))
        final_score = font_medium.render(f"Score: {score}", True, WHITE)
        best_text = font_small.render(f"Best: {best_score}", True, (255, 255, 100))
        restart = font_small.render("Tap or SPACE to Menu", True, WHITE)
        screen.blit(over, (W//2 - over.get_width()//2, H//2 - 80))
        screen.blit(final_score, (W//2 - final_score.get_width()//2, H//2 - 10))
        screen.blit(best_text, (W//2 - best_text.get_width()//2, H//2 + 40))
        screen.blit(restart, (W//2 - restart.get_width()//2, H//2 + 90))
        if score == best_score and score > 0:
            new_best = font_small.render("NEW BEST!", True, (50, 255, 100))
            screen.blit(new_best, (W//2 - new_best.get_width()//2, H//2 - 45))
    elif game_state == "win":
        screen.fill((20, 10, 40))
        win_title = font_large.render("YOU WIN!", True, (255, 215, 0))
        congrats = font_medium.render("Congratulations!", True, WHITE)
        final_score_text = font_medium.render(f"Final Score: {score}", True, WHITE)
        thanks = font_small.render("You have completed Dodge the Blocks!", True, (200, 200, 200))
        credit = font_small.render("Created by: Amirmahdi Ghorbani", True, (150, 150, 255))
        restart_text = font_small.render("Tap or SPACE to Menu", True, WHITE)
        screen.blit(win_title, (W//2 - win_title.get_width()//2, H//2 - 120))
        screen.blit(congrats, (W//2 - congrats.get_width()//2, H//2 - 60))
        screen.blit(final_score_text, (W//2 - final_score_text.get_width()//2, H//2 - 10))
        screen.blit(thanks, (W//2 - thanks.get_width()//2, H//2 + 40))
        screen.blit(credit, (W//2 - credit.get_width()//2, H//2 + 80))
        screen.blit(restart_text, (W//2 - restart_text.get_width()//2, H//2 + 140))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()