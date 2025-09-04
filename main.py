import pygame
import sys
import math
import time

pygame.init()

# Kích thước cửa sổ
WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mô phỏng xe vật lý")

# Màu sắc
WHITE = (255, 255, 255)
GRAY = (220, 220, 220)
BLUE = (0, 100, 255)
GREEN = (0, 200, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Đơn vị
PIXELS_PER_METER = 20
METER_PER_PIXEL = 1 / PIXELS_PER_METER

# Font
font = pygame.font.SysFont(None, 24)
big_font = pygame.font.SysFont(None, 28)

# Tải ảnh xe (đã resize)
car_image = pygame.image.load("car.jpg").convert_alpha()
car_image = pygame.transform.scale(car_image, (120, 60))

# Thông số xe
car_width, car_height = car_image.get_size()
road_y = HEIGHT - 20  # mặt đường cao cách đáy màn hình 20 px
car_y = road_y - car_height

clock = pygame.time.Clock()
FPS = 60

# Vị trí ban đầu
START_X = WIDTH // 2

# --- Trạng thái mô phỏng ---
car_x = START_X
car_dragging = False
velocity = 0.0        # m/s
acceleration = 0.0    # m/s²
drag_accel = -3.0     # m/s² khi phanh
mode = 0              # 0: tự do, 1: phanh

elapsed_time = 0.0
displacement = 0.0    # m
distance_traveled = 0.0  # m
last_px = car_x
has_started = False   # Đã từng kéo xe hay chưa

# --- Nút restart ---
restart_rect = pygame.Rect(WIDTH - 130, 20, 100, 30)

def reset_simulation():
    global car_x, velocity, acceleration, elapsed_time
    global displacement, distance_traveled, has_started
    car_x = START_X
    velocity = 0.0
    acceleration = 0.0
    elapsed_time = 0.0
    displacement = 0.0
    distance_traveled = 0.0
    has_started = False

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

    # Thông tin vật lý (hiện dưới mặt đường)
    info_y = road_y + 10
    s_text = font.render(f"Độ dời s': {displacement:.2f} m", True, BLACK)
    s_real_text = font.render(f"Quãng đường s: {distance_traveled:.2f} m", True, BLACK)
    v_text = font.render(f"Vận tốc v: {velocity:.2f} m/s", True, BLACK)
    a_text = font.render(f"Gia tốc a: {acceleration:.2f} m/s²", True, BLACK)
    t_text = font.render(f"Thời gian t: {elapsed_time:.2f} s", True, BLACK)
    mode_text = font.render(f"Chế độ: {'Dùng phanh' if mode else 'Tự do'} (SPACE để đổi)", True, RED)

    screen.blit(s_text, (30, info_y))
    screen.blit(s_real_text, (250, info_y))
    screen.blit(v_text, (500, info_y))
    screen.blit(a_text, (700, info_y))
    screen.blit(t_text, (850, info_y))
    screen.blit(mode_text, (30, info_y + 25))

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

        # Nhấn chuột vào xe để kéo
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.Rect(car_x, car_y, car_width, car_height).collidepoint(event.pos):
                car_dragging = True
                velocity = 0
                acceleration = 0
                has_started = True

            # Kiểm tra nhấn nút restart
            elif restart_rect.collidepoint(event.pos):
                reset_simulation()

        elif event.type == pygame.MOUSEBUTTONUP:
            if car_dragging:
                car_dragging = False
                dx_px = car_x - last_px
                velocity = dx_px * METER_PER_PIXEL / dt if dt > 0 else 0
                acceleration = 0 if mode == 0 else drag_accel * math.copysign(1, velocity)

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                mode = 1 - mode
                if not car_dragging:
                    acceleration = 0 if mode == 0 else drag_accel * math.copysign(1, velocity)

    if car_dragging:
        mx, _ = pygame.mouse.get_pos()
        last_px = car_x
        car_x = mx - car_width // 2
        velocity = (car_x - last_px) * METER_PER_PIXEL / dt if dt > 0 else 0
        acceleration = 0
    elif has_started:
        car_x += velocity * dt * PIXELS_PER_METER
        velocity += acceleration * dt

        if mode == 1 and abs(velocity) < 0.05:
            velocity = 0
            acceleration = 0

    car_x = max(0, min(car_x, WIDTH - car_width))

    # Cập nhật thông số
    displacement = (car_x - START_X) * METER_PER_PIXEL
    if has_started:
        distance_traveled += abs(velocity) * dt

    if has_started and not car_dragging:
        if abs(velocity) < 1e-3:  # xe dừng hẳn
            elapsed_time = 0.0
        else:
            if mode == 0:  # tự do
                elapsed_time = abs(displacement) / max(abs(velocity), 1e-5)
            else:  # có phanh
                if acceleration != 0:
                    v0 = math.sqrt(max(velocity ** 2 - 2 * acceleration * displacement, 0))
                    elapsed_time = abs((velocity - v0) / acceleration)
                else:
                    elapsed_time = 0.0
    elif not has_started:
        elapsed_time = 0.0

    # Vẽ xe
    screen.blit(car_image, (car_x, car_y))

    draw_ui()
    pygame.display.flip()
