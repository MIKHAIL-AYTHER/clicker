import pygame

pygame.init()

# створюємо вікно
win_width = 700
win_height = 500
pygame.display.set_caption("анегдот невлез плачим")
window = pygame.display.set_mode((win_width, win_height))

# фони
menu_background = pygame.transform.scale(pygame.image.load("menu_fone.jpg"), (win_width, win_height))
game_background = pygame.Surface((win_width, win_height))
game_background.fill((100, 200, 100))  # зелений фон для гри

# кольори та шрифт
WHITE = (255, 255, 255)
font1 = pygame.font.SysFont("Arial", 30)

# клас кнопки з фоновим зображенням
class Button:
    def __init__(self, x, y, w, h, text, image_path, text_color):
        self.rect = pygame.Rect(x, y, w, h)
        self.image = pygame.transform.scale(pygame.image.load(image_path), (w, h))
        self.text = text
        self.text_color = text_color

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)  # кнопка як зображення
        text_img = font1.render(self.text, True, self.text_color)
        text_rect = text_img.get_rect(center=self.rect.center)
        surface.blit(text_img, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

# створюємо кнопку з фоном-картинкою
start_button = Button(250, 330, 200, 60, "Test_Button", "bg_btt.png", WHITE)

# керування сценами
scene = "menu"
run = True
while run:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            run = False
        elif e.type == pygame.MOUSEBUTTONDOWN:
            if scene == "menu" and start_button.is_clicked(e.pos):
                print("Переходимо до гри!")
                scene = "game"

    if scene == "menu":
        window.blit(menu_background, (0, 0))
        start_button.draw(window)
         x,y = mouse.get_pos()
        if start_button.rect.collidepoint(x,y):
            start_button.image = pygame.transform.scale(pygame.image.load(), (w, h))
        else:
            start_button.image = pygame.transform.scale(pygame.image.load(), (w, h))
    elif scene == "game":
        window.blit(game_background, (0, 0))
        text = font1.render("Тут буде гра!", True, WHITE)
        window.blit(text, (250, 220))

    pygame.display.update()
    pygame.time.delay(50)
