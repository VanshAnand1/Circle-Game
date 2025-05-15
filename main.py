import pygame
import random
import math
pygame.font.init()

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800
INC = 20
STAT_FONT = pygame.font.SysFont("comicsans", 50)

class Circle:
    def __init__(self, player):
        self.radius = random.randint(max(2, player.radius - 45), player.radius + 20)
        self.color = (random.randint(30, 230), random.randint(30, 230), random.randint(30, 230))
        r = random.randint(1, 4)
        if r % 4 == 0:
            self.x = -20
            self.y = random.randint(-20, WINDOW_HEIGHT + INC)
            self.angle = random.randint(-45, 45)
        elif r % 4 == 1:
            self.x = WINDOW_WIDTH + INC
            self.y = random.randint(-20, WINDOW_HEIGHT + INC)
            self.angle = random.randint(135, 225)
        elif r % 4 == 2:
            self.x = random.randint(-20, WINDOW_WIDTH + INC)
            self.y = -20
            self.angle = random.randint(225, 315)
        else:
            self.x = random.randint(-20, WINDOW_WIDTH + INC)
            self.y = WINDOW_HEIGHT + INC
            self.angle = random.randint(45, 135)
        if self.radius < 5:
            self.velocity = 40/self.radius
        else:
            self.velocity = 140/self.radius
        self.velocity *= 1/4
    
    def move(self):
        self.x += math.sin(self.angle) * self.velocity
        self.y += math.cos(self.angle) * self.velocity

    def border(self):
        if self.x > WINDOW_WIDTH + 2.5 * INC or self.x < -50 or self.y > WINDOW_HEIGHT + 2.5 * INC or self.y < -50:
            return True
        return False
        
    def draw(self, window):
        pygame.draw.circle(window, self.color, (self.x, self.y), self.radius)

class Player:
    def __init__(self):
        self.x = 400
        self.y = 400
        self.radius = 10
        self.color = (255, 255, 255)

    def move(self):
        coordinates = pygame.mouse.get_pos()
        self.x = coordinates[0]
        self.y = coordinates[1]

    def collisions(self, circle):
        dx = self.x - circle.x
        dy = self.y - circle.y
        distance = math.hypot(dx, dy)
        if distance < self.radius + circle.radius - 2:
            if self.radius >= circle.radius:
                return 1
            return 0
        return -1

    def draw(self, window):
        pygame.draw.circle(window, self.color, (self.x, self.y), self.radius)

def draw_window(window, circles, player, score):
    window.fill((0, 0, 0))
    for circle in circles:
        circle.draw(window)
    player.draw(window)
    text = STAT_FONT.render("Score: " + str(score), 1, (255, 0, 0))
    window.blit(text, (WINDOW_WIDTH - 300, 10))
    pygame.display.update()

def main():
    clock = pygame.time.Clock()
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.mouse.set_visible(False)

    state = False
    run = True
    while run:
        if state == False:
            text = STAT_FONT.render("press any key to start the game", 1, (255, 0, 0))
            window.blit(text, (25, 400))
            pygame.display.update()
            circles = []
            remove = []
            score = 0
            player = Player()
            while len(circles) < 20:
                circles.append(Circle(player))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    state = False
                    run = False
                    break
                if event.type == pygame.KEYDOWN:
                    state = True
                    break
        if state:
            clock.tick(120)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    
            player.move()
            for circle in circles:
                if circle.border():
                    remove.append(circle)
                elif player.collisions(circle) == 1:
                    player.radius += 1
                    remove.append(circle)
                elif player.collisions(circle) == 0:
                    state = False
                circle.move()

            for circle in remove:
                circles.remove(circle)
            remove.clear()

            while len(circles) < 25:
                circles.append(Circle(player))

            if player.radius >= 410:
                player.radius = 410
        
            score = player.radius - 10
            draw_window(window, circles, player, score)

main()
pygame.quit()
quit()