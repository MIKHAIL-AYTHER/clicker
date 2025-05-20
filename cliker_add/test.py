import pygame
import sys

pygame.init()

# Константи
WIN_WIDTH = 1200
WIN_HEIGHT = 800
FPS = 60

# Кольори
WHITE = (255, 255, 255)

# Створення вікна
pygame.display.set_caption("анегдот невлез плачим")
window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))


def load_image(path, width=None, height=None):
    """
    Завантажує зображення із файлу.
    При вказівці width та height масштабує зображення до заданого розміру.
    """
    try:
        image = pygame.image.load(path)
        if width is not None and height is not None:
            image = pygame.transform.scale(image, (width, height))
        return image
    except Exception as e:
        print(f"Ошибка загрузки изображения {path}: {e}")
        sys.exit(1)


# Передзавантаження зображень для фонів та кнопок
menu_background = load_image("images/bg/menu_fone.jpg", WIN_WIDTH, WIN_HEIGHT)
game_background = load_image("images/bg/game_1.png", WIN_WIDTH, WIN_HEIGHT)

# Шляхи до зображень кнопок
default_button_image_path = "images/button/bg_btt.png"
hover_button_image_path = "images/button/text.png"
default_hamster_path = "images/hamsters/default/1.png"
hover_hamster_path = "images/hamsters/hovered/1.png"

# Завантажуємо зображення кнопок один раз
default_button_image = load_image(default_button_image_path, 200, 60)
hover_button_image = load_image(hover_button_image_path, 200, 60)
default_hamster = load_image(default_hamster_path, 200, 400)
hover_hamster = load_image(hover_hamster_path, 200, 400)

# Шрифт
font1 = pygame.font.SysFont("Arial", 30)


class Button:
    def __init__(self, x, y, w, h, text, default_image, hover_image, text_color=WHITE):
        self.rect = pygame.Rect(x, y, w, h)
        # Масштабуємо завантажені зображення під розміри кнопки
        self.default_image = pygame.transform.scale(default_image, (w, h))
        self.hover_image = pygame.transform.scale(hover_image, (w, h))
        self.image = self.default_image
        self.text = text
        self.text_color = text_color

    def draw(self, surface):
        """Відображає кнопку із зображенням та текстом."""
        surface.blit(self.image, self.rect.topleft)
        text_img = font1.render(self.text, True, self.text_color)
        text_rect = text_img.get_rect(center=self.rect.center)
        surface.blit(text_img, text_rect)

    def is_clicked(self, pos):
        """Перевіряє, чи знаходиться позиція миші всередині кнопки."""
        return self.rect.collidepoint(pos)

    def update_hover(self, mouse_pos):
        """Обновлює зображення кнопки залежно від положення миші."""
        if self.rect.collidepoint(mouse_pos):
            self.image = self.hover_image
        else:
            self.image = self.default_image


class AutoClicker:
    def __init__(self):
        # Початкові рівні покращень
        self.speed_level = 1         # впливає на інтервал автокліку
        self.quantity_level = 1      # кількість автоклікерів
        self.clicks_level = 1        # кліки за раз
        self.base_interval = 5000    # базовий інтервал у мс
        self.last_time = pygame.time.get_ticks()

        # Базові вартості покращень
        self.speed_cost = 20
        self.quantity_cost = 40
        self.clicks_cost = 25

    def get_interval(self):
        """
        Розраховує інтервал автокліку з покращенням швидкості.
        Кожен рівень зменшує інтервал на 500 мс, але не нижче 1000 мс.
        """
        interval = max(1000, self.base_interval - (self.speed_level - 1) * 500)
        return interval

    def get_auto_clicks(self):
        """
        Загальна кількість кліків, які додаються під час спрацювання автоклікера:
        = (кількість автоклікерів) * (сила автоклікера)
        """
        return self.quantity_level * self.clicks_level

    def upgrade_speed(self, game):
        if game.currency >= self.speed_cost:
            game.currency -= self.speed_cost
            self.speed_level += 1
            self.speed_cost = int(self.speed_cost * 1.5)
            print(f"Поліпшено швидкість автоклікера, новий рівень: {self.speed_level}")
        else:
            print("Недостатньо валюти для покращення швидкості автоклікера!")

    def upgrade_quantity(self, game):
        if game.currency >= self.quantity_cost:
            game.currency -= self.quantity_cost
            self.quantity_level += 1
            self.quantity_cost = int(self.quantity_cost * 1.5)
            print(f"Поліпшено кількість автоклікерів, новий рівень: {self.quantity_level}")
        else:
            print("Недостатньо валюти для покращення кількості автоклікерів!")

    def upgrade_clicks(self, game):
        if game.currency >= self.clicks_cost:
            game.currency -= self.clicks_cost
            self.clicks_level += 1
            self.clicks_cost = int(self.clicks_cost * 1.5)
            print(f"Поліпшено силу автоклікера (кліки за раз), новий рівень: {self.clicks_level}")
        else:
            print("Недостатньо валюти для покращення сили автоклікера!")


