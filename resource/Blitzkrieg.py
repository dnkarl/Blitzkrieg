import os, sys, pygame, random, math, time, subprocess, heapq

pygame.init()
RESOURCE_PATH = os.path.join(sys._MEIPASS) if getattr(sys, '_MEIPASS', False) else os.path.dirname(os.path.abspath(__file__))
def resource_path(filename): return os.path.join(RESOURCE_PATH, filename)

def open_readme():
    readme_path = resource_path("README.txt")
    try:
        if sys.platform == "win32":
            os.startfile(readme_path)
        elif sys.platform == "darwin":
            subprocess.call(["open", readme_path])
        else:
            subprocess.call(["xdg-open", readme_path])
    except Exception as e:
        print(f"Error opening README.txt: {e}")

# SIZE
WIDTH, HEIGHT, CELL_SIZE = 1280, 720, 80
COLS, ROWS = WIDTH // CELL_SIZE, HEIGHT // CELL_SIZE
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# FONT
font = pygame.font.Font(None, 45)
small_font = pygame.font.Font(None, 30)
viet_font = pygame.font.Font(resource_path("font_ForcedSquare.ttf"), 50)
pixel_font = pygame.font.Font(resource_path("font_upheavtt.ttf"), 80)
tutorial_font = pygame.font.Font(resource_path("font_dejavu.ttf"), 30)
battle_font = pygame.font.Font(resource_path("font_battleground.ttf"), 40)
small_battle_font = pygame.font.Font(resource_path("font_battleground.ttf"), 32)

# RESOURCE
left_logo = pygame.transform.smoothscale(pygame.image.load(resource_path("logo-left-tank.png")).convert_alpha(), (319, 227))
right_logo = pygame.transform.smoothscale(pygame.image.load(resource_path("logo-right-tank.png")).convert_alpha(), (396, 366))
background = pygame.image.load(resource_path("background.png")).convert()
background_maze = pygame.image.load(resource_path("background_maze.png")).convert()
background_maze_pve = pygame.image.load(resource_path("background_maze_pve.png")).convert()
pygame.display.set_caption("Blitzkrieg")
icon = pygame.image.load(resource_path("icon.png"))
pygame.display.set_icon(icon)
laser_icon = pygame.transform.smoothscale(pygame.image.load(resource_path("laser_icon.png")).convert_alpha(), (20, 20))
shield_icon = pygame.transform.smoothscale(pygame.image.load(resource_path("shield_icon.png")).convert_alpha(), (40, 40))
mine_icon = pygame.transform.smoothscale(pygame.image.load(resource_path("mine_icon.png")).convert_alpha(), (20, 20))
smaller_icon = pygame.transform.smoothscale(pygame.image.load(resource_path("smaller_icon.png")).convert_alpha(), (20, 20))  # Icon mới cho Smaller

# COLOR
WHITE, BLACK, GRAY = (255, 255, 255), (0, 0, 0), (150, 150, 150)

# MUSIC
pygame.mixer.init()
music = pygame.mixer.music.load(resource_path("background_music.mp3"))
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.5)
click_sound = pygame.mixer.Sound(resource_path("click.wav"))
click_sound.set_volume(0.8)
explosion_sound = pygame.mixer.Sound(resource_path("explosion.mp3"))
explosion_sound.set_volume(0.8)

# BUTTON
class Button:
    def __init__(self, text, x, y, w, h, font=font, color=GRAY, hover_color=(200, 200, 200)):
        self.text, self.rect = text, pygame.Rect(x, y, w, h)
        self.font = font
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False

    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        current_color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surface, current_color, self.rect, border_radius=10)
        text_surface = self.font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        if self.rect.collidepoint(pos):
            click_sound.play()
            return True
        return False

