import pygame
import os

pygame.font.init()  # Шрифты
pygame.mixer.init()  # Звук

# Настройка дисплея
WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("First Game!")

WHITE = (255, 255, 255)  # Белый цвет
BLACK = (0, 0, 0)  # Чёрный цвет
RED = (255, 0, 0)  # Красный цвет
YELLOW = (255, 255, 0)  # Жёлтый цвет

BORDER = pygame.Rect(WIDTH // 2 - 5, 0, 10, HEIGHT)  # Размер и расположение границы

HEALTH_FONT = pygame.font.SysFont('comicsans', 30)  # Шрифт
WINNER_FONT = pygame.font.SysFont('comicsans', 100)  # Шрифт

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'grenade.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'gun.mp3'))

FPS = 60  # Задержка
VEL = 5  # Скорость караблей
BULLET_VEL = 10  # Скорость пули
MAX_BULLETS = 5  # Максимальное кол-во пуль
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 70, 50  # Размер караблей
# Создаём объект пользователя
YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

# Загружаем картинки караблей
YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join(
    'Assets', 'spaceship_yellow.png'))
# Изменение размера изображения, и поворот
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE,
                                                                  (SPACESHIP_WIDTH,
                                                                   SPACESHIP_HEIGHT)), 90)
RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join(
    'Assets', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE,
                                                               (SPACESHIP_WIDTH,
                                                                SPACESHIP_HEIGHT)), 270)
# Добавляем фон и подгоняем по размеру
SPACE = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT))


# Функция окна
def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    WIN.blit(SPACE, (0, 0))  # Фон
    pygame.draw.rect(WIN, BLACK, BORDER)  # Добавляем границу
    red_health_text = HEALTH_FONT.render("Health: " + str(red_health), 1,
                                         WHITE)  # Выводим на экран здоровье по координатам X,Y
    yellow_health_text = HEALTH_FONT.render("Health: " + str(yellow_health), 1, WHITE)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, 10))
    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))  # Вывод на экран по координатам X,Y
    WIN.blit(RED_SPACESHIP, (red.x, red.y))

    # Прорисовываем пули
    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)
    # Обновление окна
    pygame.display.update()


# Функция движения жёлтого корабля + граници движения по координатам
def yellow_handle_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0:  # Лево
        yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x:  # Право
        yellow.x += VEL
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0:  # Вверх
        yellow.y -= VEL
    if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT - 10:  # Вниз
        yellow.y += VEL


# Функция движения красного корабля + граници движения по координатам
def red_handle_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width:  # Лево
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH:  # Право
        red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0:  # Вверх
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT - 10:  # Вниз
        red.y += VEL


# Функция стрельбы
def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):  # Проверка столкновения пули с кораблём
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:  # Обрабатываем вылет пули за пределы поля
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):  # Проверка столкновения пули с кораблём
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)


# Вывод победителя на экран
def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH / 2 - draw_text.get_width() / 2, HEIGHT / 2 - draw_text.get_height() / 2))
    pygame.display.update()
    pygame.time.delay(5000)  # Пауза перед рестартом


# Основной цикл игры
def main():
    # Определяем положение караблей
    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    red_bullets = []
    yellow_bullets = []

    red_health = 10  # Кол-во жизней
    yellow_health = 10

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)  # устанавливаем 60 fps
        # Цикл выхода из игры
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            # Настройка выстрелов
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height // 2 + 2, 10, 5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x, red.y + red.height // 2 + 7, 10, 5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()
            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()

        winner_text = ""
        if red_health <= 0:
            winner_text = "Yellow Wins!"

        if yellow_health <= 0:
            winner_text = "Red Wins!"

        if winner_text != "":
            draw_winner(winner_text)
            break

        # Настройка клавишь
        keys_pressed = pygame.key.get_pressed()
        yellow_handle_movement(keys_pressed, yellow)
        red_handle_movement(keys_pressed, red)
        handle_bullets(yellow_bullets, red_bullets, yellow, red)
        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)

    main()


if __name__ == "__main__":
    main()
