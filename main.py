import pygame
import time

# Initialize Pygame
pygame.init()

Black = (0, 0, 0)
P1Color = (0, 0, 255)  # player 1 trail colour
P2Color = (255, 0, 0)  # player 2 trail colour

class Player:
    def __init__(self, x, y, d, c):
        "init method for class"
        #player x coord
        self.x = x
        #player y coord
        self.y = y
        #player speed
        self.speed = 4
        #player direction
        self.direction = d
        self.color = c
        self.rect = pygame.Rect(self.x - 1, self.y - 1, 2, 2)

    def draw(self, screen):
        "method to draw player"
        self.rect = pygame.Rect(self.x - 1, self.y - 1, 2, 2) #redefines rectangle
        pygame.draw.rect(screen, self.color, self.rect, 0) # draws player on the screen

    def move(self):
        "method for moving the players"
        self.x += self.direction[0]
        self.y += self.direction[1]

def new_game():
    TempP1 = Player(50, height//2, (-2, 0), P1Color)
    TempP2 = Player(width-50, height//2, (-2, 0), P2Color)
    return TempP1, TempP2


# Set up the game window
height = 400
width = 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("2D Tron")
factor = 40
font = pygame.font.Font(None, 72)

clock = pygame.time.Clock()
checkTime = time.time()

p1 = Player(50, (height - factor) / 2, (-2, 0), P1Color)
p2 = Player(width - 50, (height - factor) / 2, (-2, 0), P2Color)
objects = [p1, p2] # list of all players objects
path = [(p1.rect.copy(), '1'), (p2.rect.copy(), '2')]

Score = [0, 0]
walls = [pygame.Rect([0, factor, 15, height]), pygame.Rect([0, factor, width, 15]),\
         pygame.Rect([width - 15, factor, 15, height]),\
         pygame.Rect([0, height - 15, width, 15])] # all four walls of screen

new = False
running = True

# Game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            #Player 1
            if event.key == pygame.K_w:
                objects[0].direction = (0, -2)
            elif event.key == pygame.K_s:
                objects[0].direction = (0, 2)
            elif event.key == pygame.K_a:
                objects[0].direction = (-2, 0)
            elif event.key == pygame.K_d:
                objects[0].direction = (2, 0)
            #Player 2
            if event.key == pygame.K_UP:
                objects[1].direction = (0, -2)
            elif event.key == pygame.K_DOWN:
                objects[1].direction = (0, 2)
            elif event.key == pygame.K_LEFT:
                objects[1].direction = (-2, 0)
            elif event.key == pygame.K_RIGHT:
                objects[1].direction = (2, 0)

        screen.fill(Black)

        for wall in walls:
            pygame.draw.rect(screen, (42, 42, 42), wall, 0) # draw the walls

        for player in objects:
            player_rect = pygame.Rect(player.x - 1, player.y - 1, 2, 2)
            collision = (
            any(player_rect.colliderect(p[0]) for p in path) or
            player_rect.collidelist(walls) > -1
            )

            if collision and (time.time() - checkTime) >= 0.1:
                checkTime = time.time()
                if player.color == P1Color:
                    Score[1] += 1
                else:
                    Score[0] += 1
                new = True
                p1, p2 = new_game()
                objects = [p1, p2]
                path = [(p1.rect.copy(), '1'), (p2.rect.copy(), '2')]
                break
            else:
                tag = '1' if player.color == P1Color else '2'
                path.append((player.rect.copy(), tag))
                player.draw(screen)
                player.move()

    if new:
        path = []
        new = False
    else:
        for segment in path:
            color = P1Color if segment[1] == '1' else P2Color
            pygame.draw.rect(screen, color, segment[0], 0)

    score_text = font.render(f'{Score[0]} : {Score[1]}', True, (255, 153, 51))
    score_text_pos = score_text.get_rect(center=(width // 2, factor // 2))
    screen.blit(score_text, score_text_pos)

    pygame.display.flip()
    clock.tick(7)

pygame.quit()
pygame.quit()