buttons = [Button(txt, 490, y, 300, 70, font, (255, 100, 100), (255, 150, 150)) for txt, y in [("Play Game", 250), ("Tutorial", 360), ("Settings", 470), ("Credits", 580)]]
back_button = Button("Back", 10, HEIGHT - 60, 150, 50, font, (255, 100, 100), (255, 150, 150))
main_menu_button = Button("Main Menu", WIDTH - 170, 12, 160, 50, small_font, (255, 100, 100), (255, 150, 150))
exit_button = Button("Exit", WIDTH - 160, 10, 150, 50, font, (255, 100, 100), (255, 150, 150))
pvp_button = Button("PvP", 490, 250, 300, 70, font, (100, 200, 100), (150, 255, 150))
pve_button = Button("PvE", 490, 360, 300, 70, font, (100, 150, 255), (150, 200, 255))
enter_button = Button("Enter", WIDTH - 160, HEIGHT - 60, 150, 50, font, (100, 200, 100), (150, 255, 150))
easy_button = Button("Easy", 490, 250, 300, 70, font, (100, 200, 100), (150, 255, 150))
medium_button = Button("Medium", 490, 360, 300, 70, font, (255, 200, 100), (255, 255, 150))
hard_button = Button("Hard", 490, 470, 300, 70, font, (255, 100, 100), (255, 150, 150))
settings_game_button = Button("Settings", 0, 0, 150, 50, small_font, (100, 150, 255), (150, 200, 255))
victory_main_menu_button = Button("Main Menu", WIDTH // 2 - 85, HEIGHT // 2 + 50, 200, 60, small_font, (100, 200, 100), (150, 255, 150))
readme_button = Button("README", WIDTH // 2 - 180, HEIGHT // 2 + 285, 170, 60, small_font, (100, 150, 255), (150, 200, 255))
update_history_button = Button("Update History", WIDTH // 2, HEIGHT // 2 + 285, 220, 60, font=small_font)

# CHECK BOX / TICK BOX
class Checkbox:
    def __init__(self, x, y, label):
        self.checkbox_rect = pygame.Rect(x, y, 25, 25)
        self.checked = False
        self.label = label
        label_surface = battle_font.render(self.label, True, WHITE)
        label_width = label_surface.get_width()
        label_height = label_surface.get_height()
        self.rect = pygame.Rect(x, y, 25 + 30 + label_width, max(25, label_height))

    def draw(self, surface):
        pygame.draw.rect(surface, WHITE, self.checkbox_rect, 2)
        if self.checked:
            pygame.draw.line(surface, WHITE, (self.checkbox_rect.x + 3, self.checkbox_rect.y + 3),
                             (self.checkbox_rect.x + 22, self.checkbox_rect.y + 22), 4)
            pygame.draw.line(surface, WHITE, (self.checkbox_rect.x + 22, self.checkbox_rect.y + 3),
                             (self.checkbox_rect.x + 3, self.checkbox_rect.y + 22), 4)
        label_surface = battle_font.render(self.label, True, WHITE)
        surface.blit(label_surface, (self.checkbox_rect.x + 35, self.checkbox_rect.y + 5))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.checked = not self.checked
bullet_limit_inf_checkbox = Checkbox(960, 530, "inf")
bullet_lifetime_inf_checkbox = Checkbox(960, 610, "inf")
time_inf_checkbox = Checkbox(820, 460, "inf")

# SLIDER
class Slider:
    def __init__(self, x, y, w, h, min_value, max_value, default_value, is_percentage=False, has_infinity_option=False, infinity_checkbox=None):
        self.rect = pygame.Rect(x, y, w, h)
        knob_width = 10
        self.min_value = min_value
        self.max_value = max_value
        self.is_percentage = is_percentage
        self.has_infinity_option = has_infinity_option
        self.infinity_checkbox = infinity_checkbox
        value_range = max_value - min_value
        default_ratio = (default_value - min_value) / value_range
        knob_x = x + round(default_ratio * (w - knob_width))
        self.knob = pygame.Rect(knob_x, y - 5, knob_width, h + 10)
        self.dragging = False
        self.font = pygame.font.Font(None, 25)

    def draw(self, surface):
        pygame.draw.rect(surface, GRAY, self.rect)
        pygame.draw.rect(surface, WHITE, self.knob)
        if self.has_infinity_option and self.infinity_checkbox.checked:
            display_text = "inf"
        else:
            current_value = self.get_value()
            if self.is_percentage:
                display_text = f"{int(current_value * 100)}%"
            else:
                if self.min_value == 0.28 and self.max_value == 2.0:
                    display_text = f"{current_value:.2f}"
                else:
                    display_text = f"{int(round(current_value))}"
        text_surface = self.font.render(display_text, True, WHITE)
        text_rect = text_surface.get_rect(center=(self.knob.centerx, self.knob.y - 10))
        surface.blit(text_surface, text_rect)

    def set_knob_pos(self, x):
        self.knob.x = max(self.rect.x, min(x, self.rect.x + self.rect.width - self.knob.width))

    def get_value(self):
        ratio = (self.knob.x - self.rect.x) / (self.rect.width - self.knob.width)
        return self.min_value + ratio * (self.max_value - self.min_value)

music_slider = Slider(450, 130, 480, 20, 0.0, 1.0, 0.5, is_percentage=True)
sound_slider = Slider(450, 210, 480, 20, 0.0, 1.0, 0.8, is_percentage=True)
tank_speed_slider = Slider(450, 290, 480, 20, 50, 500, 200)
bullet_speed_slider = Slider(450, 370, 480, 20, 50, 600, 300)
reload_speed_slider = Slider(450, 450, 480, 20, 0.28, 2.0, 0.5)
bullet_limit_slider = Slider(450, 530, 480, 20, 5, 20, 10, has_infinity_option=True, infinity_checkbox=bullet_limit_inf_checkbox)
bullet_lifetime_slider = Slider(450, 610, 480, 20, 2, 30, 10, has_infinity_option=True, infinity_checkbox=bullet_lifetime_inf_checkbox)

# SHADOW TEXT
def draw_text_with_shadow(surface, text, font, color, shadow_color, x, y):
    shadow_surface = font.render(text, True, shadow_color)
    text_surface = font.render(text, True, color)
    surface.blit(shadow_surface, (x + 3, y + 3))
    surface.blit(text_surface, (x, y))

# TIME
def format_time(milliseconds):
    seconds = milliseconds // 1000
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return f"Playtime: {hours:02d}:{minutes:02d}:{seconds:02d}"

# TUTORIAL
tutorial_text = (
"   Đây là trò chơi sinh tồn, thắng bại tại kĩ năng, hai anh em ngồi trên hai xe tank khác nhau và bắn ra những cục kẹo (đồng). Ai ăn trúng kẹo (đồng) sẽ thua. Bản đồ sẽ được tạo ra liên tục để tăng tính thú vị cho trò chơi.\n"
"   Bước 1: Nhấn \"Play Game\"\n"
"   Bước 2: Chọn chế độ\n"
" - Ở chế độ PvP\n"
"   P1: W-Lên, A-Trái, S-Xuống, D-Phải, R-Bắn\n"
"   P2: UP-Lên, LEFT-Trái, DOWN-Xuống, RIGHT-Phải, \\-Bắn\n"
" - Ở chế độ PvE: Người chơi sẽ đấu với AI\n"
"   Có 3 độ khó, mỗi độ khó thể hiện trình độ \"máy trí\" khác nhau\n"
"   Các nút di chuyển và bắn tương tự P1 của chế độ PvP\n"
"   Bước 3: Nhập tên và thời gian chơi (đơn vị giây)\n"
"   Bước 4: Cùng thưởng thức xem tình anh em có bền được lâu?\n"
"   Và trong game có một tính năng đặc biệt khi bắn súng. Lưu ý: đây là tính năng và không phải \"bọ\"\n"
"   Vì đây là phiên bản beta, vui lòng liên hệ cho chúng tôi khi bạn phát hiện ra những \"em bọ\" bay vào trò chơi này. Xin cảm ơn!\n"
" _Version: Beta 3.0.3_"
)

# Textbox cho Tutorial và Update History
class TextBox:
    def __init__(self, x, y, w, h, text, font):
        self.rect = pygame.Rect(x, y, w, h)
        self.font = font
        self.scroll_y = 0
        self.line_height = self.font.get_height() + 2
        self.text_lines = []
        max_width = w - 10
        for paragraph in text.split('\n'):
            words = paragraph.split(' ')
            current_line = ""
            for word in words:
                test_line = current_line + word + " "
                if self.font.size(test_line)[0] <= max_width:
                    current_line = test_line
                else:
                    if current_line:
                        self.text_lines.append(current_line.strip())
                    current_line = word + " "
            if current_line:
                self.text_lines.append(current_line.strip())
        total_text_height = len(self.text_lines) * self.line_height
        self.max_scroll = max(0, total_text_height - h)
        self.scrollbar_dragging = False
        self.content_dragging = False
        self.last_y = 0
        self.scrollbar_width = 10

    def draw(self, surface):
        background = pygame.Surface((self.rect.width, self.rect.height))
        background.set_alpha(75)
        surface.blit(background, (self.rect.x, self.rect.y))
        pygame.draw.rect(surface, GRAY, self.rect, 2)
        visible_height = self.rect.height
        start_line = max(0, int(self.scroll_y / self.line_height))
        end_line = min(len(self.text_lines), start_line + int(visible_height / self.line_height) + 1)

        for i in range(start_line, end_line):
            line_y = self.rect.y + (i * self.line_height) - self.scroll_y
            if line_y >= self.rect.y and line_y + self.line_height <= self.rect.y + self.rect.height:
                surface.blit(self.font.render(self.text_lines[i], True, WHITE), (self.rect.x + 5, line_y))

        if self.max_scroll > 0:
            scrollbar_x = self.rect.right - self.scrollbar_width - 2
            scrollbar_height = self.rect.height * (self.rect.height / (self.max_scroll + self.rect.height))
            scrollbar_y = self.rect.y + (self.scroll_y / self.max_scroll) * (self.rect.height - scrollbar_height)
            self.scrollbar_rect = pygame.Rect(scrollbar_x, scrollbar_y, self.scrollbar_width, scrollbar_height)
            pygame.draw.rect(surface, (150, 150, 150), self.scrollbar_rect)

    def scroll(self, dy):
        self.scroll_y = max(0, min(self.scroll_y + dy, self.max_scroll))

    def handle_event(self, event):
        if self.max_scroll > 0:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.scrollbar_rect.collidepoint(event.pos):
                    self.scrollbar_dragging = True
                elif self.rect.collidepoint(event.pos):
                    self.content_dragging = True
                    self.last_y = event.pos[1]
            elif event.type == pygame.MOUSEBUTTONUP:
                self.scrollbar_dragging = False
                self.content_dragging = False
            elif event.type == pygame.MOUSEMOTION:
                if self.scrollbar_dragging:
                    dy = event.rel[1]
                    scroll_factor = self.max_scroll / (self.rect.height - self.scrollbar_rect.height)
                    self.scroll_y = max(0, min(self.scroll_y + dy * scroll_factor * 1.5, self.max_scroll))
                elif self.content_dragging:
                    current_y = event.pos[1]
                    dy = self.last_y - current_y
                    self.scroll_y = max(0, min(self.scroll_y + dy * 1.5, self.max_scroll))
                    self.last_y = current_y

# INPUT BOX
class InputBox:
    def __init__(self, x, y, w, h, next_box=None):
        click_sound.play()
        self.rect = pygame.Rect(x, y, w, h)
        self.text = ""
        self.active = False
        self.next_box = next_box
        self.scroll_x = 0
        self.font = font
        self.scrollbar_height = 8
        self.dragging_scrollbar = False

    def draw(self, surface):
        pygame.draw.rect(surface, WHITE if self.active else GRAY, self.rect, 2)
        text_surface = self.font.render(self.text, True, WHITE)
        text_width = text_surface.get_width()
        max_width = self.rect.width - 10

        if text_width > max_width:
            visible_surface = pygame.Surface((max_width, self.rect.height - self.scrollbar_height - 2), pygame.SRCALPHA)
            visible_surface.blit(text_surface, (-self.scroll_x, 0))
            surface.blit(visible_surface, (self.rect.x + 5, self.rect.y + 5))
            
            scrollbar_width = max(20, max_width * (max_width / text_width))
            scrollbar_x = self.rect.x + 5 + (self.scroll_x / max(1, text_width - max_width)) * (max_width - scrollbar_width)
            scrollbar_rect = pygame.Rect(scrollbar_x, self.rect.y + self.rect.height - self.scrollbar_height - 2, scrollbar_width, self.scrollbar_height)
            pygame.draw.rect(surface, WHITE if self.dragging_scrollbar else GRAY, scrollbar_rect)
            self.scrollbar_rect = scrollbar_rect
        else:
            surface.blit(text_surface, (self.rect.x + 5, self.rect.y + 5))
            self.scroll_x = 0

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = True
                text_width = self.font.size(self.text)[0]
                if text_width > self.rect.width - 10 and hasattr(self, 'scrollbar_rect') and self.scrollbar_rect.collidepoint(event.pos):
                    self.dragging_scrollbar = True
            else:
                self.active = False
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging_scrollbar = False
        elif event.type == pygame.MOUSEMOTION and self.dragging_scrollbar:
            text_width = self.font.size(self.text)[0]
            max_width = self.rect.width - 10
            max_scroll = max(0, text_width - max_width)
            scroll_factor = max_scroll / (max_width - self.scrollbar_rect.width)
            dx = event.rel[0] * scroll_factor
            self.scroll_x = max(0, min(self.scroll_x + dx, max_scroll))
        elif event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key == pygame.K_RETURN:
                if self.next_box:
                    self.active = False
                    self.next_box.active = True
            else:
                self.text += event.unicode
                text_width = self.font.size(self.text)[0]
                max_width = self.rect.width - 10
                if text_width > max_width:
                    self.scroll_x = text_width - max_width
        elif event.type == pygame.MOUSEWHEEL and self.rect.collidepoint(pygame.mouse.get_pos()):
            text_width = self.font.size(self.text)[0]
            max_width = self.rect.width - 10
            if text_width > max_width:
                self.scroll_x = max(0, min(self.scroll_x - event.y * 20, text_width - max_width))
player1_input = InputBox(600, 250, 200, 44)
player2_input = InputBox(600, 350, 200, 44)
player_input = InputBox(600, 330, 200, 44)
time_input = InputBox(600, 450, 200, 44)
player1_input.next_box = player2_input
player2_input.next_box = time_input
player_input.next_box = time_input

# TANK AND BULLET
player1_image = pygame.transform.smoothscale(pygame.image.load(resource_path("tank1.png")).convert_alpha(), (25, 35))
player2_image = pygame.transform.smoothscale(pygame.image.load(resource_path("tank2.png")).convert_alpha(), (25, 35))
player1_image = pygame.transform.rotate(player1_image, 90)
player2_image = pygame.transform.rotate(player2_image, 90)

class Bullet:
    def __init__(self, x, y, angle):
        self.pos = pygame.Vector2(x, y)
        self.vel = pygame.Vector2(bullet_speed * math.cos(math.radians(angle)), bullet_speed * math.sin(math.radians(angle)))
        self.spawn_time = time.time()

    def update(self, dt, maze_lines):
        global rect
        new_pos = self.pos + self.vel * dt
        bullet_rect = pygame.Rect(new_pos.x - 4, new_pos.y - 4, 8, 8)

        for (x1, y1), (x2, y2) in maze_lines:
            if x1 == x2:
                wall_rect = pygame.Rect(x1 - 2.5, min(y1, y2), 5, abs(y1 - y2))
            else:
                wall_rect = pygame.Rect(min(x1, x2), y1 - 2.5, abs(x1 - x2), 5)

            if bullet_rect.colliderect(wall_rect):
                if x1 == x2:
                    if self.vel.x > 0:
                        new_pos.x = wall_rect.left - 4
                    else:
                        new_pos.x = wall_rect.right + 4
                    self.vel.x *= -1
                else:
                    if self.vel.y > 0:
                        new_pos.y = wall_rect.top - 4
                    else:
                        new_pos.y = wall_rect.bottom + 4
                    self.vel.y *= -1
                break

        if new_pos.x < rect.left + 4:
            new_pos.x = rect.left + 4
            self.vel.x *= -1
        elif new_pos.x > rect.right - 4:
            new_pos.x = rect.right - 4
            self.vel.x *= -1
        if new_pos.y < rect.top + 4:
            new_pos.y = rect.top + 4
            self.vel.y *= -1
        elif new_pos.y > rect.bottom - 4:
            new_pos.y = rect.bottom - 4
            self.vel.y *= -1

        self.pos = new_pos

    def draw(self):
        bullet_radius = 4
        bullet_surface = pygame.Surface((bullet_radius * 2, bullet_radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(bullet_surface, WHITE, (bullet_radius, bullet_radius), bullet_radius)
        screen.blit(bullet_surface, (int(self.pos.x - bullet_radius), int(self.pos.y - bullet_radius)))

class SmokeParticle:
    def __init__(self, x, y, angle):
        self.pos = pygame.Vector2(x, y)
        self.vel = pygame.Vector2(-math.cos(math.radians(angle)) * random.uniform(20, 50),
                                 -math.sin(math.radians(angle)) * random.uniform(20, 50))
        self.radius = random.randint(6, 11)
        self.life = random.uniform(0.6, 1.1)
        self.alpha = 255

    def update(self, dt):
        self.pos += self.vel * dt
        self.life -= dt
        self.radius = max(1, self.radius - dt * 4)
        self.alpha = max(0, self.alpha - dt * 255 / self.life)
        return self.life > 0

    def draw(self, surface):
        smoke_surface = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(smoke_surface, (150, 150, 150, int(self.alpha)), (self.radius, self.radius), self.radius)
        surface.blit(smoke_surface, (int(self.pos.x - self.radius), int(self.pos.y - self.radius)))

class Explosion:
    def __init__(self, x, y):
        self.pos = pygame.Vector2(x, y)
        self.start_time = time.time()
        self.duration = 1.8
        self.particles = []
        for _ in range(40):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(50, 150)
            self.particles.append({
                'pos': pygame.Vector2(x, y),
                'vel': pygame.Vector2(speed * math.cos(angle), speed * math.sin(angle)),
                'radius': random.randint(3, 12),
                'life': random.uniform(0.3, 0.5)
            })

    def update(self, dt):
        elapsed = time.time() - self.start_time
        for particle in self.particles[:]:
            particle['pos'] += particle['vel'] * dt
            particle['life'] -= dt
            particle['radius'] = max(1, particle['radius'] - dt * 10)
            if particle['life'] <= 0:
                self.particles.remove(particle)
        return elapsed < self.duration

    def draw(self, surface):
        for particle in self.particles:
            pygame.draw.circle(surface, (255, 100, 100), (int(particle['pos'].x), int(particle['pos'].y)), int(particle['radius']))

class Buff:
    def __init__(self, x, y):
        self.image = pygame.transform.smoothscale(pygame.image.load(resource_path("buff.png")).convert_alpha(), (18, 18))
        self.rect = self.image.get_rect(center=(x, y))

class Mine:
    def __init__(self, x, y):
        self.pos = pygame.Vector2(x, y)
        self.visible = True
        self.timer = 2.0  # 2 giây trước khi tàng hình
        self.rect = pygame.Rect(x - 15, y - 15, 30, 30)  # Tăng kích thước từ 20x20 thành 30x30
        self.image = pygame.transform.smoothscale(pygame.image.load(resource_path("mine.png")).convert_alpha(), (30, 30))  # Tăng kích thước hình ảnh

    def update(self, dt):
        if self.visible:
            self.timer -= dt
            if self.timer <= 0:
                self.visible = False

    def draw(self, surface):
        if self.visible:
            surface.blit(self.image, self.rect)

# Hàm kiểm tra va chạm với tia laser dày
def check_laser_collision(tank_rect, laser_start, laser_end, laser_width):
    dir_vec = laser_end - laser_start
    length = dir_vec.length()
    if length == 0:
        return False
    dir_vec /= length
    perp_vec = pygame.Vector2(-dir_vec.y, dir_vec.x)
    offset = perp_vec * (laser_width / 2)
    lines = [
        (laser_start - offset, laser_end - offset),
        (laser_start, laser_end),
        (laser_start + offset, laser_end + offset)
    ]
    for line in lines:
        if tank_rect.clipline(line):
            return True
    return False

# MAIN SCREEN
show_credits = show_game = show_settings = show_mode_select = show_pvp \
= show_pve = show_difficulty = show_victory = show_tutorial = show_update_history = False
exit_to_victory = False
maze_lines, rect = [], pygame.Rect(0, 0, 0, 0)
player1_name, player2_name = "", ""
error_message = ""
player1_pos, player2_pos = pygame.Vector2(0, 0), pygame.Vector2(0, 0)
game_mode = "PvP"
opened_from_game = False
is_paused = False
paused_time = 0
actual_playtime = 0
last_update_time = 0
maze_surface, final_game_surface, tutorial_text_box, update_history_box = None, None, None, None
angle1, angle2 = 0, 0
player1_bullets, player2_bullets = [], []
last_shot_time_p1, last_shot_time_p2 = 0, 0
original_tank_size = 20  # Kích thước gốc của tank
smaller_tank_size = original_tank_size / 2  # Kích thước khi thu nhỏ
speed, bullet_speed, reload_speed, bullet_limit, bullet_lifetime = 200, 300, 0.5, 10, 10
player1_score, player2_score = 0, 0
game_time_seconds = 0
game_start_time = 0
player1_smoke_particles = player2_smoke_particles = []
smoke_spawn_rate = 0.05
last_smoke_time_p1 = last_smoke_time_p2 = 0
explosion = explosion2 = None
slow_motion = False
slow_motion_start = 0
slow_motion_duration = 2
slow_motion_paused_time = 0
shake_offset = pygame.Vector2(0, 0)
overlay_alpha = 0
bot_difficulty = "Easy"
bot_stuck_time = bot_last_shot = bot_target_angle = 0
bot_position_history = []
bot_history_limit = 50
buffs = []
level_start_time = 0
next_buff_spawn_time = 0
player1_skill = None
player1_skill_active = False
player1_skill_timer = 0.0
player1_laser_angle = 0.0
player1_smaller_timer = 0.0  # Timer cho skill Smaller của Player 1
player2_skill = None
player2_skill_active = False
player2_skill_timer = 0.0
player2_laser_angle = 0.0
player2_smaller_timer = 0.0  # Timer cho skill Smaller của Player 2
active_mines = []

# MAZE - DFS - RANDOM DELETE WALL
def generate_maze():
    global maze_surface, level_start_time, next_buff_spawn_time, buffs, player1_skill, player1_skill_active, player2_skill, player2_skill_active, active_mines, player1_smaller_timer, player2_smaller_timer
    cols, rows = ((WIDTH - 100) // (CELL_SIZE // 2)), ((HEIGHT + 50) // (CELL_SIZE // 2))
    maze = [[1] * cols for _ in range(rows)]
    stack = [(1, 1)]
    maze[1][1] = 0
    directions = [(0, -2), (0, 2), (-2, 0), (2, 0)]

    while stack:
        x, y = stack[-1]
        random.shuffle(directions)
        found = False
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 < nx < rows - 1 and 0 < ny < cols - 1 and maze[nx][ny] == 1:
                maze[nx][ny] = 0
                maze[x + dx // 2][y + dy // 2] = 0
                stack.append((nx, ny))
                found = True
                if random.random() < 0.3: break
        if not found: stack.pop()

    for _ in range((cols * rows) // 4):
        rx, ry = random.randint(1, rows - 2), random.randint(1, cols - 2)
        if maze[rx][ry] == 1: maze[rx][ry] = 0

    maze_lines = []
    for r in range(rows):
        for c in range(cols):
            x, y = c * (CELL_SIZE // 2), r * (CELL_SIZE // 2)
            if maze[r][c] == 1:
                if r + 1 < rows and maze[r + 1][c] == 1:
                    maze_lines.append(((x, y), (x, y + (CELL_SIZE // 2))))
                if c + 1 < cols and maze[r][c + 1] == 1:
                    maze_lines.append(((x, y), (x + (CELL_SIZE // 2), y)))
    rect = pygame.Rect(0, 0, cols * (CELL_SIZE // 2), HEIGHT)
    
    while True:
        x1 = random.randint(rect.left + 20 + original_tank_size // 2, rect.left + rect.width // 2)
        y1 = random.randint(rect.top + 20 + original_tank_size // 2, rect.top + rect.height // 2)
        if not any(pygame.Rect(x1 - original_tank_size // 2, y1 - original_tank_size // 2, original_tank_size, original_tank_size).clipline((x1_, y1_), (x2_, y2_)) for (x1_, y1_), (x2_, y2_) in maze_lines):
            player1_pos.update(x1, y1)
            break

    while True:
        x2 = random.randint(rect.right - rect.width // 2, rect.right - 20 - original_tank_size // 2)
        y2 = random.randint(rect.bottom - rect.height // 2, rect.bottom - 20 - original_tank_size // 2)
        if not any(pygame.Rect(x2 - original_tank_size // 2, y2 - original_tank_size // 2, original_tank_size, original_tank_size).clipline((x1_, y1_), (x2_, y2_)) for (x1_, y1_), (x2_, y2_) in maze_lines):
            player2_pos.update(x2, y2)
            break
    
    maze_surface = pygame.Surface((WIDTH, HEIGHT))
    if game_mode == "PvE":
        maze_surface.blit(background_maze_pve, (0, 0))
    else:
        maze_surface.blit(background_maze, (0, 0))
    for (x1, y1), (x2, y2) in maze_lines:
        pygame.draw.line(maze_surface, WHITE, (x1, y1), (x2, y2), 6)
    
    level_start_time = time.time()
    next_buff_spawn_time = level_start_time + 5
    buffs = []
    player1_skill = None
    player1_skill_active = False
    player1_smaller_timer = 0.0  # Reset timer khi tạo map mới
    player2_skill = None
    player2_skill_active = False
    player2_smaller_timer = 0.0  # Reset timer khi tạo map mới
    active_mines = []
    return maze_lines, rect

def check_collision(pos, maze_lines, tank_size_to_use):
    tank_rect = pygame.Rect(pos.x - tank_size_to_use // 2, pos.y - tank_size_to_use // 2, tank_size_to_use, tank_size_to_use)
    return any(tank_rect.clipline((x1, y1), (x2, y2)) for (x1, y1), (x2, y2) in maze_lines)

def draw_tank(position, angle, image, smaller_timer):
    if smaller_timer > 0:
        scaled_image = pygame.transform.smoothscale(image, (int(25 / 2), int(35 / 2)))
    else:
        scaled_image = image
    rotated_image = pygame.transform.rotate(scaled_image, -angle)
    image_rect = rotated_image.get_rect(center=position)
    screen.blit(rotated_image, image_rect)

def find_laser_endpoint(tank_pos, angle, maze_lines, rect):
    direction = pygame.Vector2(math.cos(math.radians(angle)), math.sin(math.radians(angle)))
    min_t = float('inf')
    endpoint = None

    if direction.x != 0:
        t_left = (rect.left - tank_pos.x) / direction.x
        if t_left > 0:
            y_left = tank_pos.y + t_left * direction.y
            if rect.top <= y_left <= rect.bottom and t_left < min_t:
                min_t = t_left
                endpoint = pygame.Vector2(rect.left, y_left)
        t_right = (rect.right - tank_pos.x) / direction.x
        if t_right > 0:
            y_right = tank_pos.y + t_right * direction.y
            if rect.top <= y_right <= rect.bottom and t_right < min_t:
                min_t = t_right
                endpoint = pygame.Vector2(rect.right, y_right)
    if direction.y != 0:
        t_top = (rect.top - tank_pos.y) / direction.y
        if t_top > 0:
            x_top = tank_pos.x + t_top * direction.x
            if rect.left <= x_top <= rect.right and t_top < min_t:
                min_t = t_top
                endpoint = pygame.Vector2(x_top, rect.top)
        t_bottom = (rect.bottom - tank_pos.y) / direction.y
        if t_bottom > 0:
            x_bottom = tank_pos.x + t_bottom * direction.x
            if rect.left <= x_bottom <= rect.right and t_bottom < min_t:
                min_t = t_bottom
                endpoint = pygame.Vector2(x_bottom, rect.bottom)

    for (p1, p2) in maze_lines:
        if p1[0] == p2[0]:
            wx = p1[0]
            if direction.x != 0:
                t = (wx - tank_pos.x) / direction.x
                if t > 0:
                    y = tank_pos.y + t * direction.y
                    if min(p1[1], p2[1]) <= y <= max(p1[1], p2[1]) and t < min_t:
                        min_t = t
                        endpoint = pygame.Vector2(wx, y)
        elif p1[1] == p2[1]:
            wy = p1[1]
            if direction.y != 0:
                t = (wy - tank_pos.y) / direction.y
                if t > 0:
                    x = tank_pos.x + t * direction.x
                    if min(p1[0], p2[0]) <= x <= max(p1[0], p2[0]) and t < min_t:
                        min_t = t
                        endpoint = pygame.Vector2(x, wy)
    if endpoint is None:
        endpoint = tank_pos + direction * 10000
    return endpoint

update_history_text = (
    "**Beta 1.0.1**: (18/02/2025 - by dnkarlarl, tmh9)\n"
    "  - Tạo giao diện người dùng trắng, xám, đen.\n"
    "  - Chỉ có 1 map.\n"
    "  - Tank spawn tại hai vị trí góc phải trên cùng và góc trái dưới cùng.\n"
    "  - Đạn có thể bắn ra liên tục, không biến mất.\n"
    "  - Thêm Credits.\n\n"
    
    "**Beta 1.0.2**: (20/02/2025 - by dnkarl)\n"
    "  - Thêm Tutorial.\n"
    "  - Thêm Playtime.\n"
    "  - Thêm nhạc nền.\n"
    "  - Sửa lỗi nút ấn cố định, giờ đây khi ấn nút nào thì màn hình liên kết với nút đó mới xuất hiện.\n"
    "  - Sửa lỗi đạn bay xuyên một vài tường.\n"
    "  - Map giờ đây có thể random.\n\n"
    
    "**Beta 1.0.3**: (23/02/2025 - by dnkarl)\n"
    "  - Sửa lỗi đạn bay khỏi khung hình và không bật lại.\n"
    "  - Sửa độ dày của tường trong map.\n"
    "  - Thêm Settings.\n"
    "  - Thêm chỉnh âm lượng nhạc nền ở Music trong Settings.\n"
    "  - Thêm phần nhập tên người chơi.\n"
    "  - Thêm giới hạn đạn ( 10 ).\n"
    "  - Thêm giới hạn thời gian tồn tại của đạn ( 10s ).\n\n"
    
    "**Beta 1.0.4**: (25/02/2025 - by dnkarl)\n"
    "  - Sửa lỗi map không thông thoáng, khó đi.\n"
    "  - Sửa lỗi font và TextBox của Tutorial.\n"
    "  - Thêm 3 chế độ: Dễ, Vừa, Khó trong chế độ PvE (đấu với máy).\n"
    "  - Thêm chỉnh sửa tốc độ xe tank và tốc độ đạn bay (người chơi chỉnh sửa trong Settings).\n"
    "  - Thêm phần nhập thời gian chơi (đơn vị giây).\n"
    "  - Thêm bảng tỉ số.\n"
    "  - Thêm Time Left.\n"
    "  - Thêm nút Settings trong khi chơi.\n\n"
    
    "**Beta 2.0.1**: (27/02/2025 - by dnkarl)\n"
    "  - Sửa lỗi bảng tỉ số không vừa vặn, khó nhìn.\n"
    "  - Sửa lỗi văn bản trong Tutorial tràn màn hình.\n"
    "  - Nâng cấp giao diện người dùng.\n"
    "  - Thêm README.txt.\n"
    "  - Thêm hình nền ở màn hình chính và ở map khi chơi.\n"
    "  - Thêm màu cho các nút ấn.\n"
    "  - Đổi màu chữ.\n"
    "  - Thêm âm thanh click (người chơi có thể chỉnh âm lượng ở Sound Effect trong Settings).\n"
    "  - Thêm màn hình chiến thắng sau khi hết thời gian chơi.\n"
    "  - Thêm icon cho phần mềm .exe.\n\n"
    
    "**Beta 2.0.2**: (02/03/2025 - by dnkarl)\n"
    "  - Sửa lỗi Time Left không tạm dừng (Pause) khi nhấn Settings.\n"
    "  - Sửa lỗi không có nút ấn vẫn ấn được.\n"
    "  - Nâng cấp giao diện người dùng.\n"
    "  - Đổi nhạc nền.\n"
    "  - Làm mới màu sắc cho tank.\n"
    "  - Thêm Update History (Chi tiết các bản cập nhật).\n"
    "  - Thêm thanh cuộn văn bản cho Tutorial và Update History.\n\n"
    
    "**Beta 3.0.1**: (04-05/03/2025 - by dnkarl)\n"
    "  - Điều chỉnh nút bắn ở P1: R và ở P2: \\ .\n"
    "  - Sửa lỗi tên người chơi và thời gian đã nhập trước đó không xoá khi quay lại màn hình chính.\n"
    "  - Sửa lỗi không thể dùng thanh cuộn để cuộn. Giờ đây không cần chuột hay touchpad, người chơi có thể nhấn giữ thanh cuộn để cuộn văn bản.\n"
    "  - Sửa lỗi thời gian trong ô Time Left nếu quá dài sẽ bị tràn màn hình. Giờ đây đã được fit lại cho vừa màn hình.\n"
    "  - Nâng cấp giao diện người dùng mượt hơn.\n"
    "  - Nâng cấp giao diện Settings.\n"
    "  - Nâng cấp thanh cuộn giờ đây có thể scroll văn bản bằng màn hình cảm ứng.\n"
    "  - Nâng cấp map, mở rộng chiều rộng map.\n"
    "  - Hạn chế hai tank spawn gần nhau ở đầu game.\n"
    "  - Tên bây giờ có thể để trống.\n"
    "  - Khi đang chơi, màn hình sẽ tự động chuyển qua Pause nếu con trỏ chuột không nằm trên màn hình chơi.\n"
    "  - Giới hạn thời gian chơi tối đa là 1000000000s nếu người chơi không chọn inf (endless mode).\n"
    "  - Thêm background vào chế độ PvE.\n"
    "  - Thêm nút Main Menu trong Settings ở màn hình chơi.\n"
    "  - Thêm tính năng triệt tiêu đạn (hai đạn đụng nhau sẽ biến mất).\n"
    "  - Thêm hiệu ứng phát nổ, rung màn hình, nhấp nháy, làm chậm 2s khi xe tank trúng đạn.\n"
    "  - Thêm âm thanh nổ, có thể được điều chỉnh ở Sound Effect trong Settings.\n"
    "  - Thêm chỉnh sửa giới hạn đạn, thời gian reload đạn, thời gian tồn tại của đạn trên map (người chơi chỉnh sửa trong Settings).\n"
    "  - Thêm không giới hạn đạn và không giới hạn thời gian tồn tại của đạn.\n"
    "  - Thêm khi nhấn Esc ở trong trò chơi, màn hình PAUSE sẽ hiện lên, khi nhấn Esc ở những nơi khác sẽ quay lại màn hình trước.\n"
    "  - Thêm khi nhấn Enter ở ô nhập tên sẽ qua ô tiếp theo rồi qua màn hình chơi.\n\n"

    "**Beta 3.0.2**: (07-08/03/2025 - by dnkarl) \n"
    "  - Sửa lỗi button không hoạt động.\n"
    "  - Sửa lỗi cho phép hai tên trùng nhau.\n"
    "  - Sửa lỗi endless mode không hoạt động.\n"
    "  - Sửa lỗi hiệu ứng nhấp nháy, rung không hoạt động khi có xe tank bị nổ.\n"
    "  - Sửa lỗi phím Esc và Enter không hoạt động đúng.\n"
    "  - Nâng cấp đạn nhìn rõ hơn.\n"
    "  - Thêm tính năng sẵn sàng để nhập cho ô Time mà không cần click vào khi người chơi tới màn hình nhập Time.\n"
    "  - Thêm hiệu ứng khói khi xe tank di chuyển.\n"
    "  - Thêm tính năng hai xe tank đụng nhau sẽ nổ (hoà).\n"
    "  - (BETA) Thêm AI (Bot) cả 3 độ khó vào chế độ PvE (developed with python source code, currently in testing phase, by dnkarl).\n\n"

    "**Beta 3.0.3**: (20-21/03/2025 - by tmh9, huy, phanlam) -- **Latest version**\n"
    "  - Nâng cấp cơ chế di chuyển của tank mượt hơn.\n"
    "  - Thêm AI (Bot) vào chế độ PvE ở cả 3 độ khó.\n"
    "  - Thêm Buffs/ Debuffs (Gacha) xuất hiện ngẫu nhiên trong map.\n"
    "  - Thêm skill Laser Beam khi nhặt buff random trúng số 1.\n"
    "  - Thêm skill Shield khi nhặt buff random trúng số 2.\n"
    "  - Thêm skill Mine khi nhặt buff random trúng số 3.\n"
    "  - Thêm skill Smaller khi nhặt buff random trúng số 4.\n"
)

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_star(start, goal, maze_lines, rect):
    grid_size = CELL_SIZE // 2
    start = (int(start.x // grid_size), int(start.y // grid_size))
    goal = (int(goal.x // grid_size), int(goal.y // grid_size))
    cols, rows = rect.width // grid_size, rect.height // grid_size

    open_set = [(0, start)]
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}

    while open_set:
        current = heapq.heappop(open_set)[1]

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return path[::-1]

        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            neighbor = (current[0] + dx, current[1] + dy)
            if not (0 <= neighbor[0] < cols and 0 <= neighbor[1] < rows):
                continue

            neighbor_pos = pygame.Vector2(neighbor[0] * grid_size + grid_size // 2, neighbor[1] * grid_size + grid_size // 2)
            if any(pygame.Rect(neighbor_pos.x - original_tank_size // 2, neighbor_pos.y - original_tank_size // 2, original_tank_size, original_tank_size).clipline((x1, y1), (x2, y2)) for (x1, y1), (x2, y2) in maze_lines):
                continue

            tentative_g_score = g_score[current] + 1
            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return None

clock = pygame.time.Clock()
while True:
    dt = clock.tick(120) / 1000
    if not is_paused:
        current_time = pygame.time.get_ticks()
        if last_update_time != 0:
            actual_playtime += current_time - last_update_time
        last_update_time = current_time

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.ACTIVEEVENT:
            if event.gain == 0 and event.state == 1 and show_game:
                show_game = False
                show_settings = True
                opened_from_game = True
                is_paused = True
                paused_time = time.time() - game_start_time
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                click_sound.play()
                if show_game:
                    show_game = False
                    show_settings = True
                    opened_from_game = True
                    is_paused = True
                    paused_time = time.time() - game_start_time
                elif show_settings:
                    show_settings = False
                    if opened_from_game:
                        show_game = True
                        opened_from_game = False
                        is_paused = False
                        game_start_time = time.time() - paused_time
                        last_update_time = pygame.time.get_ticks()
                    player1_input.active = player2_input.active = player_input.active = time_input.active = False
                elif show_mode_select:
                    show_mode_select = False
                elif show_pvp:
                    show_pvp = False
                    show_mode_select = True
                    error_message = ""
                    player1_input.active = player2_input.active = time_input.active = False
                elif show_pve:
                    show_pve = False
                    show_mode_select = True
                    error_message = ""
                    player_input.active = time_input.active = False
                elif show_difficulty:
                    show_difficulty = False
                    show_pve = True
                    time_input.active = True
                elif show_victory:
                    show_victory = False
                    player1_score, player2_score = 0, 0
                    player1_bullets.clear()
                    player2_bullets.clear()
                elif show_tutorial:
                    show_tutorial = False
                    tutorial_text_box = None
                elif show_credits:
                    show_credits = False
                elif show_update_history:
                    show_update_history = False
                    show_credits = True
                    update_history_box = None
            elif event.key == pygame.K_RETURN:
                click_sound.play()
                if show_pvp:
                    player1_name_temp = player1_input.text if player1_input.text else "Player 1"
                    player2_name_temp = player2_input.text if player2_input.text else "Player 2"
        
                    if player1_name_temp == player2_name_temp:
                        error_message = "Player names cannot be the same!"
                    else:
                        if not time_inf_checkbox.checked:
                            if not time_input.text:
                                error_message = "Please enter the time in second(s)!"
                            else:
                                try:
                                    time_value = int(time_input.text)
                                    if time_value <= 0 or time_value > 1000000000:
                                        error_message = "Time must be a positive number <= 1000000000 (10^9)"
                                    else:
                                        game_time_seconds = time_value
                                        player1_name = player1_name_temp
                                        player2_name = player2_name_temp
                                        show_pvp = False
                                        show_game = True
                                        maze_lines, rect = generate_maze()
                                        game_start_time = time.time()
                                        error_message = ""
                                except ValueError:
                                    error_message = "Time must be a valid number!"
                        else:
                            game_time_seconds = float('inf')
                            player1_name = player1_name_temp
                            player2_name = player2_name_temp
                            show_pvp = False
                            show_game = True
                            maze_lines, rect = generate_maze()
                            game_start_time = time.time()
                            error_message = ""
                elif show_pve:
                    if not time_inf_checkbox.checked:
                        if not time_input.text:
                            error_message = "Please enter the time in second(s)!"
                        else:
                            try:
                                time_value = int(time_input.text)
                                if time_value <= 0 or time_value > 1000000000:
                                    error_message = "Time must be a positive number <= 1000000000 (10^9)"
                                else:
                                    game_time_seconds = time_value
                                    player1_name = player_input.text if player_input.text else "Player 1"
                                    player2_name = "Bot"
                                    show_pve = False
                                    show_difficulty = True
                                    error_message = ""
                            except ValueError:
                                error_message = "Time must be a valid number!"
                    else:
                        game_time_seconds = float('inf')
                        player1_name = player_input.text if player_input.text else "Player 1"
                        player2_name = "Bot"
                        show_pve = False
                        show_difficulty = True
                        error_message = ""

        if show_pvp:
            player1_input.handle_event(event)
            player2_input.handle_event(event)
            time_input.handle_event(event)
        if show_pve:
            player_input.handle_event(event)
            time_input.handle_event(event)

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            print(f"Click at position: {pos}")

            if show_pvp:
                if back_button.is_clicked(pos):
                    show_pvp = False
                    show_mode_select = True
                    error_message = ""
                    player1_input.active = player2_input.active = time_input.active = False
                elif enter_button.is_clicked(pos):
                    player1_name_temp = player1_input.text if player1_input.text else "Player 1"
                    player2_name_temp = player2_input.text if player2_input.text else "Player 2"

                    if player1_name_temp == player2_name_temp:
                        error_message = "Player names cannot be the same!"
                    else:
                        if not time_inf_checkbox.checked:
                            if not time_input.text:
                                error_message = "Please enter the time in second(s)!"
                            else:
                                try:
                                    time_value = int(time_input.text)
                                    if time_value <= 0 or time_value > 1000000000:
                                        error_message = "Time must be a positive number <= 1000000000 (10^9)"
                                    else:
                                        game_time_seconds = time_value
                                        player1_name = player1_name_temp
                                        player2_name = player2_name_temp
                                        show_pvp = False
                                        show_game = True
                                        maze_lines, rect = generate_maze()
                                        game_start_time = time.time()
                                    error_message = ""
                                except ValueError:
                                    error_message = "Time must be a valid number!"
                        else:
                            game_time_seconds = float('inf')
                            player1_name = player1_name_temp
                            player2_name = player2_name_temp
                            show_pvp = False
                            show_game = True
                            maze_lines, rect = generate_maze()
                            game_start_time = time.time()
                            error_message = ""
            elif show_pve:
                if back_button.is_clicked(pos):
                    show_pve = False
                    show_mode_select = True
                    error_message = ""
                    player_input.active = time_input.active = False
                elif enter_button.is_clicked(pos):
                    if not time_inf_checkbox.checked:
                        if not time_input.text:
                            error_message = "Please enter the time in second(s)!"
                        else:
                            try:
                                time_value = int(time_input.text)
                                if time_value <= 0 or time_value > 1000000000:
                                    error_message = "Time must be a positive number <= 1000000000 (10^9)"
                                else:
                                    game_time_seconds = time_value
                                    player1_name = player_input.text if player_input.text else "Player 1"
                                    player2_name = "Bot"
                                    show_pve = False
                                    show_difficulty = True
                                    error_message = ""
                            except ValueError:
                                error_message = "Time must be a valid number!"
                    else:
                        game_time_seconds = float('inf')
                        player1_name = player_input.text if player_input.text else "Player 1"
                        player2_name = "Bot"
                        show_pve = False
                        show_difficulty = True
                        error_message = ""

            elif show_mode_select:
                if back_button.is_clicked(pos):
                    show_mode_select = False
                elif pvp_button.is_clicked(pos):
                    player1_input.active = player2_input.active = player_input.active = time_input.active = False
                    show_mode_select = False
                    show_pvp = True
                    game_mode = "PvP"
                    time_input.active = True
                elif pve_button.is_clicked(pos):
                    player1_input.active = player2_input.active = player_input.active = time_input.active = False
                    show_mode_select = False
                    show_pve = True
                    game_mode = "PvE"
                    time_input.active = True
            elif show_difficulty:
                if back_button.is_clicked(pos):
                    show_difficulty = False
                    show_pve = True
                    time_input.active = True
                elif easy_button.is_clicked(pos):
                    show_difficulty = False
                    bot_difficulty = "Easy"
                    show_game = True
                    maze_lines, rect = generate_maze()
                    game_start_time = time.time()
                elif medium_button.is_clicked(pos):
                    show_difficulty = False
                    bot_difficulty = "Medium"
                    show_game = True
                    maze_lines, rect = generate_maze()
                    game_start_time = time.time()
                elif hard_button.is_clicked(pos):
                    show_difficulty = False
                    bot_difficulty = "Hard"
                    show_game = True
                    maze_lines, rect = generate_maze()
                    game_start_time = time.time()
            elif show_settings:
                bullet_limit_inf_checkbox.handle_event(event)
                bullet_lifetime_inf_checkbox.handle_event(event)
                if music_slider.knob.collidepoint(event.pos): music_slider.dragging = True
                if sound_slider.knob.collidepoint(event.pos): sound_slider.dragging = True
                if tank_speed_slider.knob.collidepoint(event.pos): tank_speed_slider.dragging = True
                if bullet_speed_slider.knob.collidepoint(event.pos): bullet_speed_slider.dragging = True
                if reload_speed_slider.knob.collidepoint(event.pos): reload_speed_slider.dragging = True
                if bullet_limit_slider.knob.collidepoint(event.pos): bullet_limit_slider.dragging = True
                if bullet_lifetime_slider.knob.collidepoint(event.pos): bullet_lifetime_slider.dragging = True
                elif back_button.is_clicked(pos):
                    show_settings = False
                    if opened_from_game:
                        show_game = True
                        opened_from_game = False
                        is_paused = False
                        game_start_time = time.time() - paused_time
                elif exit_button.is_clicked(pos) and not opened_from_game:
                    sys.exit()
                elif main_menu_button.is_clicked(pos) and opened_from_game:
                    show_settings = False
                    show_game = True
                    opened_from_game = False
                    is_paused = False
                    exit_to_victory = True
            elif show_game and settings_game_button.is_clicked(pos):
                show_game = False
                show_settings = True
                opened_from_game = True
                is_paused = True
                paused_time = time.time() - game_start_time
            elif show_victory and victory_main_menu_button.is_clicked(pos):
                show_victory = False
                player1_score = player2_score = 0
                player1_pos = pygame.Vector2(0, 0)
                player2_pos = pygame.Vector2(0, 0)
                angle1 = angle2 = 0
                player1_bullets.clear()
                player2_bullets.clear()
                last_shot_time_p1 = last_shot_time_p2 = 0
                game_time_seconds = game_start_time = paused_time = 0
                maze_lines, rect = [], pygame.Rect(0, 0, 0, 0)
                maze_surface = None
                is_paused = False
                game_mode = "PvP"
                bot_difficulty = "Easy"
                player1_name, player2_name = "", ""
                player1_input.text, player2_input.text = "", ""
                player_input.text, time_input.text = "", ""
                player1_input.active = player2_input.active = player_input.active = time_input.active = False
                player1_skill = player2_skill = None
                player1_skill_active = player2_skill_active = False
                player1_smaller_timer = player2_smaller_timer = 0.0
                active_mines.clear()
            elif show_tutorial:
                if back_button.is_clicked(pos):
                    show_tutorial = False
                    tutorial_text_box = None
                elif tutorial_text_box:
                    tutorial_text_box.handle_event(event)
            elif show_credits:
                if back_button.is_clicked(pos):
                    show_credits = False
                elif readme_button.is_clicked(pos):
                    open_readme()
                elif update_history_button.is_clicked(pos):
                    show_update_history = True
                    show_credits = False
                    update_history_box = TextBox(140, 140, 1000, 500, update_history_text, tutorial_font)
            elif show_update_history:
                if back_button.is_clicked(pos):
                    show_update_history = False
                    show_credits = True
                    update_history_box = None
                elif update_history_box:
                    update_history_box.handle_event(event)
            elif not (show_credits or show_game or show_settings or show_mode_select \
                      or show_pvp or show_pve or show_difficulty or show_victory or show_tutorial):
                for button in buttons:
                    if button.is_clicked(pos):
                        if button.text == "Credits":
                            show_credits = True
                        elif button.text == "Play Game":
                            show_mode_select = True
                        elif button.text == "Settings":
                            show_settings = True
                        elif button.text == "Tutorial":
                            show_tutorial = True
            if show_pvp or show_pve:
                time_inf_checkbox.handle_event(event)

        if event.type == pygame.MOUSEWHEEL:
            if show_tutorial and tutorial_text_box:
                tutorial_text_box.scroll(-event.y * 20)
            elif show_update_history and update_history_box:
                update_history_box.scroll(-event.y * 20)
            elif show_pvp:
                player1_input.handle_event(event)
                player2_input.handle_event(event)
                time_input.handle_event(event)
            elif show_pve:
                player_input.handle_event(event)
                time_input.handle_event(event)

        if event.type == pygame.MOUSEMOTION:
            if show_settings:
                if music_slider.dragging: music_slider.set_knob_pos(event.pos[0])
                if sound_slider.dragging: sound_slider.set_knob_pos(event.pos[0])
                if tank_speed_slider.dragging: tank_speed_slider.set_knob_pos(event.pos[0])
                if bullet_speed_slider.dragging: bullet_speed_slider.set_knob_pos(event.pos[0])
                if reload_speed_slider.dragging: reload_speed_slider.set_knob_pos(event.pos[0])
                if bullet_limit_slider.dragging: bullet_limit_slider.set_knob_pos(event.pos[0])
                if bullet_lifetime_slider.dragging: bullet_lifetime_slider.set_knob_pos(event.pos[0])
            if show_tutorial and tutorial_text_box:
                tutorial_text_box.handle_event(event)
            elif show_update_history and update_history_box:
                update_history_box.handle_event(event)

        if event.type == pygame.MOUSEBUTTONUP:
            music_slider.dragging, sound_slider.dragging = False, False
            tank_speed_slider.dragging, bullet_speed_slider.dragging = False, False
            reload_speed_slider.dragging, bullet_limit_slider.dragging = False, False
            bullet_lifetime_slider.dragging = False
            if show_tutorial and tutorial_text_box:
                tutorial_text_box.handle_event(event)
            elif show_update_history and update_history_box:
                update_history_box.handle_event(event)

    if show_settings:
        music_volume = music_slider.get_value()
        pygame.mixer.music.set_volume(music_volume)
        sound_volume = sound_slider.get_value()
        click_sound.set_volume(sound_volume)
        explosion_sound.set_volume(sound_volume)
        speed = tank_speed_slider.get_value()
        bullet_speed = bullet_speed_slider.get_value()
        reload_speed = reload_speed_slider.get_value()
        if not bullet_limit_inf_checkbox.checked:
            bullet_limit = int(bullet_limit_slider.get_value())
        bullet_lifetime = bullet_lifetime_slider.get_value()

    if show_tutorial and tutorial_text_box is None:
        tutorial_text_box = TextBox(140, 140, 1000, 500, tutorial_text, tutorial_font)

    screen.blit(background, (0, 0))

    if show_credits:
        back_button.draw(screen)
        draw_text_with_shadow(screen, "Credits", pixel_font, WHITE, BLACK, WIDTH // 2 - 160, 60)
        for i, name in enumerate(["Developer:", "Đinh Nguyên Khoa", "Trần Minh Hiếu 09",
                                "Nguyễn Trương Ngọc Huy", "Phan Khánh Lâm", "AI: Grok 3, Chat GPT 4o, Copilot VSC"]):
            screen.blit(viet_font.render(name, True, WHITE), (WIDTH // 2 - viet_font.size(name)[0] // 2, HEIGHT // 2 - 200 + i * 50))
        screen.blit(viet_font.render("_Version: Beta 3.0.3_", True, WHITE), (WIDTH // 2 - viet_font.size("_Version: Beta 3.0.3_")[0] // 2, HEIGHT // 2 + 125))
        update_history_button.draw(screen)
        screen.blit(viet_font.render("Copyright © 2025 Blitzkrieg", True, WHITE), (WIDTH // 2 - viet_font.size("Copyright © 2025 Blitzkrieg")[0] // 2, HEIGHT // 2 + 165))
        screen.blit(viet_font.render("Contact us if you see any bugs", True, WHITE), (WIDTH // 2 - viet_font.size("Contact us if you see any bugs")[0] // 2, HEIGHT // 2 + 235))
        readme_button.draw(screen)
        update_history_button.draw(screen)

    elif show_update_history:
        back_button.draw(screen)
        screen.blit(pixel_font.render("Update History", True, WHITE), (WIDTH // 2 - pixel_font.size("Update History")[0] // 2, 30))
        if update_history_box:
            update_history_box.draw(screen)
        if tutorial_text_box:
            tutorial_text_box.draw(screen)
        if back_button.is_clicked(pos):
            show_update_history = False
            show_credits = True

    elif show_game:
        if slow_motion:
            shake_offset = pygame.Vector2(random.uniform(-5, 5), random.uniform(-5, 5))
        else:
            shake_offset = pygame.Vector2(0, 0)
        screen.blit(maze_surface, shake_offset)
        
        for buff in buffs:
            screen.blit(buff.image, buff.rect.move(shake_offset))

        # Vẽ mìn
        for mine in active_mines:
            mine.update(dt)
            mine.draw(screen)

        scoreboard_width, scoreboard_height = 180, 150
        scoreboard_x = rect.width + (WIDTH - rect.width - scoreboard_width) // 2
        scoreboard_y = (HEIGHT - scoreboard_height) // 2

        settings_game_button.rect.x = scoreboard_x
        settings_game_button.rect.y = scoreboard_y - 60
        if game_mode == "PvP":
            settings_game_button.color = (100, 200, 100)
            settings_game_button.hover_color = (150, 255, 150)
        else:
            screen.blit(small_battle_font.render(bot_difficulty.upper(), True, (255, 50, 50)), (1125 + (155 - small_battle_font.size(bot_difficulty.upper())[0]) // 2, 165))
            settings_game_button.color = (100, 150, 255)
            settings_game_button.hover_color = (150, 200, 255)
        settings_game_button.draw(screen)

        pygame.draw.rect(screen, WHITE, (scoreboard_x, scoreboard_y, scoreboard_width, scoreboard_height), 2)
        screen.blit(player1_image, (scoreboard_x + 10, scoreboard_y + 10))
        screen.blit(small_font.render(f" {player1_name}", True, WHITE), (scoreboard_x + 45, scoreboard_y + 15))
        screen.blit(small_font.render(f"Score: {player1_score}", True, WHITE), (scoreboard_x + 10, scoreboard_y + 50))
        screen.blit(player2_image, (scoreboard_x + 10, scoreboard_y + 80))
        screen.blit(small_font.render(f" {player2_name}", True, WHITE), (scoreboard_x + 45, scoreboard_y + 85))
        screen.blit(small_font.render(f"Score: {player2_score}", True, WHITE), (scoreboard_x + 10, scoreboard_y + 120))

        keys = pygame.key.get_pressed()
        current_time = time.time()

        # Vẽ tank với kích thước thay đổi nếu có skill Smaller
        draw_tank(player1_pos, angle1, player1_image, player1_smaller_timer)
        draw_tank(player2_pos, angle2, player2_image, player2_smaller_timer)

        # Hiển thị icon skill phía trên tank
        if player1_skill:
            if player1_skill == "laser_beam":
                icon = laser_icon
            elif player1_skill == "shield":
                icon = shield_icon
            elif player1_skill == "mine":
                icon = mine_icon
            elif player1_skill == "smaller":
                icon = smaller_icon
            icon_rect = icon.get_rect(center=(player1_pos.x, player1_pos.y - 120))
            screen.blit(icon, icon_rect)

        if player2_skill:
            if player2_skill == "laser_beam":
                icon = laser_icon
            elif player2_skill == "shield":
                icon = shield_icon
            elif player2_skill == "mine":
                icon = mine_icon
            elif player2_skill == "smaller":
                icon = smaller_icon
            icon_rect = icon.get_rect(center=(player2_pos.x, player2_pos.y - 120))
            screen.blit(icon, icon_rect)

        # Xử lý shield khi active
        if player1_skill == "shield" and player1_skill_active:
            pygame.draw.circle(screen, (0, 0, 255), player1_pos, 20, 2)
        if player2_skill == "shield" and player2_skill_active:
            pygame.draw.circle(screen, (0, 0, 255), player2_pos, 20, 2)

        if not is_paused and not time_inf_checkbox.checked:
            if not slow_motion:
                elapsed_time = current_time - game_start_time
                if elapsed_time > game_time_seconds:
                    show_game = False
                    show_victory = True
                    final_game_surface = screen.copy()
                else:
                    remaining_time = max(0, game_time_seconds - elapsed_time)
                    time_text = f"Time Left: {int(remaining_time)}s"
                    text_width = small_font.size(time_text)[0]
                    max_width = WIDTH - 1130
                    if text_width <= max_width:
                        screen.blit(small_font.render(time_text, True, WHITE), (1130, 450))
                    else:
                        screen.blit(small_font.render("Time Left:", True, WHITE), (1130, 450))
                        remaining_str = str(int(remaining_time))
                        chunk_size = 10
                        chunks = [remaining_str[i:i+chunk_size] for i in range(0, len(remaining_str), chunk_size)]
                        for i, chunk in enumerate(chunks):
                            y_pos = 450 + (i + 1) * 25
                            if i == len(chunks) - 1:
                                screen.blit(small_font.render(f"{chunk}s", True, WHITE), (1130, y_pos))
                            else:
                                screen.blit(small_font.render(chunk, True, WHITE), (1130, y_pos))
            else:
                remaining_time = max(0, game_time_seconds - slow_motion_paused_time)
                time_text = f"Time Left: {int(remaining_time)}s"
                text_width = small_font.size(time_text)[0]
                max_width = WIDTH - 1130
                if text_width <= max_width:
                    screen.blit(small_font.render(time_text, True, WHITE), (1130, 450))
                else:
                    screen.blit(small_font.render("Time Left:", True, WHITE), (1130, 450))
                    remaining_str = str(int(remaining_time))
                    chunk_size = 10
                    chunks = [remaining_str[i:i+chunk_size] for i in range(0, len(remaining_str), chunk_size)]
                    for i, chunk in enumerate(chunks):
                        y_pos = 450 + (i + 1) * 25
                        if i == len(chunks) - 1:
                            screen.blit(small_font.render(f"{chunk}s", True, WHITE), (1130, y_pos))
                        else:
                            screen.blit(small_font.render(chunk, True, WHITE), (1130, y_pos))
        elif is_paused and not time_inf_checkbox.checked:
            remaining_time = max(0, game_time_seconds - paused_time)
            time_text = f"Time Left: {int(remaining_time)}s"
            text_width = small_font.size(time_text)[0]
            max_width = WIDTH - 1130
            if text_width <= max_width:
                screen.blit(small_font.render(time_text, True, WHITE), (1130, 450))
            else:
                screen.blit(small_font.render("Time Left:", True, WHITE), (1130, 450))
                remaining_str = str(int(remaining_time))
                chunk_size = 10
                chunks = [remaining_str[i:i+chunk_size] for i in range(0, len(remaining_str), chunk_size)]
                for i, chunk in enumerate(chunks):
                    y_pos = 450 + (i + 1) * 25
                    if i == len(chunks) - 1:
                        screen.blit(small_font.render(f"{chunk}s", True, WHITE), (1130, y_pos))
                    else:
                        screen.blit(small_font.render(chunk, True, WHITE), (1130, y_pos))

        if slow_motion:
            dt = dt * 0.09
            shake_offset = pygame.Vector2(random.uniform(-20, 20), random.uniform(-20, 20))
            elapsed = current_time - slow_motion_start
            overlay_alpha = 100 + 50 * math.sin(elapsed * 10)
            if current_time - slow_motion_start >= slow_motion_duration:
                slow_motion = False
                explosion = None
                shake_offset = pygame.Vector2(0, 0)
                overlay_alpha = 0
                maze_lines, rect = generate_maze()

        if explosion:
            if explosion.update(dt):
                explosion.draw(screen)
            else:
                explosion = None
        if explosion2:
            if explosion2.update(dt):
                explosion2.draw(screen)
            else:
                explosion2 = None
        if slow_motion and overlay_alpha > 0:
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(overlay_alpha)
            overlay.fill((0, 0, 0))
            screen.blit(overlay, (0, 0))

        if exit_to_victory:
            final_game_surface = screen.copy()
            show_game = False
            show_victory = True
            exit_to_victory = False

        if not is_paused and not slow_motion:
            current_time = time.time()

            # Spawn buffs
            if len(buffs) < 5 and current_time >= next_buff_spawn_time:
                while True:
                    x = random.randint(rect.left + 9, rect.right - 9)
                    y = random.randint(rect.top + 9, rect.bottom - 9)
                    buff_rect = pygame.Rect(x - 9, y - 9, 18, 18)
                    if not any(buff_rect.clipline(line) for line in maze_lines):
                        buffs.append(Buff(x, y))
                        break
                next_buff_spawn_time += 5

            # Update skill timers
            if player1_skill_active and player1_skill == "laser_beam":
                player1_skill_timer -= dt
                if player1_skill_timer <= 0:
                    player1_skill_active = False
                    player1_skill = None
            if player2_skill_active and player2_skill == "laser_beam":
                player2_skill_timer -= dt
                if player2_skill_timer <= 0:
                    player2_skill_active = False
                    player2_skill = None

            # Update Smaller timers
            if player1_smaller_timer > 0:
                player1_smaller_timer -= dt
                if player1_smaller_timer <= 0:
                    player1_skill = None
                    player1_smaller_timer = 0.0
            if player2_smaller_timer > 0:
                player2_smaller_timer -= dt
                if player2_smaller_timer <= 0:
                    player2_skill = None
                    player2_smaller_timer = 0.0

            # Draw lasers if active
            offset_distance = 20
            if player1_skill_active and player1_skill == "laser_beam":
                laser_start = player1_pos + pygame.Vector2(offset_distance * math.cos(math.radians(player1_laser_angle)),
                                                          offset_distance * math.sin(math.radians(player1_laser_angle)))
                laser_end = find_laser_endpoint(laser_start, player1_laser_angle, maze_lines, rect)
                pygame.draw.line(screen, (0, 255, 255), laser_start + shake_offset, laser_end + shake_offset, 9)
                tank2_size = smaller_tank_size if player2_smaller_timer > 0 else original_tank_size
                tank2_rect = pygame.Rect(player2_pos.x - tank2_size // 2, player2_pos.y - tank2_size // 2, tank2_size, tank2_size)
                if check_laser_collision(tank2_rect, laser_start, laser_end, 9) and not slow_motion:
                    player1_score += 1
                    explosion = Explosion(player2_pos.x, player2_pos.y)
                    explosion_sound.play()
                    slow_motion = True
                    slow_motion_start = current_time
                    slow_motion_paused_time = current_time - game_start_time
                    player1_bullets.clear()
                    player2_bullets.clear()
                    active_mines.clear()
                    buffs = []
                    player1_skill = None
                    player1_skill_active = False
                    player1_smaller_timer = 0.0
                    player2_skill = None
                    player2_skill_active = False
                    player2_smaller_timer = 0.0
            if player2_skill_active and player2_skill == "laser_beam":
                laser_start = player2_pos + pygame.Vector2(offset_distance * math.cos(math.radians(player2_laser_angle)),
                                                          offset_distance * math.sin(math.radians(player2_laser_angle)))
                laser_end = find_laser_endpoint(laser_start, player2_laser_angle, maze_lines, rect)
                pygame.draw.line(screen, (0, 255, 255), laser_start + shake_offset, laser_end + shake_offset, 9)
                tank1_size = smaller_tank_size if player1_smaller_timer > 0 else original_tank_size
                tank1_rect = pygame.Rect(player1_pos.x - tank1_size // 2, player1_pos.y - tank1_size // 2, tank1_size, tank1_size)
                if check_laser_collision(tank1_rect, laser_start, laser_end, 9) and not slow_motion:
                    player2_score += 1
                    explosion = Explosion(player1_pos.x, player1_pos.y)
                    explosion_sound.play()
                    slow_motion = True
                    slow_motion_start = current_time
                    slow_motion_paused_time = current_time - game_start_time
                    player1_bullets.clear()
                    player2_bullets.clear()
                    active_mines.clear()
                    buffs = []
                    player1_skill = None
                    player1_skill_active = False
                    player1_smaller_timer = 0.0
                    player2_skill = None
                    player2_skill_active = False
                    player2_smaller_timer = 0.0

            # Điều khiển Player 1
            delta_x1 = 0
            delta_y1 = 0
            tank1_size = smaller_tank_size if player1_smaller_timer > 0 else original_tank_size
            if not player1_skill_active or player1_skill == "shield" or player1_skill == "smaller":
                if keys[pygame.K_w]:
                    delta_x1 += speed * dt * math.cos(math.radians(angle1))
                    delta_y1 += speed * dt * math.sin(math.radians(angle1))
                if keys[pygame.K_s]:
                    delta_x1 -= speed * dt * math.cos(math.radians(angle1))
                    delta_y1 -= speed * dt * math.sin(math.radians(angle1))
                if keys[pygame.K_a]:
                    angle1 -= 200 * dt
                if keys[pygame.K_d]:
                    angle1 += 200 * dt

            if delta_x1 != 0 or delta_y1 != 0:
                temp_pos1 = player1_pos.copy()
                temp_pos1.x += delta_x1
                if not check_collision(temp_pos1, maze_lines, tank1_size):
                    player1_pos.x = temp_pos1.x
                temp_pos1 = player1_pos.copy()
                temp_pos1.y += delta_y1
                if not check_collision(temp_pos1, maze_lines, tank1_size):
                    player1_pos.y = temp_pos1.y
                if current_time - last_smoke_time_p1 >= smoke_spawn_rate:
                    player1_smoke_particles.append(SmokeParticle(player1_pos.x - 15 * math.cos(math.radians(angle1)),
                                                                player1_pos.y - 15 * math.sin(math.radians(angle1)), angle1))
                    last_smoke_time_p1 = current_time
            if keys[pygame.K_r] and current_time - last_shot_time_p1 > reload_speed:
                if player1_skill == "laser_beam" and not player1_skill_active:
                    player1_skill_active = True
                    player1_skill_timer = 5.0
                    player1_laser_angle = angle1
                    last_shot_time_p1 = current_time
                elif player1_skill == "mine":
                    active_mines.append(Mine(player1_pos.x, player1_pos.y))
                    player1_skill = None
                    last_shot_time_p1 = current_time
                elif not player1_skill_active or player1_skill == "shield" or player1_skill == "smaller":
                    if bullet_limit_inf_checkbox.checked or len(player1_bullets) < bullet_limit:
                        player1_bullets.append(Bullet(player1_pos.x + 30 * math.cos(math.radians(angle1)), player1_pos.y + 30 * math.sin(math.radians(angle1)), angle1))
                        last_shot_time_p1 = current_time

            # Kiểm tra va chạm với mìn
            tank1_rect = pygame.Rect(player1_pos.x - tank1_size // 2, player1_pos.y - tank1_size // 2, tank1_size, tank1_size)
            tank2_size = smaller_tank_size if player2_smaller_timer > 0 else original_tank_size
            tank2_rect = pygame.Rect(player2_pos.x - tank2_size // 2, player2_pos.y - tank2_size // 2, tank2_size, tank2_size)
            for mine in active_mines[:]:
                if not mine.visible:
                    mine_rect = mine.rect
                    if tank1_rect.colliderect(mine_rect) and not slow_motion:
                        player2_score += 1
                        explosion = Explosion(player1_pos.x, player1_pos.y)
                        explosion_sound.play()
                        slow_motion = True
                        slow_motion_start = current_time
                        slow_motion_paused_time = current_time - game_start_time
                        player1_bullets.clear()
                        player2_bullets.clear()
                        active_mines.remove(mine)
                        buffs = []
                        player1_skill = None
                        player1_skill_active = False
                        player1_smaller_timer = 0.0
                        player2_skill = None
                        player2_skill_active = False
                        player2_smaller_timer = 0.0
                        break
                    elif tank2_rect.colliderect(mine_rect) and not slow_motion:
                        player1_score += 1
                        explosion = Explosion(player2_pos.x, player2_pos.y)
                        explosion_sound.play()
                        slow_motion = True
                        slow_motion_start = current_time
                        slow_motion_paused_time = current_time - game_start_time
                        player1_bullets.clear()
                        player2_bullets.clear()
                        active_mines.remove(mine)
                        buffs = []
                        player1_skill = None
                        player1_skill_active = False
                        player1_smaller_timer = 0.0
                        player2_skill = None
                        player2_skill_active = False
                        player2_smaller_timer = 0.0
                        break

            if game_mode == "PvE":
                bot_speed = speed
                bot_reload = reload_speed
                direction_to_player = player1_pos - player2_pos
                distance_to_player = direction_to_player.length()

                if bot_difficulty == "Easy":
                    detection_radius = 200
                    accuracy = 0.6
                    dodge_chance = 0.6
                    turn_speed = 200 * 0.8
                    center_x, center_y = WIDTH // 2, HEIGHT // 2
                    if not (center_x - 200 < player2_pos.x < center_x + 200 and center_y - 200 < player2_pos.y < center_y + 200):
                        target_pos = pygame.Vector2(center_x, center_y)
                    elif distance_to_player < detection_radius:
                        target_pos = player1_pos
                    else:
                        target_pos = pygame.Vector2(player2_pos.x + random.uniform(-100, 100), player2_pos.y + random.uniform(-100, 100))

                elif bot_difficulty == "Medium":
                    detection_radius = 350
                    accuracy = 0.8
                    dodge_chance = 0.8
                    turn_speed = 200
                    if distance_to_player < detection_radius:
                        target_pos = player1_pos
                    else:
                        target_pos = pygame.Vector2(player2_pos.x + random.uniform(-200, 200), player2_pos.y + random.uniform(-200, 200))

                elif bot_difficulty == "Hard":
                    detection_radius = 500
                    accuracy = 0.99
                    dodge_chance = 0.99
                    turn_speed = 200 * 1.2
                    path = a_star(player2_pos, player1_pos, maze_lines, rect)
                    if path and len(path) > 1:
                        next_step = path[1]
                        target_pos = pygame.Vector2(next_step[0] * (CELL_SIZE // 2) + (CELL_SIZE // 4),
                                                next_step[1] * (CELL_SIZE // 2) + (CELL_SIZE // 4))
                    else:
                        target_pos = player1_pos

                if bot_difficulty in ["Easy", "Medium"]:
                    bot_position_history.append((int(player2_pos.x // 20), int(player2_pos.y // 20)))
                    if len(bot_position_history) > bot_history_limit:
                        bot_position_history.pop(0)
                    current_pos = (int(target_pos.x // 20), int(target_pos.y // 20))
                    visit_count = bot_position_history.count(current_pos)
                    if visit_count > 2:
                        target_pos = pygame.Vector2(player2_pos.x + random.uniform(-200, 200),
                                                player2_pos.y + random.uniform(-200, 200))

                dodge_triggered = False
                for bullet in player1_bullets:
                    bullet_pos = pygame.Vector2(bullet.pos.x, bullet.pos.y)
                    distance_to_bullet = (bullet_pos - player2_pos).length()
                    if distance_to_bullet < 100:
                        if random.random() < dodge_chance:
                            bullet_angle = math.degrees(math.atan2(bullet.pos.y - player1_pos.y, bullet.pos.x - player1_pos.x))
                            dodge_angle = bullet_angle + random.choice([-90, 90])
                            angle2 = dodge_angle
                            dodge_triggered = True
                            break

                target_angle = math.degrees(math.atan2(target_pos.y - player2_pos.y, target_pos.x - player2_pos.x))
                angle_diff = (target_angle - angle2 + 180) % 360 - 180

                delta_x2 = bot_speed * dt * math.cos(math.radians(angle2))
                delta_y2 = bot_speed * dt * math.sin(math.radians(angle2))
                temp_pos2 = player2_pos.copy()
                temp_pos2.x += delta_x2
                temp_pos2.y += delta_y2

                should_turn = False
                tank2_size = smaller_tank_size if player2_smaller_timer > 0 else original_tank_size
                if check_collision(temp_pos2, maze_lines, tank2_size):
                    should_turn = True
                elif distance_to_player < detection_radius:
                    should_turn = True

                if not player2_skill_active or player2_skill == "shield" or player2_skill == "smaller":
                    if should_turn and abs(angle_diff) > 5:
                        if angle_diff > 0:
                            angle2 += turn_speed * dt
                        else:
                            angle2 -= turn_speed * dt
                    elif not check_collision(temp_pos2, maze_lines, tank2_size):
                        player2_pos.x = temp_pos2.x
                        player2_pos.y = temp_pos2.y
                        if current_time - last_smoke_time_p2 >= smoke_spawn_rate:
                            player2_smoke_particles.append(SmokeParticle(player2_pos.x - 15 * math.cos(math.radians(angle2)),
                                                                        player2_pos.y - 15 * math.sin(math.radians(angle2)), angle2))
                            last_smoke_time_p2 = current_time

                if check_collision(temp_pos2, maze_lines, tank2_size):
                    for offset in [-45, 45, -90, 90]:
                        test_angle = angle2 + offset
                        test_pos = player2_pos + pygame.Vector2(bot_speed * dt * math.cos(math.radians(test_angle)),
                                                               bot_speed * dt * math.sin(math.radians(test_angle)))
                        if not check_collision(test_pos, maze_lines, tank2_size):
                            angle2 = test_angle
                            player2_pos.x = test_pos.x
                            player2_pos.y = test_pos.y
                            break

                if distance_to_player < detection_radius and abs(angle_diff) < 20 and current_time - bot_last_shot > bot_reload:
                    if player2_skill == "laser_beam" and not player2_skill_active:
                        player2_skill_active = True
                        player2_skill_timer = 5.0
                        player2_laser_angle = angle2
                        bot_last_shot = current_time
                    elif player2_skill == "mine":
                        active_mines.append(Mine(player2_pos.x, player2_pos.y))
                        player2_skill = None
                        bot_last_shot = current_time
                    elif not player2_skill_active or player2_skill == "shield" or player2_skill == "smaller":
                        if bullet_limit_inf_checkbox.checked or len(player2_bullets) < bullet_limit:
                            shot_angle = angle2 + random.uniform(-30 * (1 - accuracy), 30 * (1 - accuracy))
                            player2_bullets.append(Bullet(player2_pos.x + 30 * math.cos(math.radians(shot_angle)),
                                                        player2_pos.y + 30 * math.sin(math.radians(shot_angle)), shot_angle))
                            bot_last_shot = current_time
            else:
                delta_x2 = 0
                delta_y2 = 0
                tank2_size = smaller_tank_size if player2_smaller_timer > 0 else original_tank_size
                if not player2_skill_active or player2_skill == "shield" or player2_skill == "smaller":
                    if keys[pygame.K_UP]:
                        delta_x2 += speed * dt * math.cos(math.radians(angle2))
                        delta_y2 += speed * dt * math.sin(math.radians(angle2))
                    if keys[pygame.K_DOWN]:
                        delta_x2 -= speed * dt * math.cos(math.radians(angle2))
                        delta_y2 -= speed * dt * math.sin(math.radians(angle2))
                    if keys[pygame.K_LEFT]:
                        angle2 -= 200 * dt
                    if keys[pygame.K_RIGHT]:
                        angle2 += 200 * dt

                if delta_x2 != 0 or delta_y2 != 0:
                    temp_pos2 = player2_pos.copy()
                    temp_pos2.x += delta_x2
                    if not check_collision(temp_pos2, maze_lines, tank2_size):
                        player2_pos.x = temp_pos2.x
                    temp_pos2 = player2_pos.copy()
                    temp_pos2.y += delta_y2
                    if not check_collision(temp_pos2, maze_lines, tank2_size):
                        player2_pos.y = temp_pos2.y
                    if current_time - last_smoke_time_p2 >= smoke_spawn_rate:
                        player2_smoke_particles.append(SmokeParticle(player2_pos.x - 15 * math.cos(math.radians(angle2)),
                                                                    player2_pos.y - 15 * math.sin(math.radians(angle2)), angle2))
                        last_smoke_time_p2 = current_time

                if keys[pygame.K_BACKSLASH] and current_time - last_shot_time_p2 > reload_speed:
                    if player2_skill == "laser_beam" and not player2_skill_active:
                        player2_skill_active = True
                        player2_skill_timer = 5.0
                        player2_laser_angle = angle2
                        last_shot_time_p2 = current_time
                    elif player2_skill == "mine":
                        active_mines.append(Mine(player2_pos.x, player2_pos.y))
                        player2_skill = None
                        last_shot_time_p2 = current_time
                    elif not player2_skill_active or player2_skill == "shield" or player2_skill == "smaller":
                        if bullet_limit_inf_checkbox.checked or len(player2_bullets) < bullet_limit:
                            player2_bullets.append(Bullet(player2_pos.x + 30 * math.cos(math.radians(angle2)), player2_pos.y + 30 * math.sin(math.radians(angle2)), angle2))
                            last_shot_time_p2 = current_time

            # Kiểm tra va chạm tank với buff
            tank1_rect = pygame.Rect(player1_pos.x - tank1_size // 2, player1_pos.y - tank1_size // 2, tank1_size, tank1_size)
            tank2_rect = pygame.Rect(player2_pos.x - tank2_size // 2, player2_pos.y - tank2_size // 2, tank2_size, tank2_size)
            for buff in buffs[:]:
                if tank1_rect.colliderect(buff.rect):
                    if player1_skill is None:
                        buffs.remove(buff)
                        effect = random.randint(1, 4)
                        print(f"Tank 1 picked up buff with effect {effect}")
                        if effect == 1:
                            player1_skill = "laser_beam"
                            print("Tank 1 gained Laser Beam skill")
                        elif effect == 2:
                            player1_skill = "shield"
                            player1_skill_active = True
                            print("Tank 1 gained Shield skill")
                        elif effect == 3:
                            player1_skill = "mine"
                            print("Tank 1 gained Mine skill")
                        elif effect == 4:
                            player1_skill = "smaller"
                            player1_smaller_timer = 15.0
                            print("Tank 1 gained Smaller skill")
                elif tank2_rect.colliderect(buff.rect):
                    if player2_skill is None:
                        buffs.remove(buff)
                        effect = random.randint(1, 4)
                        print(f"Tank 2 picked up buff with effect {effect}")
                        if effect == 1:
                            player2_skill = "laser_beam"
                            print("Tank 2 gained Laser Beam skill")
                        elif effect == 2:
                            player2_skill = "shield"
                            player2_skill_active = True
                            print("Tank 2 gained Shield skill")
                        elif effect == 3:
                            player2_skill = "mine"
                            print("Tank 2 gained Mine skill")
                        elif effect == 4:
                            player2_skill = "smaller"
                            player2_smaller_timer = 15.0
                            print("Tank 2 gained Smaller skill")

            # Va chạm tank đụng nhau
            if tank1_rect.colliderect(tank2_rect) and not slow_motion:
                explosion = Explosion(player1_pos.x, player1_pos.y)
                explosion2 = Explosion(player2_pos.x, player2_pos.y)
                explosion_sound.play()
                slow_motion = True
                slow_motion_start = current_time
                slow_motion_paused_time = current_time - game_start_time
                player1_bullets.clear()
                player2_bullets.clear()
                active_mines.clear()
                buffs = []
                player1_skill = None
                player1_skill_active = False
                player1_smaller_timer = 0.0
                player2_skill = None
                player2_skill_active = False
                player2_smaller_timer = 0.0

        for smoke in player1_smoke_particles[:]:
            if smoke.update(dt):
                smoke.draw(screen)
            else:
                player1_smoke_particles.remove(smoke)
        for smoke in player2_smoke_particles[:]:
            if smoke.update(dt):
                smoke.draw(screen)
            else:
                player2_smoke_particles.remove(smoke)

        all_bullets = player1_bullets + player2_bullets
        i = len(all_bullets) - 1
        while i >= 0:
            if i >= len(all_bullets):
                i -= 1
                continue

            bullet = all_bullets[i]
            bullet.update(dt, maze_lines)
            bullet_rect = pygame.Rect(bullet.pos.x - 5, bullet.pos.y - 5, 10, 10)

            # Check collision with lasers
            offset_distance = 20
            if player1_skill_active and player1_skill == "laser_beam":
                laser_start = player1_pos + pygame.Vector2(offset_distance * math.cos(math.radians(player1_laser_angle)),
                                                          offset_distance * math.sin(math.radians(player1_laser_angle)))
                laser_end = find_laser_endpoint(laser_start, player1_laser_angle, maze_lines, rect)
                if bullet_rect.clipline(laser_start, laser_end):
                    if bullet in player1_bullets:
                        player1_bullets.remove(bullet)
                    elif bullet in player2_bullets:
                        player2_bullets.remove(bullet)
                    i -= 1
                    continue
            if player2_skill_active and player2_skill == "laser_beam":
                laser_start = player2_pos + pygame.Vector2(offset_distance * math.cos(math.radians(player2_laser_angle)),
                                                          offset_distance * math.sin(math.radians(player2_laser_angle)))
                laser_end = find_laser_endpoint(laser_start, player2_laser_angle, maze_lines, rect)
                if bullet_rect.clipline(laser_start, laser_end):
                    if bullet in player1_bullets:
                        player1_bullets.remove(bullet)
                    elif bullet in player2_bullets:
                        player2_bullets.remove(bullet)
                    i -= 1
                    continue

            bullet.draw()

            if not bullet_lifetime_inf_checkbox.checked and current_time - bullet.spawn_time > bullet_lifetime:
                if bullet in player1_bullets:
                    player1_bullets.remove(bullet)
                elif bullet in player2_bullets:
                    player2_bullets.remove(bullet)
                i -= 1
                continue

            j = len(all_bullets) - 1
            collision_detected = False
            while j >= 0:
                if j >= len(all_bullets) or j == i:
                    j -= 1
                    continue
                other_bullet = all_bullets[j]
                other_rect = pygame.Rect(other_bullet.pos.x - 5, other_bullet.pos.y - 5, 10, 10)
                if bullet_rect.colliderect(other_rect):
                    if bullet in player1_bullets:
                        player1_bullets.remove(bullet)
                    elif bullet in player2_bullets:
                        player2_bullets.remove(bullet)
                    if other_bullet in player1_bullets:
                        player1_bullets.remove(other_bullet)
                    elif other_bullet in player2_bullets:
                        player2_bullets.remove(other_bullet)
                    collision_detected = True
                    break
                j -= 1

            if collision_detected:
                i -= 1
                continue

            # Check collision with Player 1
            tank1_size = smaller_tank_size if player1_smaller_timer > 0 else original_tank_size
            if pygame.Rect(player1_pos.x - tank1_size // 2, player1_pos.y - tank1_size // 2, tank1_size, tank1_size).collidepoint(bullet.pos):
                if player1_skill == "shield" and player1_skill_active:
                    player1_skill_active = False
                    player1_skill = None
                    if bullet in player1_bullets:
                        player1_bullets.remove(bullet)
                    elif bullet in player2_bullets:
                        player2_bullets.remove(bullet)
                else:
                    player2_score += 1
                    explosion = Explosion(player1_pos.x, player1_pos.y)
                    explosion_sound.play()
                    slow_motion = True
                    slow_motion_start = current_time
                    slow_motion_paused_time = current_time - game_start_time
                    player1_bullets.clear()
                    player2_bullets.clear()
                    active_mines.clear()
                    buffs = []
                    player1_skill = None
                    player1_skill_active = False
                    player1_smaller_timer = 0.0
                    player2_skill = None
                    player2_skill_active = False
                    player2_smaller_timer = 0.0
                    break
            # Check collision with Player 2
            tank2_size = smaller_tank_size if player2_smaller_timer > 0 else original_tank_size
            if pygame.Rect(player2_pos.x - tank2_size // 2, player2_pos.y - tank2_size // 2, tank2_size, tank2_size).collidepoint(bullet.pos):
                if player2_skill == "shield" and player2_skill_active:
                    player2_skill_active = False
                    player2_skill = None
                    if bullet in player1_bullets:
                        player1_bullets.remove(bullet)
                    elif bullet in player2_bullets:
                        player2_bullets.remove(bullet)
                else:
                    player1_score += 1
                    explosion = Explosion(player2_pos.x, player2_pos.y)
                    explosion_sound.play()
                    slow_motion = True
                    slow_motion_start = current_time
                    slow_motion_paused_time = current_time - game_start_time
                    player1_bullets.clear()
                    player2_bullets.clear()
                    active_mines.clear()
                    buffs = []
                    player1_skill = None
                    player1_skill_active = False
                    player1_smaller_timer = 0.0
                    player2_skill = None
                    player2_skill_active = False
                    player2_smaller_timer = 0.0
                    break
            i -= 1

    elif show_settings:
        back_button.draw(screen)
        screen.blit(pixel_font.render("Settings", True, WHITE), (WIDTH // 2 - 160, 20))
        if opened_from_game and is_paused:
            screen.blit(pixel_font.render("PAUSE", True, (255, 50, 50)), (WIDTH - 170 - pixel_font.size("PAUSE")[0] // 2, 300))
            main_menu_button.draw(screen)
        else:
            exit_button.draw(screen)
        screen.blit(battle_font.render("Music", True, WHITE), (270, 120))
        music_slider.draw(screen)
        screen.blit(battle_font.render("Sound Effect", True, WHITE), (160, 200))
        sound_slider.draw(screen)
        screen.blit(battle_font.render("Tank Speed", True, WHITE), (190, 280))
        tank_speed_slider.draw(screen)
        screen.blit(battle_font.render("Bullet Speed", True, WHITE), (160, 360))
        bullet_speed_slider.draw(screen)
        screen.blit(battle_font.render("Reload Speed", True, WHITE), (160, 440))
        reload_speed_slider.draw(screen)
        screen.blit(battle_font.render("Bullet Limit", True, WHITE), (160, 520))
        bullet_limit_slider.draw(screen)
        screen.blit(battle_font.render("Bullet Lifetime", True, WHITE), (110, 600))
        bullet_lifetime_slider.draw(screen)
        bullet_limit_inf_checkbox.draw(screen)
        bullet_lifetime_inf_checkbox.draw(screen)
        playtime = format_time(actual_playtime)
        screen.blit(font.render(playtime, True, WHITE), (WIDTH // 2 - small_font.size(playtime)[0] // 2, HEIGHT - 50))

    elif show_mode_select:
        back_button.draw(screen)
        pvp_button.draw(screen)
        pve_button.draw(screen)

    elif show_pvp:
        back_button.draw(screen)
        screen.blit(tutorial_font.render("Name can be blank", True, WHITE), (470, 160))
        screen.blit(font.render("Player 1", True, WHITE), (400, 250))
        screen.blit(font.render("Player 2", True, WHITE), (400, 350))
        screen.blit(font.render("Time (seconds)", True, WHITE), (320, 450))
        player1_input.draw(screen)
        player2_input.draw(screen)
        time_input.draw(screen)
        time_inf_checkbox.draw(screen)
        enter_button.draw(screen)
        if error_message:
            screen.blit(font.render(error_message, True, WHITE), (WIDTH // 2 - font.size(error_message)[0] // 2, 550))

    elif show_pve:
        back_button.draw(screen)
        screen.blit(tutorial_font.render("Name can be blank", True, WHITE), (470, 240))
        screen.blit(font.render("Player", True, WHITE), (400, 330))
        screen.blit(font.render("Time (seconds)", True, WHITE), (320, 450))
        player_input.draw(screen)
        time_input.draw(screen)
        time_inf_checkbox.draw(screen)
        enter_button.draw(screen)
        if error_message:
            screen.blit(font.render(error_message, True, WHITE), (WIDTH // 2 - font.size(error_message)[0] // 2, 535))
        
    elif show_tutorial:
        back_button.draw(screen)
        screen.blit(pixel_font.render("Tutorial", True, WHITE), (WIDTH // 2 - pixel_font.size("Tutorial")[0] // 2, 30))
        if tutorial_text_box:
            tutorial_text_box.draw(screen)
        
    elif show_difficulty:
        back_button.draw(screen)
        easy_button.draw(screen)
        medium_button.draw(screen)
        hard_button.draw(screen)
        screen.blit(pixel_font.render("Select Difficulty", True, WHITE), (WIDTH // 2 - pixel_font.size("Select Difficulty")[0] // 2, 100))

    elif show_victory:
        screen.blit(final_game_surface, (0, 0))
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(120)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        if player1_score > player2_score:
            winner_line1 = "The Winner is"
            winner_line2 = f"Player 1 : {player1_name}" if player1_name != "Player 1" else "Player 1"
        elif player2_score > player1_score:
            winner_line1 = "The Winner is"
            if game_mode == "PvE" and player2_name == "Bot":
                winner_line2 = "Bot"
            else:
                winner_line2 = f"Player 2 : {player2_name}" if player2_name != "Player 2" else "Player 2"
        else:
            winner_line1 = "It's a Tie!"
            winner_line2 = ""

        screen.blit(pixel_font.render(winner_line1, True, WHITE), (WIDTH // 2 - pixel_font.size(winner_line1)[0] // 2, HEIGHT // 2 - 100))
        if winner_line2:
            screen.blit(pixel_font.render(winner_line2, True, WHITE), (WIDTH // 2 - pixel_font.size(winner_line2)[0] // 2, HEIGHT // 2 - 40))
        victory_main_menu_button.draw(screen)
        
    else:
        draw_text_with_shadow(screen, "Blitzkrieg", pixel_font, WHITE, BLACK, WIDTH // 2 - pixel_font.size("Blitzkrieg")[0] // 2, 100)
        screen.blit(left_logo, (WIDTH // 2 - 550, 300))
        screen.blit(right_logo, (WIDTH // 2 + 200, 300))
        for button in buttons: button.draw(screen)
    
    pygame.display.flip()

__author__ = "Đinh Nguyên Khoa"
__version__ = "Beta 3.0.3"
__date__ = "2025-03-21"