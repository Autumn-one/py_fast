import random
import time

# 定义游戏参数
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
BALL_SIZE = 10
PADDLE_SIZE = 100

# 定义游戏对象
class Ball:
  def __init__(self, x, y):
    self.x = x
    self.y = y
    self.vx = random.randint(-5, 5)
    self.vy = random.randint(-5, 5)

  def move(self):
    self.x += self.vx
    self.y += self.vy

    # 反弹
    if self.x < 0 or self.x >= SCREEN_WIDTH:
      self.vx = -self.vx
    if self.y < 0:
      self.vy = -self.vy
    if self.y >= SCREEN_HEIGHT:
      print('Game Over!')
      exit()

class Paddle:
  def __init__(self, x, y):
    self.x = x
    self.y = y

  def move_left(self):
    self.x -= 10

  def move_right(self):
    self.x += 10

# 定义游戏函数
def draw_game():
  # 清除屏幕
  screen.fill((0, 0, 0))

  # 绘制球
  pygame.draw.rect(screen, (255, 255, 255), (ball.x, ball.y, BALL_SIZE, BALL_SIZE))

  # 绘制挡板
  pygame.draw.rect(screen, (255, 255, 255), (paddle.x, paddle.y, PADDLE_SIZE, PADDLE_SIZE))

  # 更新屏幕
  pygame.display.update()

def handle_events():
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      exit()

    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_LEFT:
        paddle.move_left()
      elif event.key == pygame.K_RIGHT:
        paddle.move_right()

# 初始化游戏
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# 创建游戏对象
ball = Ball(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
paddle = Paddle(SCREEN_WIDTH // 2 - PADDLE_SIZE // 2, SCREEN_HEIGHT - PADDLE_SIZE)

# 游戏循环
while True:
  # 处理事件
  handle_events()

  # 更新游戏状态
  ball.move()

  # 碰撞检测
  if ball.y >= paddle.y - BALL_SIZE and ball.x >= paddle.x - BALL_SIZE and ball.x <= paddle.x + PADDLE_SIZE:
    ball.vy = -ball.vy

  # 绘制游戏画面
  draw_game()

  # 限制游戏速度
  clock.tick(60)
