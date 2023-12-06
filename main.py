import pygame
import spritesheet

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('New Platformer')

# Game Function
def draw_text(text, font, text_col, x, y, bg_col=None, get=False):
    img = font.render(text, True, text_col, bg_col)
    screen.blit(img, (x, y))

    if get:
        return img

def draw_btn(text, font, text_col, x, y, scale, bg_col=None, get=False):
    img = draw_text(text, font, text_col, x, y, bg_col, True)
    if get:
        return (x-(scale[0]//2)+5, y-(scale[1]//2)+5, x+img.get_width()+(scale[0]//2)-5, y+img.get_height()+(scale[1]//2)-5)
    else:
        pygame.draw.rect(screen, text_col, pygame.Rect(x-(scale[0]//2), y-(scale[1]//2), img.get_width()+scale[0], img.get_height()+scale[1]), 3)


def check_btn(text, font, text_col, x, y, scale, bg_col=None):
    btn_pos = draw_btn(text, font, text_col, x, y, scale, bg_col, True)
    mouse = pygame.mouse.get_pos()
    if mouse[0] > btn_pos[0] and mouse[0] < btn_pos[2] and mouse[1] > btn_pos[1] and mouse[1] < btn_pos[3]:
        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(btn_pos[0]-5, btn_pos[1]-5, btn_pos[2]-x+(scale[0]//2)+5, btn_pos[3]-y+(scale[1]//2)+5))
        draw_btn(text, font, bg_col, x, y, scale, text_col)
        if pygame.mouse.get_pressed()[0]:
            task_btn(text)
    else:
        draw_btn(text, font, text_col, x, y, scale, bg_col)

def task_btn(text):
    global run, state
    if text == 'QUIT':
        run = False
    elif text == 'PLAY':
        state = 'PLAY'
    elif text == 'SETTINGS':
        print('Updating')

def gamedisplay(cstate, x, y):
    sprite_sheet_image = pygame.image.load('doux.png').convert_alpha()
    sprite_sheet = spritesheet.SpriteSheet(sprite_sheet_image)

    BLACK = (0, 0, 0)

    frame = [sprite_sheet.get_image(i, 24, 24, 3, BLACK) for i in range(24)]

    screen.blit(frame[animations(cstate)], (x, y))


def animations(cstate):
    global animationcount
    
    if cstate == 'stand':
        if int(animationcount) == 0:
            animationcount = 4
        animationcount -= 0.1
        return int(animationcount)
    
    elif cstate == 'move':
        if int(animationcount) == 0:
            animationcount = 6
        animationcount -= 0.1
        return 6-int(animationcount)+3

def move_character():
    key = pygame.key.get_pressed()
    global character_pos

    if key[pygame.K_a] and key[pygame.K_d]:
        return 'stand'

    if key[pygame.K_a] or key[pygame.K_d]:
        if key[pygame.K_a]:
            character_pos[0] -= 2
        if key[pygame.K_d]:
            character_pos[0] += 2
        return 'move'
    
    return 'stand'
    


# Game Variable
font = pygame.font.SysFont('arial', 40)
state = 'MENU'
animationcount = 0
character_pos = [0, 528]



# Game Loop
run = True
clock = pygame.time.Clock()
while run:

    # Check game state
    if state == 'MENU':
        screen.fill((52, 78, 91))
        check_btn('PLAY', font, (255, 255, 255), 100, 200, (100, 20), (52, 78, 91))
        check_btn('SETTINGS', font, (255, 255, 255), 100, 300, (100, 20), (52, 78, 91))
        check_btn('QUIT', font, (255, 255, 255), 100, 400, (100, 20), (52, 78, 91))
    elif state == 'PLAY':
        screen.fill((255, 255, 255))
        
        gamedisplay(move_character(), character_pos[0], character_pos[1])
        

    # Events Handle
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()
    clock.tick(60)

pygame.quit()