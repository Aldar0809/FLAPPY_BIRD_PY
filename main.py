import pygame
import sys
import random
import configparser
import os

pygame.init()
pygame.mixer.init()
jump_sound = pygame.mixer.Sound('data/jump_sound.mp3')
crash_sound = pygame.mixer.Sound('data/collision_sound.wav')
score_sound = pygame.mixer.Sound('data/score_sound.mp3')

# Определение констант
WIDTH, HEIGHT = 1000, 600
FPS = 60
GROUND_HEIGHT = 100
GRAVITY = 1
JUMP_POWER = -12
PIPE_SPEED = 8
PIPE_PAIR_SEC_DISTANCE = 800
BIRD_SIZE = 1.0

# Определение цветов
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Загрузка изображений
upward_pipe_image = pygame.image.load('data/stolb-up.png')
downward_pipe_image = pygame.image.load('data/stolb-down.png')
background_image = pygame.image.load('data/background.png')
ground_image = pygame.image.load('data/ground.png')
start_screen_image = pygame.image.load('data/start_screen.png')

# Создание экрана
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Создание групп спрайтов
all_sprites = pygame.sprite.Group()
pipes = pygame.sprite.Group()

# Определение константы для файла конфигурации
config_file = 'settings.ini'

# Проверка наличия файла и создание его, если он отсутствует
if not os.path.exists(config_file):
    config = configparser.ConfigParser()
    config.add_section('GameSettings')
    config['GameSettings'] = {
        'GROUND_HEIGHT': str(GROUND_HEIGHT),
        'GRAVITY': str(GRAVITY),
        'JUMP_POWER': str(JUMP_POWER),
        'PIPE_SPEED': str(PIPE_SPEED),
        'PIPE_PAIR_SEC_DISTANCE': str(PIPE_PAIR_SEC_DISTANCE),
        'BIRD_SIZE': str(BIRD_SIZE)
    }
    with open(config_file, 'w') as configfile:
        config.write(configfile)

# Теперь считываем параметры из файла
config = configparser.ConfigParser()
config.add_section('GameSettings')
config.read(config_file)

# Получение значений параметров из конфигурации
GROUND_HEIGHT = int(config['GameSettings'].get('GROUND_HEIGHT', GROUND_HEIGHT))
GRAVITY = int(config['GameSettings'].get('GRAVITY', GRAVITY))
JUMP_POWER = int(config['GameSettings'].get('JUMP_POWER', JUMP_POWER))
PIPE_SPEED = int(config['GameSettings'].get('PIPE_SPEED', PIPE_SPEED))
PIPE_PAIR_SEC_DISTANCE = int(config['GameSettings'].get('PIPE_PAIR_SEC_DISTANCE', PIPE_PAIR_SEC_DISTANCE))
BIRD_SIZE = float(config['GameSettings'].get('BIRD_SIZE', BIRD_SIZE))



