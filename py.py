#August 2020
#Make the classic game snake, but preferably with some kind of twist

import pygame , random , sys
from pathlib import Path

class Snake(pygame.sprite.Sprite):
    def __init__(self):
        self.length = 0
        super().__init__()
        self.image = pygame.Surface((20,20))
        self.image.fill((0 , 255 , 0))
        self.rect = self.image.get_rect()
    def grow(self):
        self.length += 2
    def change(self , event):
        global direction
        if (event.key == pygame.K_LEFT or event.key == pygame.K_a) and direction != "right":
            direction = "left"
        elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and direction != "left":
            direction = "right"
        elif (event.key == pygame.K_UP or event.key == pygame.K_w) and direction != "down":
            direction = "up"
        elif (event.key == pygame.K_DOWN or event.key == pygame.K_s) and direction != "up":
            direction = "down"
    def move(self):
        global direction
        if direction == "left":
            self.rect.x -= 20
        elif direction == "right":
            self.rect.x += 20
        elif direction == "up":
            self.rect.y -= 20
        elif direction == "down":
            self.rect.y += 20

class Food(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((20,20))
        self.image.fill((255 , 0 , 0))
        self.rect = self.image.get_rect()

class History:
    def __init__(self):
        self.l = []
    def add(self,val):
        max = 48*48
        if len(self.l) < max:
            self.l.append(val)
        elif len(self.l) == max:
            self.l.remove(self.l[0])
            self.l.append(val)
        else:
            sys.exit(1)

class SnakeAddition(pygame.sprite.Sprite):
    def __init__(self):
        self.length = 0
        super().__init__()
        self.image = pygame.Surface((20,20))
        self.image.fill((100 , 155 , 0))
        self.rect = self.image.get_rect()
        self.id = len(snake_group) + 2
    def move(self):
        self.rect.x , self.rect.y = hist.l[-self.id]

class Score(pygame.sprite.Sprite):
    def __init__(self,y):
        super().__init__()
        self.image = pygame.Surface((298,20),flags=pygame.SRCALPHA)
        self.image.fill((255,255,255,0))
        self.rect = self.image.get_rect()
        self.font = pygame.font.Font(f"{Path(__file__).parents[0]}/MAINBRG.ttf", 20)
        self.text = self.font.render(f"Your length was: {snake.length + 1}" , True , (255,255,255))
        self.text_rect = self.text.get_rect(center=(500, y))
        self.image.blit(self.text , (0, 0))

class press_enter(pygame.sprite.Sprite):
    def __init__(self,y):
        super().__init__()
        self.image = pygame.Surface((349,20),flags=pygame.SRCALPHA)
        self.image.fill((255,255,255,0))
        self.rect = self.image.get_rect()
        self.font = pygame.font.Font(f"{Path(__file__).parents[0]}/MAINBRG.ttf", 20)
        self.text = self.font.render(f"press ENTER to play again" , True , (255,255,255))
        self.text_rect = self.text.get_rect(center=(500, y))
        self.image.blit(self.text , (0, 0))

class press_q(pygame.sprite.Sprite):
    def __init__(self,y):
        super().__init__()
        self.image = pygame.Surface((203,20),flags=pygame.SRCALPHA)
        self.image.fill((255,255,255,0))
        self.rect = self.image.get_rect()
        self.font = pygame.font.Font(f"{Path(__file__).parents[0]}/MAINBRG.ttf" , 20)
        self.text = self.font.render(f"press Q to quit", True, (255,255,255))
        self.text_rect = self.text.get_rect(center=(500, y))
        self.image.blit(self.text , (0, 0))

class GG(pygame.sprite.Sprite):
    def __init__(self,y):
        super().__init__()
        self.image = pygame.Surface((203,40),flags=pygame.SRCALPHA)
        self.image.fill((255,255,255,0))
        self.rect = self.image.get_rect()
        self.font = pygame.font.Font(f"{Path(__file__).parents[0]}/MAINBRG.ttf" , 40)
        self.text = self.font.render(f"GG", True, (255,255,255))
        self.text_rect = self.text.get_rect(center=(500, y))
        self.image.blit(self.text , (0, 0))

def end_text(y1,y2,y3):
    score = Score(y1)
    enter = press_enter(y2)
    q = press_q(y3)
    screen.blit(score.image,score.text_rect)
    screen.blit(enter.image,enter.text_rect)
    screen.blit(q.image,q.text_rect)

def main():
    pygame.init()
    global screen
    screen = pygame.display.set_mode((1000 , 1000))
    icon = pygame.image.load(f"{Path(__file__).parents[0]}/py.png")
    pygame.display.set_icon(icon)
    pygame.display.set_caption("Snake")
    screen.fill((0 , 0 , 0))
    screen.fill((100 , 100 , 100) , ((20 , 20) , (960 , 960)))
    clock = pygame.time.Clock()

    global snake
    snake = Snake()
    food = Food()
    global hist
    hist = History()
    player_group = pygame.sprite.Group()
    global snake_group
    snake_group = pygame.sprite.Group()
    food_group = pygame.sprite.Group()
    player_group.add(snake)
    food_group.add(food)

    DONE = False
    global direction
    direction = None
    snake.rect.x = 500
    snake.rect.y = 500
    hist.add((snake.rect.x,snake.rect.y))
    x = random.randint(1,48)*20
    y = random.randint(1,48)*20
    food.rect.x = x
    food.rect.y = y
    while not DONE:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                DONE = True
            if event.type == pygame.KEYDOWN:
                snake.change(event)
                break
        snake.move()
        if (snake.rect.x,snake.rect.y) != hist.l[-1]:
            hist.add((snake.rect.x,snake.rect.y))
        for collision in pygame.sprite.spritecollide(snake,food_group,False):
            collision.kill()
            food = Food()
            food_group.add(food)
            snake.grow()
            x = random.randint(1,48)*20
            y = random.randint(1,48)*20
            while (x,y) in [(link.rect.x,link.rect.y) for link in snake_group] or (x,y) == (snake.rect.x,snake.rect.y):
                x = random.randint(1,48)*20
                y = random.randint(1,48)*20
            food.rect.x = x
            food.rect.y = y
        while snake.length != len(snake_group.sprites()):
            snake_addition = SnakeAddition()
            snake_group.add(snake_addition)
            if len(snake_group) + 2 >= 48*48:
                tea = pygame.image.load(f"{Path(__file__).parents[0]}/tea.png")
                screen.blit(tea,(0,0))
                end_text(730,760,790)
                gg = GG(240)
                screen.blit(gg.image,gg.text_rect)
                pygame.display.flip()
                snake.kill()
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            break
                        elif event.key == pygame.K_q:
                            sys.exit()
                else:
                    continue
                main()
        for link in snake_group.sprites():
            try:
                link.move()
            except:
                pass
        screen.fill((0 , 0 , 0))
        screen.fill((100 , 100 , 100) , ((20 , 20) , (960 , 960)))
        player_group.draw(screen)
        snake_group.draw(screen)
        food_group.draw(screen)
        if snake.rect.x < 20 or snake.rect.x > 960 or snake.rect.y < 20 or snake.rect.y > 960 or len(pygame.sprite.spritecollide(snake,snake_group,False)) != 0:
            screen.fill((0 , 0 , 255) , ((snake.rect.x,snake.rect.y), (20 , 20)))
            end_text(470,500,530)
            if snake.alive():
                pygame.display.flip()
            snake.kill()
        if snake.alive():
            pygame.display.flip()
        else:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        break
                    elif event.key == pygame.K_q:
                        sys.exit()
            else:
                continue
            main()
        clock.tick(15)

if __name__=="__main__":
    main()
