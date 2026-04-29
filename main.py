import pygame, random

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 200)
font1 = pygame.font.SysFont(None, 100)

white = (255,255,255)
black = (0,0,0)
red = (255,0,0)

scrw, scrh = screen.get_size()

cat_sleep = pygame.image.load('image/cat_sleep.png')
cat_stare = pygame.image.load('image/cat_stare.png')
cat_head_orig = pygame.image.load('image/cat_head.png')
cat_head = pygame.transform.scale(cat_head_orig, (600,600))

cat_sz = min(scrw, scrh)
cat_w = cat_sz/10*7
cat_h = cat_sz
cat_bottom_pos = screen.get_rect().centery + cat_h//2

hands = [pygame.transform.scale(pygame.image.load(f'image/hand{i}.png'), (400,400)) for i in range(5)]
pat_sounds = [pygame.mixer.Sound(f'sound/pat{i}.ogg') for i in range(3)]
bruh_sound = pygame.mixer.Sound("sound/bruh.ogg")
crazy_sound = pygame.mixer.Sound("sound/crazy.ogg")

hand_frame = 0
frame_delay = 2
frame_counter = 0
hand_loop_counter = 0
pat_play = False
touch_pos = (0,0)

stare_random = 0
stare_counter = 0
cat_is_staring = False
display_head = False
head_tick_counter = 0

head_scale = 1.0
head_grow_speed = 0.08
head_rect = None
head_center = None

game_over = False
can_pat = True
score = 0

stare_tick_counter = 0
stare_duration_in_ticks = 90

def play_patpat():
    random.choice(pat_sounds).play()

def reset_game():
    global hand_frame, frame_counter, hand_loop_counter, pat_play, touch_pos
    global stare_random, stare_counter, cat_is_staring
    global display_head, head_tick_counter, head_scale, head_rect, head_center
    global game_over, can_pat, score, stare_tick_counter
    hand_frame = 0
    frame_counter = 0
    hand_loop_counter = 0
    pat_play = False
    touch_pos = (0,0)
    stare_random = 0
    stare_counter = 0
    cat_is_staring = False
    display_head = False
    head_tick_counter = 0
    head_scale = 1.0
    head_rect = None
    head_center = None
    game_over = False
    can_pat = True
    score = 0
    stare_tick_counter = 0

def render_hand(frame, pos):
    hand_surf = hands[frame]
    hand_rect = hand_surf.get_rect(center=pos)
    screen.blit(hand_surf, hand_rect)
    return hand_rect

def render_cat(frame_index, is_staring=False):
    if is_staring:
        cat_scaled = pygame.transform.scale(cat_stare, (int(cat_w), int(cat_h)))
    else:
        scale_factor = 1.0 if frame_index == 0 else 1.0 - 0.03*frame_index
        new_height = int(cat_h * scale_factor)
        cat_scaled = pygame.transform.scale(cat_sleep, (int(cat_w), new_height))
    cat_rect = cat_scaled.get_rect()
    cat_rect.midbottom = (screen.get_rect().centerx, cat_bottom_pos)
    screen.blit(cat_scaled, cat_rect)
    return cat_rect

running = True
while running:
    clock.tick(60)
    screen.fill(white)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEMOTION):
            touch_pos = event.pos
        if event.type == pygame.MOUSEBUTTONDOWN:
            if game_over:
                reset_game()
            elif can_pat:
                pat_play = True
                if not cat_is_staring:
                    stare_random = random.randint(0,150)
                    stare_counter = 0
        elif event.type == pygame.MOUSEBUTTONUP:
            pat_play = False

    if not game_over:
        cat_rect = render_cat(hand_frame if pat_play else 0, is_staring=cat_is_staring)

        if not cat_is_staring and not display_head:
            z_text = font1.render("z..Z..z", True, black)
            z_rect = z_text.get_rect()
            z_rect.midleft = (cat_rect.right-80, cat_rect.top  + cat_rect.height //16)
            screen.blit(z_text, z_rect)

        if pat_play and can_pat:
            hand_rect = render_hand(hand_frame, touch_pos)
            if hand_rect.colliderect(cat_rect):
                stare_counter += 1
                if stare_counter >= stare_random and not cat_is_staring:
                    bruh_sound.play()
                    cat_is_staring = True
                    display_head = False
                    head_tick_counter = 0
                    head_scale = 1.0
                    head_rect = cat_head.get_rect()
                    head_rect.topright = (cat_rect.right, cat_rect.top - 75)
                    head_center = head_rect.center
                    stare_tick_counter = 0

                frame_counter += 1
                if frame_counter >= frame_delay:
                    hand_frame += 1
                    frame_counter = 0
                    if hand_frame >= len(hands):
                        hand_frame = 0
                        hand_loop_counter += 1
                        play_patpat()
                        if hand_loop_counter >= 3:
                            score += 1
                            hand_loop_counter = 0

                if cat_is_staring and not display_head:
                    head_tick_counter += 1
                    if head_tick_counter >= 15:
                        display_head = True
                        head_scale = 1.0
                        head_rect = cat_head.get_rect()
                        head_rect.topright = (cat_rect.right, cat_rect.top - 75)
                        head_center = head_rect.center
                        crazy_sound.play()
        else:
            hand_frame = 0
            frame_counter = 0
            if cat_is_staring and not display_head:
                stare_tick_counter += 1
                if stare_tick_counter >= stare_duration_in_ticks:
                    cat_is_staring = False
                    stare_tick_counter = 0

        if cat_is_staring and display_head:
            can_pat = False
            head_scale += head_grow_speed
            max_scale = max(scrh, scrw) / cat_head.get_height()
            if head_scale > max_scale:
                head_scale = max_scale
                game_over = True

            new_width = int(cat_head.get_width() * head_scale)
            new_height = int(cat_head.get_height() * head_scale)
            scaled_head = pygame.transform.scale(cat_head, (new_width, new_height))
            rect_head_scaled = scaled_head.get_rect()
            rect_head_scaled.center = head_center
            screen.blit(scaled_head, rect_head_scaled)

        score_text = font.render(str(score), True, black)
        screen.blit(score_text, (30, 30))

    else:
        screen.fill(black)
        you_die_text = font.render("YOU DIE", True, red)
        you_die_rect = you_die_text.get_rect(center=(scrw//2, scrh//2))
        score_text = font1.render(f"score {score}", True, white)
        score_rect = score_text.get_rect(center=(scrw//2, scrh//2 + 250))
        screen.blit(you_die_text, you_die_rect)
        screen.blit(score_text, score_rect)

    pygame.display.flip()

pygame.quit()