# Функция для отображения и обработки экрана настроек
def show_settings_screen():
    global GROUND_HEIGHT, GRAVITY, JUMP_POWER, PIPE_SPEED, PIPE_PAIR_SEC_DISTANCE, BIRD_SIZE

    config = configparser.ConfigParser()

    settings_font = pygame.font.Font(None, 36)
    selected_param = 0  # Индекс выбранного параметра

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # Сохранение параметров в файл перед выходом
                    with open('settings.ini', 'w') as configfile:
                        config.write(configfile)
                    return  # Вернуться к игре
                elif event.key == pygame.K_RIGHT:
                    # Увеличить значение выбранного параметра
                    if selected_param == 0:
                        GROUND_HEIGHT += 10
                    elif selected_param == 1:
                        GRAVITY += 1
                    elif selected_param == 2:
                        JUMP_POWER += 1
                    elif selected_param == 3:
                        PIPE_SPEED += 1
                    elif selected_param == 4:
                        PIPE_PAIR_SEC_DISTANCE += 10
                    elif selected_param == 5:
                        BIRD_SIZE += 0.1  # Изменено на увеличение размера птицы на 0.1
                elif event.key == pygame.K_LEFT:
                    # Уменьшить значение выбранного параметра
                    if selected_param == 0:
                        GROUND_HEIGHT -= 10
                    elif selected_param == 1:
                        GRAVITY -= 1
                    elif selected_param == 2:
                        JUMP_POWER -= 1
                    elif selected_param == 3:
                        PIPE_SPEED -= 1
                    elif selected_param == 4:
                        PIPE_PAIR_SEC_DISTANCE -= 10
                    elif selected_param == 5:
                        BIRD_SIZE -= 0.1  # Изменено на уменьшение размера птицы на 0.1

                    # Защита от отрицательных значений
                    if GROUND_HEIGHT < 0:
                        GROUND_HEIGHT = 0
                    if GRAVITY < 0:
                        GRAVITY = 0
                    if JUMP_POWER < -20:
                        JUMP_POWER = -20
                    if PIPE_SPEED < 1:
                        PIPE_SPEED = 1
                    if PIPE_PAIR_SEC_DISTANCE < 10:
                        PIPE_PAIR_SEC_DISTANCE = 10
                    if BIRD_SIZE < 0.1:  # Задайте минимальное значение размера птицы по желанию
                        BIRD_SIZE = 0.1

                elif event.key == pygame.K_DOWN:
                    # Переключиться на следующий параметр
                    selected_param = (selected_param + 1) % 6
                elif event.key == pygame.K_UP:
                    # Переключиться на предыдущий параметр
                    selected_param = (selected_param - 1) % 6

                # Ограничение диапазона значений
                GROUND_HEIGHT = max(0, GROUND_HEIGHT)
                GRAVITY = max(0, GRAVITY)
                JUMP_POWER = max(-20, JUMP_POWER)
                PIPE_SPEED = max(1, PIPE_SPEED)
                PIPE_PAIR_SEC_DISTANCE = max(10, PIPE_PAIR_SEC_DISTANCE)
                BIRD_SIZE = max(0.1, BIRD_SIZE)

                # Сохранение параметров в конфигурационный файл
                config['GameSettings'] = {
                    'GROUND_HEIGHT': str(GROUND_HEIGHT),
                    'GRAVITY': str(GRAVITY),
                    'JUMP_POWER': str(JUMP_POWER),
                    'PIPE_SPEED': str(PIPE_SPEED),
                    'PIPE_PAIR_SEC_DISTANCE': str(PIPE_PAIR_SEC_DISTANCE),
                    'BIRD_SIZE': str(BIRD_SIZE)
                }

                # Обновление текста параметров
                selected_param = min(5, max(0, selected_param))  # Ограничение диапазона выбора параметров

        screen.fill((255, 255, 255))
        screen.blit(background_image, (0, 0))

        settings_text = settings_font.render("Настройки", True, (0, 0, 0))
        screen.blit(settings_text, (WIDTH // 2 - 50, 50))

        settings_info = [
            f"GROUND_HEIGHT: {GROUND_HEIGHT}",
            f"GRAVITY: {GRAVITY}",
            f"JUMP_POWER: {JUMP_POWER}",
            f"PIPE_SPEED: {PIPE_SPEED}",
            f"PIPE_PAIR_SEC_DISTANCE: {PIPE_PAIR_SEC_DISTANCE}",
            f"BIRD_SIZE: {BIRD_SIZE}",
            "Используйте стрелки ВВЕРХ/ВНИЗ/ВПРАВО/ВЛЕВО для изменения, Escape - вернуться к игре"
        ]

        for i, text in enumerate(settings_info):
            if i == selected_param:
                text_render = settings_font.render(text, True, (255, 0, 0))
            else:
                text_render = settings_font.render(text, True, (0, 0, 0))
            screen.blit(text_render, (50, 100 + i * 40))

        pygame.display.flip()
        clock.tick(FPS)


# Создание класса для птицы
class Bird(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.index = 0
        self.images = [pygame.image.load('data/bird1.png'),
                       pygame.image.load('data/bird2.png'),
                       pygame.image.load('data/bird3.png')]
        self.image = self.images[self.index].convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (100, HEIGHT // 2)
        self.velocity = 0
        self.animation_speed = 5
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.velocity += GRAVITY
        self.rect.y += self.velocity
        self.animate_wings()

        # Учет размера птицы
        scaled_width = int(self.images[0].get_width() * BIRD_SIZE)
        scaled_height = int(self.images[0].get_height() * BIRD_SIZE)
        self.image = pygame.transform.scale(self.images[self.index // self.animation_speed].convert_alpha(),
                                           (scaled_width, scaled_height))

        if self.rect.bottom > HEIGHT - GROUND_HEIGHT:
            self.rect.bottom = HEIGHT - GROUND_HEIGHT
            self.velocity = 0
            game_over_function()

        if self.rect.top < 0:
            self.rect.top = 0
            self.velocity = 0

        self.mask = pygame.mask.from_surface(self.image)

    def animate_wings(self):
        self.index += 1
        if self.index >= len(self.images) * self.animation_speed:
            self.index = 0
        self.image = self.images[self.index // self.animation_speed].convert_alpha()


# Создание класса для столбов
class PipePair(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        self.upward_pipe = downward_pipe_image
        self.downward_pipe = upward_pipe_image
        self.gap_height = random.randint(150, HEIGHT - GROUND_HEIGHT - 150)
        self.pipe_width = self.upward_pipe.get_width()
        self.pipe_height = self.upward_pipe.get_height()
        self.scaled_upward_pipe = pygame.transform.scale(self.upward_pipe, (self.pipe_width, self.gap_height))
        self.scaled_downward_pipe = pygame.transform.scale(self.downward_pipe,
                                                           (self.pipe_width, HEIGHT - self.gap_height - GROUND_HEIGHT))
        self.image = pygame.Surface((self.pipe_width, HEIGHT), pygame.SRCALPHA)
        self.rect = self.image.get_rect(topleft=(x, 0))
        self.mask = pygame.mask.from_surface(self.image)
        self.passed = False

        self.image.blit(self.scaled_upward_pipe, (0, 0))
        self.image.blit(self.scaled_downward_pipe, (0, self.gap_height + 150))

    def update(self):
        self.rect.x -= PIPE_SPEED
        self.mask = pygame.mask.from_surface(self.image)

        # Проверка и коррекция, чтобы столбы не выходили за границы экрана
        if self.rect.right < 0:
            self.kill()


# Функция завершения игры
def game_over_function():
    global game_over
    game_over = True


# Функция обновления лучшего счета
def update_best_score(current_score):
    try:
        with open('data/best.txt', 'r') as file:
            best_score = int(file.read())
    except FileNotFoundError:
        # Если файл не найден, создаем его
        best_score = 0

    if current_score > best_score:
        best_score = current_score

        # Обновляем лучший счет в файле
        with open('data/best.txt', 'w') as file:
            file.write(str(best_score))

    # Отображаем лучший счет на экране
    font = pygame.font.Font(None, 36)
    best_score_text = font.render(f"Best: {best_score}", True, (0, 0, 0))
    screen.blit(best_score_text, (10, 50))


# Создание экземпляров классов
bird = Bird()
all_sprites.add(bird)

# Основной игровой цикл
clock = pygame.time.Clock()
game_over = False
score = 0
spawn_pipe_event = pygame.USEREVENT + 1
pygame.time.set_timer(spawn_pipe_event, PIPE_PAIR_SEC_DISTANCE)
scored_pipe = None
crash = False

show_start_screen = True
while show_start_screen:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                show_start_screen = False

    screen.blit(start_screen_image, (0, 0))
    pygame.display.flip()
    clock.tick(FPS)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                show_settings_screen()
            elif event.key == pygame.K_SPACE and not game_over:
                bird.velocity = JUMP_POWER
                jump_sound.play()
        elif event.type == spawn_pipe_event:
            pipe_pair = PipePair(WIDTH)
            pipes.add(pipe_pair)
            all_sprites.add(pipe_pair)
            scored_pipe = None
            pygame.time.set_timer(spawn_pipe_event, PIPE_PAIR_SEC_DISTANCE)

    all_sprites.update()

    # Обработка столкновений
    hit_pipe_pairs = pygame.sprite.spritecollide(bird, pipes, False, pygame.sprite.collide_mask)
    if hit_pipe_pairs:
        if not game_over:
            game_over_function()
            # Здесь можно обновить лучший счет и записать его в файл
            update_best_score(score)

    if not game_over:
        for pipe_pair in pipes:
            if pipe_pair.rect.right < 0:
                pipes.remove(pipe_pair)
                all_sprites.remove(pipe_pair)

            # Проверка, прошла ли птица через столбы
            if not pipe_pair.passed and pipe_pair.rect.right < bird.rect.centerx:
                pipe_pair.passed = True
                score += 1  # Yвеличение счета на 1
                score_sound.play()

        screen.fill(WHITE)
        screen.blit(background_image, (0, 0))
        all_sprites.draw(screen)
        screen.blit(ground_image, (0, HEIGHT - GROUND_HEIGHT))

        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {score}", True, (0, 0, 0))
        screen.blit(score_text, (10, 10))

        # Отображение лучшего счета
        update_best_score(score)

        pygame.display.flip()
        clock.tick(FPS)
    else:
        if not crash:  # Проверка, активен ли звук столкновения
            crash_sound.play()
            crash = True

        font_large = pygame.font.Font(None, 72)
        game_over_text = font_large.render("Game Over", True, RED)
        screen.blit(game_over_text, (WIDTH // 2 - 150, HEIGHT // 2 - 50))

        score_text = font_large.render(f"Score: {score}", True, (0, 0, 0))
        screen.blit(score_text, (WIDTH // 2 - 60, HEIGHT // 2 + 20))

        restart_text = font_large.render("Press R to Restart", True, (0, 0, 0))
        screen.blit(restart_text, (WIDTH // 2 - 180, HEIGHT // 2 + 90))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    all_sprites.empty()
                    pipes.empty()
                    bird = Bird()
                    all_sprites.add(bird)
                    game_over = False
                    score = 0
                    spawn_pipe_event = pygame.USEREVENT + 1
                    pygame.time.set_timer(spawn_pipe_event, 1500)
                    scored_pipe = None
                    crash = False

                clock.tick(FPS)

