import pygame
import sys

pygame.init()

# Константы
WIN_WIDTH = 700
WIN_HEIGHT = 500
FPS = 60

# Цвета
WHITE = (255, 255, 255)

# Создание окна
pygame.display.set_caption("анегдот невлез плачим")
window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))


def load_image(path, width=None, height=None):
    """
    Загружает изображение из файла.
    При указании width и height масштабирует изображение до заданного размера.
    Если произошла ошибка, выводит сообщение и завершает работу.
    """
    try:
        image = pygame.image.load(path)
        if width is not None and height is not None:
            image = pygame.transform.scale(image, (width, height))
        return image
    except Exception as e:
        print(f"Ошибка загрузки изображения {path}: {e}")
        sys.exit(1)


# Предзагрузка изображений для фонов и кнопок
menu_background = load_image("images/bg/menu_fone.jpg", WIN_WIDTH, WIN_HEIGHT)
game_background = load_image("images/bg/game_1.png", WIN_WIDTH, WIN_HEIGHT)


# Пути к изображениям кнопок
default_button_image_path = "images/button/bg_btt.png"
hover_button_image_path = "images/button/text.png"
default_hamster_path = "images/hamsters/default/1.png"
hover_hamster_path = "images/hamsters/hovered/1.png"
# Загружаем изображения кнопок один раз
default_button_image = load_image(default_button_image_path, 200, 60)
hover_button_image = load_image(hover_button_image_path, 200, 60)
default_hamster = load_image(default_hamster_path, 200, 400)
hover_hamster = load_image(hover_hamster_path, 200, 400)
# Шрифт
font1 = pygame.font.SysFont("Arial", 30)


class Button:
    def __init__(self, x, y, w, h, text, default_image, hover_image, text_color=WHITE):
        self.rect = pygame.Rect(x, y, w, h)
        # Масштабируем загруженные изображения под размеры кнопки
        self.default_image = pygame.transform.scale(default_image, (w, h))
        self.hover_image = pygame.transform.scale(hover_image, (w, h))
        self.image = self.default_image
        self.text = text
        self.text_color = text_color

    def draw(self, surface):
        """Отрисовывает кнопку с изображением и текстом."""
        surface.blit(self.image, self.rect.topleft)
        text_img = font1.render(self.text, True, self.text_color)
        text_rect = text_img.get_rect(center=self.rect.center)
        surface.blit(text_img, text_rect)

    def is_clicked(self, pos):
        """Проверяет, находится ли позиция мыши внутри кнопки."""
        return self.rect.collidepoint(pos)

    def update_hover(self, mouse_pos):
        """Обновляет изображение кнопки в зависимости от положения мыши."""
        if self.rect.collidepoint(mouse_pos):
            self.image = self.hover_image
        else:
            self.image = self.default_image


class Game:
    def __init__(self):
        button_width, button_height = 300, 450
        # Центрируем кнопку на экране
        button_x = (WIN_WIDTH - button_width) // 2
        button_y = (WIN_HEIGHT - button_height) // 2
        self.game_button = Button(button_x, button_y, button_width, button_height, "нажми",
                                  default_hamster, hover_hamster, WHITE)
        self.click_count = 0

    def start(self, surface):
        """Отрисовывает игровую сцену с фоном, текстом и кнопкой."""
        surface.blit(game_background, (0, 0))
        # Отрисовка текста "Тут буде гра!" по центру по горизонтали (Y=220)
        text = font1.render("Тут буде гра!", True, WHITE)
        text_rect = text.get_rect(center=(WIN_WIDTH // 2, 220))
        surface.blit(text, text_rect)
        # Обновляем текст кнопки с учётом счётчика кликов
        self.game_button.text = f"Clicks: {self.click_count}"
        self.game_button.draw(surface)


def main():
    clock = pygame.time.Clock()
    scene = "menu"

    # Кнопка перехода на игровую сцену (сцена меню)
    start_button = Button(250, 330, 200, 60, "Test_Button",
                          default_button_image, hover_button_image, WHITE)
    game = Game()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                if scene == "menu":
                    if start_button.is_clicked(pos):
                        print("Переходимо до гри!")
                        scene = "game"
                elif scene == "game":
                    if game.game_button.is_clicked(pos):
                        game.click_count += 1
                        print("Кнопка игры нажата, счёт:", game.click_count)

        mouse_pos = pygame.mouse.get_pos()

        if scene == "menu":
            window.blit(menu_background, (0, 0))
            start_button.update_hover(mouse_pos)
            start_button.draw(window)
        elif scene == "game":
            game.start(window)
            game.game_button.update_hover(mouse_pos)

        pygame.display.update()
        clock.tick(FPS)


if __name__ == '__main__':
    main()
