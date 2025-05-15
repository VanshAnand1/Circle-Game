import pygame
import random
import math
pygame.font.init()

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800
STAT_FONT = pygame.font.SysFont("comicsans", 50)

class Circle:
    def __init__(self):
        self.radius = random.randint(2, 50)
        self.color = (random.randint(30, 230), random.randint(30, 230), random.randint(30, 230))
        r = random.randint(1, 4)
        if r % 4 == 0:
            self.x = -20
            self.y = random.randint(-20, 820)
            self.angle = random.randint(-45, 45)
        elif r % 4 == 1:
            self.x = 820
            self.y = random.randint(-20, 820)
            self.angle = random.randint(135, 225)
        elif r % 4 == 2:
            self.x = random.randint(-20, 820)
            self.y = -20
            self.angle = random.randint(225, 315)
        else:
            self.x = random.randint(-20, 820)
            self.y = 820
            self.angle = random.randint(45, 135)
        if self.radius < 5:
            self.velocity = 40/self.radius
        else:
            self.velocity = 110/self.radius
    
    def move(self):
        self.x += math.sin(self.angle) * self.velocity
        self.y += math.cos(self.angle) * self.velocity

    def border(self):
        if self.x > 850 or self.x < -50 or self.y > 850 or self.y < -50:
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
            while len(circles) < 20:
                circles.append(Circle())
            player = Player()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    state = False
                    run = False
                    break
                if event.type == pygame.KEYDOWN:
                    state = True
                    break
        if state:
            clock.tick(30)
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
                circles.append(Circle())

            if player.radius >= 400:
                player.radius = 400
        
            score = player.radius
            draw_window(window, circles, player, score)

main()
pygame.quit()
quit()