class Game:
    def __init__(self):
        # Основна кнопка для кліка (натискаємо на хом'ячка)
        button_width, button_height = 300, 450
        button_x = (WIN_WIDTH - button_width) // 2
        button_y = (WIN_HEIGHT - button_height) // 2
        self.back_to_menu_button = Button(WIN_WIDTH -170, WIN_HEIGHT -170, 150, 50, "← Назад", default_button_image, hover_button_image, WHITE)
        self.game_button = Button(button_x, button_y, button_width, button_height, "Нажми!",
                                  default_hamster, hover_hamster, WHITE)
        # Кнопка прокачування для ручного кліка
        self.upgrade_button = Button(WIN_WIDTH - 210, WIN_HEIGHT - 80, 200, 60, "Прокачка (10)",
                                     default_button_image, hover_button_image, WHITE)

        self.click_count = 0
        self.level = 1
        self.currency = 0
        self.click_multiplier = 1  # 1 клік = 1 очко
        self.upgrade_cost = 10     # Початкова вартість прокачування

        # Бонус за рівень: мінімум 10 валют або level*5, що більше
        # (при кожному підвищенні рівня нараховуватиметься bonus = max(level * 5, 10))

        # Автоклікер: спочатку його треба купити
        self.auto_clicker = AutoClicker()
        self.auto_clicker_enabled = False
        self.auto_clicker_purchase_cost = 100
        self.auto_clicker_purchase_button = Button(WIN_WIDTH - 210, 20, 200, 60,
                                                   f"авто клікер ({self.auto_clicker_purchase_cost})",
                                                   default_button_image, hover_button_image, WHITE)
        # Кнопки для покращення автоклікера (відображаються після покупки)
        self.auto_clicker_speed_button = Button(20, WIN_HEIGHT - 200, 250, 50,
                                                f"Скорость ({self.auto_clicker.speed_cost})",
                                                default_button_image, hover_button_image, WHITE)
        self.auto_clicker_quantity_button = Button(20, WIN_HEIGHT - 140, 250, 50,
                                                   f"Количество ({self.auto_clicker.quantity_cost})",
                                                   default_button_image, hover_button_image, WHITE)
        self.auto_clicker_clicks_button = Button(20, WIN_HEIGHT - 80, 250, 50,
                                                 f"Клики ({self.auto_clicker.clicks_cost})",
                                                 default_button_image, hover_button_image, WHITE)

    def check_level_up(self):
        while self.click_count >= 10 * (3 ** (self.level - 1)):
            required_clicks = 10 * (3 ** (self.level - 1))
            self.level += 1
            bonus = max(self.level * 5, 20)
            self.currency += bonus
            print(f"Новий рівень: {self.level}. Отримано бонусні монети: {bonus} (потрібно {required_clicks} кліков)")
            if self.level in [3, 5, 7, 9]:
                if self.level == 3:
                    default_hamster_path = "images/hamsters/default/2.png"
                    hover_hamster_path = "images/hamsters/hovered/2.png"
                elif self.level == 5:
                    default_hamster_path = "images/hamsters/default/3.png"
                    hover_hamster_path = "images/hamsters/hovered/3.png"
                elif self.level == 7:
                    default_hamster_path = "images/hamsters/default/4.png"
                    hover_hamster_path = "images/hamsters/hovered/4.png"
                elif self.level == 9:
                    default_hamster_path = "images/hamsters/default/5.png"
                    hover_hamster_path = "images/hamsters/hovered/5.png"

                default_hamster = load_image(default_hamster_path, 200, 400)
                hover_hamster = load_image(hover_hamster_path, 200, 400)

                self.game_button = Button(self.game_button.rect.x, self.game_button.rect.y,
                                          self.game_button.rect.width, self.game_button.rect.height, "Нажми!",
                                          default_hamster, hover_hamster, WHITE)

    def upgrade(self):
        """
        Якщо достатньо валюти, виконується прокачування ручного кліку:
        - Віднімається валюта
        - Збільшується множник кліку
        - Вартість покращення зростає приблизно в 1.5 рази
        """
        if self.currency >= self.upgrade_cost:
            self.currency -= self.upgrade_cost
            self.click_multiplier += 1
            self.upgrade_cost = int(self.upgrade_cost * 1.5)
            print(f"Успішне прокачування! Новий множник кліку: {self.click_multiplier}")
        else:
            print("Недостатньо валюти для прокачування!")

    def auto_clicker_tick(self):
        if self.auto_clicker_enabled:
            current_time = pygame.time.get_ticks()
            if current_time - self.auto_clicker.last_time >= self.auto_clicker.get_interval():
                auto_clicks = self.auto_clicker.get_auto_clicks()
                self.click_count += auto_clicks
                print(f"Автоклікер спрацював! Додано {auto_clicks} кліков.")
                self.auto_clicker.last_time = current_time
                self.check_level_up()

    def start(self, surface):
        """
        Малює ігрову сцену: фон, статистику (рівень, кліки, валюта, множник)
        і всі кнопки – для ручного кліка, прокачування, покупки автоклікера та покращення автоклікера.
        """
        surface.blit(game_background, (0, 0))
        # Статистика
        level_text = font1.render(f"Рівень: {self.level}", True, WHITE)
        clicks_text = font1.render(f"Тицьків: {self.click_count}", True, WHITE)
        currency_text = font1.render(f"Хомакоінс: {self.currency}", True, WHITE)
        multiplier_text = font1.render(f"Примноження: {self.click_multiplier}", True, WHITE)
        surface.blit(level_text, (20, 20))
        surface.blit(clicks_text, (20, 60))
        surface.blit(currency_text, (20, 100))
        surface.blit(multiplier_text, (20, 140))

        # Ручний клік та прокачування
        self.game_button.draw(surface)
        self.back_to_menu_button.draw(surface)
        self.upgrade_button.text = f"Покращення ({self.upgrade_cost})"
        self.upgrade_button.draw(surface)

        # Відображення інтерфейсу автоклікера
        if not self.auto_clicker_enabled:
            self.auto_clicker_purchase_button.text = f"Авто клікер ({self.auto_clicker_purchase_cost})"
            self.auto_clicker_purchase_button.draw(surface)
        else:
            self.auto_clicker_speed_button.text = f"Швидкість ({self.auto_clicker.speed_cost})"
            self.auto_clicker_quantity_button.text = f"Кількість ({self.auto_clicker.quantity_cost})"
            self.auto_clicker_clicks_button.text = f"Тицьків ({self.auto_clicker.clicks_cost})"
            self.auto_clicker_speed_button.draw(surface)
            self.auto_clicker_quantity_button.draw(surface)
            self.auto_clicker_clicks_button.draw(surface)


