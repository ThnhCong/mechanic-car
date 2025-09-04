import pygame
import sys
import math

pygame.init()

# Kích thước cửa sổ
WIDTH, HEIGHT = 1000, 300
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mô phỏng chuyển động: x(t) = -4t + 2t^2")

# Màu sắc
WHITE = (255, 255, 255)
GRAY = (220, 220, 220)
BLUE = (0, 100, 255)
GREEN = (0, 200, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Đơn vị
PIXELS_PER_METER = 50  # 1 m = 50 pixel để thấy rõ hơn
METER_PER_PIXEL = 1 / PIXELS_PER_METER

# Font
font = pygame.font.SysFont(None, 24)
big_font = pygame.font.SysFont(None, 28)

# Tải ảnh xe (đã resize)
car_image = pygame.image.load("car.jpg").convert_alpha()
car_image = pygame.transform.scale(car_image, (120, 60))

# Thông số xe
car_width, car_height = car_image.get_size()
road_y = HEIGHT - 40  # mặt đường cao cách đáy 40 px
car_y = road_y - car_height

clock = pygame.time.Clock()
FPS = 60

# Vị trí ban đầu
START_X = WIDTH // 4  # xuất phát từ khoảng 1/4 màn hình

# --- Trạng thái mô phỏng ---
time_elapsed = 0.0
car_x = START_X
velocity = 0.0
acceleration = 0.0
displacement = 0.0

# --- Nút restart ---
restart_rect = pygame.Rect(WIDTH - 130, 20, 100, 30)

def reset_simulation():
    global time_elapsed, car_x, velocity, acceleration, displacement
    time_elapsed = 0.0
    car_x = START_X
    velocity = 0.0
    acceleration = 0.0
    displacement = 0.0

def draw_arrow(surface, x, y, length_m, color, label=''):
    length_px = length_m * PIXELS_PER_METER
    if abs(length_px) < 1:
        return
    end_x = x + length_px
    pygame.draw.line(surface, color, (x, y), (end_x, y), 3)
    pygame.draw.polygon(surface, color, [(end_x, y),
                                         (end_x - 8 * math.copysign(1, length_px), y - 5),
                                         (end_x - 8 * math.copysign(1, length_px), y + 5)])
    if label:
        text = font.render(label, True, color)
        surface.blit(text, (x + length_px / 2, y - 20))

def draw_ui():
    # Vẽ mặt đường
    pygame.draw.line(screen, GRAY, (0, road_y), (WIDTH, road_y), 2)

    # Vector vật lý
    draw_arrow(screen, car_x + car_width // 2, car_y + car_height + 20, velocity, BLUE, 'v (m/s)')
    draw_arrow(screen, car_x + car_width // 2, car_y + car_height + 40, acceleration, GREEN, 'a (m/s²)')

    # Thông tin vật lý
    info_y = road_y + 10
    s_text = font.render(f"Độ dời s': {displacement:.2f} m", True, BLACK)
    v_text = font.render(f"Vận tốc v: {velocity:.2f} m/s", True, BLACK)
    a_text = font.render(f"Gia tốc a: {acceleration:.2f} m/s²", True, BLACK)
    t_text = font.render(f"Thời gian t: {time_elapsed:.2f} s", True, BLACK)

    screen.blit(s_text, (30, info_y))
    screen.blit(v_text, (300, info_y))
    screen.blit(a_text, (500, info_y))
    screen.blit(t_text, (700, info_y))

    # Nút Restart
    pygame.draw.rect(screen, RED, restart_rect, border_radius=5)
    restart_label = big_font.render("Restart", True, WHITE)
    screen.blit(restart_label, (restart_rect.x + 15, restart_rect.y + 5))

# === Vòng lặp chính ===
while True:
    dt = clock.tick(FPS) / 1000  # giây
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if restart_rect.collidepoint(event.pos):
                reset_simulation()

    # Cập nhật theo phương trình x(t) = -4t + 2t^2
    time_elapsed += dt
    x_m = -4 * time_elapsed + 2 * (time_elapsed ** 2)  # mét
    displacement = x_m
    car_x = START_X + x_m * PIXELS_PER_METER

    velocity = -4 + 4 * time_elapsed   # m/s
    acceleration = 4                   # m/s² (hằng số)

    # Vẽ xe
    screen.blit(car_image, (car_x, car_y))

    draw_ui()
    pygame.display.flip()
