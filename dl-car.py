import pygame
import sys
import math
import matplotlib.animation as animation
pygame.init()

# Kích thước cửa sổ
WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mô phỏng chuyển động: x(t) = -4t + 2t^2")

# Màu sắc
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLUE = (0, 100, 255)
GREEN = (0, 200, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Đơn vị
PIXELS_PER_METER = 50  # 1 m = 50 pixel
METER_PER_PIXEL = 1 / PIXELS_PER_METER

# Font
font = pygame.font.SysFont(None, 24)
big_font = pygame.font.SysFont(None, 28)

# Tải ảnh xe (đã resize)
car_image = pygame.image.load("car.jpg").convert_alpha()
car_image = pygame.transform.scale(car_image, (120, 60))

# Thông số xe
car_width, car_height = car_image.get_size()
road_y = HEIGHT - 60  # mặt đường
car_y = road_y - car_height

clock = pygame.time.Clock()
FPS = 60

# Vị trí ban đầu
START_X = WIDTH // 6

# === Nhập thời gian từ người dùng ===
t0 = float(input("Nhập thời gian bắt đầu t0 (giây): "))
T = float(input("Nhập thời gian kết thúc T (giây): "))

# Tính toán trước
x_t0 = -4 * t0 + 2 * t0**2
x_T = -4 * T + 2 * T**2

displacement_total = x_T - x_t0
distance_total = abs(displacement_total)
dt_total = T - t0

avg_velocity = displacement_total / dt_total if dt_total > 0 else 0
avg_speed = distance_total / dt_total if dt_total > 0 else 0

print("\n--- Kết quả tính toán ---")
print(f"Độ dời Δx từ t0={t0:.2f}s đến T={T:.2f}s: {displacement_total:.2f} m")
print(f"Vận tốc trung bình: {avg_velocity:.2f} m/s")
print(f"Tốc độ trung bình: {avg_speed:.2f} m/s")
print("---------------------------\n")

# --- Trạng thái mô phỏng ---
time_elapsed = t0  # chạy từ t0
car_x = START_X + x_t0 * PIXELS_PER_METER
velocity = -4 + 4 * t0
acceleration = 4
displacement = 0.0
distance_traveled = 0.0
last_x_m = x_t0

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
    pygame.draw.line(screen, GRAY, (0, road_y), (WIDTH, road_y), 3)

    # Vector vật lý
    draw_arrow(screen, car_x + car_width // 2, car_y + car_height + 20, velocity, BLUE, 'v (m/s)')
    draw_arrow(screen, car_x + car_width // 2, car_y + car_height + 40, acceleration, GREEN, 'a (m/s²)')

    # Thông tin
    info_y = road_y + 10
    s_text = font.render(f"Δx: {displacement:.2f} m", True, BLACK)
    s_real_text = font.render(f"Quãng đường s: {distance_traveled:.2f} m", True, BLACK)
    v_text = font.render(f"v: {velocity:.2f} m/s", True, BLACK)
    a_text = font.render(f"a: {acceleration:.2f} m/s²", True, BLACK)
    t_text = font.render(f"t: {time_elapsed:.2f} s", True, BLACK)
    avg_text = font.render(f"v_tb: {avg_velocity:.2f} m/s | tốc độ tb: {avg_speed:.2f} m/s", True, RED)

    screen.blit(s_text, (30, info_y))
    screen.blit(s_real_text, (250, info_y))
    screen.blit(v_text, (500, info_y))
    screen.blit(a_text, (650, info_y))
    screen.blit(t_text, (800, info_y))
    screen.blit(avg_text, (30, info_y + 30))

# === Vòng lặp chính ===
running = True
while running:
    dt = clock.tick(FPS) / 1000
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Animation xe chạy
    if time_elapsed <= T:
        time_elapsed += dt
        x_m = -4 * time_elapsed + 2 * (time_elapsed ** 2)

        displacement = x_m - x_t0
        distance_traveled += abs(x_m - last_x_m)
        last_x_m = x_m

        car_x = START_X + x_m * PIXELS_PER_METER

        velocity = -4 + 4 * time_elapsed
        acceleration = 4
    else:
        velocity = 0  # xe dừng
        acceleration = 0

    # Vẽ xe (có bóng cho đẹp)
    pygame.draw.ellipse(screen, GRAY, (car_x + 10, car_y + car_height - 10, car_width - 20, 15))
    screen.blit(car_image, (car_x, car_y))

    draw_ui()
    pygame.display.flip()

pygame.quit()
sys.exit()