def main():
    clock = pygame.time.Clock()
    scene = "menu"

    # Кнопка переходу з меню на гру
    start_button = Button((WIN_WIDTH -200) // 2,(WIN_HEIGHT -60) // 2, 200, 60, "Грати",
                          default_button_image, hover_button_image, WHITE)
    game = Game()

    while True:
        mouse_pos = pygame.mouse.get_pos()

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
                    # Ручний клік (хом'ячок)
                    if game.game_button.is_clicked(pos):
                        game.click_count += game.click_multiplier
                        print(f"Натиснута кнопка гри, клік додав {game.click_multiplier}. Рахунок: {game.click_count}")
                        game.check_level_up()
                    # Прокачування ручного кліку
                    elif game.upgrade_button.is_clicked(pos):
                        game.upgrade()
                    elif game.back_to_menu_button.is_clicked(pos):
                        print("Повернення в меню!")
                        scene = "menu"
                    # Інтерфейс автоклікера:
                    if not game.auto_clicker_enabled:
                        if game.auto_clicker_purchase_button.is_clicked(pos):
                            if game.currency >= game.auto_clicker_purchase_cost:
                                game.currency -= game.auto_clicker_purchase_cost
                                game.auto_clicker_enabled = True
                                game.auto_clicker.last_time = pygame.time.get_ticks()
                                print("Автоклікер куплено!")
                            else:
                                print("Недостатньо валюти для покупки автоклікера!")
                    else:
                        if game.auto_clicker_speed_button.is_clicked(pos):
                            game.auto_clicker.upgrade_speed(game)
                        elif game.auto_clicker_quantity_button.is_clicked(pos):
                            game.auto_clicker.upgrade_quantity(game)
                        elif game.auto_clicker_clicks_button.is_clicked(pos):
                            game.auto_clicker.upgrade_clicks(game)

        if scene == "menu":
            window.blit(menu_background, (0, 0))
            start_button.update_hover(mouse_pos)
            start_button.draw(window)
        elif scene == "game":
            game.auto_clicker_tick()  # Перевірка автоклікера на кожну ітерацію
            game.start(window)
            game.game_button.update_hover(mouse_pos)
            game.back_to_menu_button.update_hover(mouse_pos)
            game.upgrade_button.update_hover(mouse_pos)
            if not game.auto_clicker_enabled:
                game.auto_clicker_purchase_button.update_hover(mouse_pos)
            else:
                game.auto_clicker_speed_button.update_hover(mouse_pos)
                game.auto_clicker_quantity_button.update_hover(mouse_pos)
                game.auto_clicker_clicks_button.update_hover(mouse_pos)

        pygame.display.update()
        clock.tick(FPS)


if __name__ == '__main__':
    main()
