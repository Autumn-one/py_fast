import random
import time

# 定义游戏参数
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
SNAKE_SIZE = 10
FOOD_SIZE = 10

# 定义游戏对象
class Snake:
  def __init__(self):
    self.body = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
    self.direction = 'right'

  def move(self):
    # 将头部添加到蛇身
    self.body.insert(0, self.get_head())

    # 如果吃到食物，则增长蛇身
    if self.get_head() == food.position:
      self.body.append(self.get_tail())
      food.generate_position()

    # 如果撞到墙壁或自身，则游戏结束
    if self.get_head() in self.body[1:] or self.get_head()[0] < 0 or self.get_head()[0] >= SCREEN_WIDTH or self.get_head()[1] < 0 or self.get_head()[1] >= SCREEN_HEIGHT:
      print('Game Over!')
      exit()

    # 删除尾部
    self.body.pop()

  def get_head(self):
    return self.body[0]

  def get_tail(self):
    return self.body[-1]

  def turn(self, direction):
    self.direction = direction

class Food:
  def __init__(self):
    self.position = (random.randint(0, SCREEN_WIDTH - FOOD_SIZE), random.randint(0, SCREEN_HEIGHT - FOOD_SIZE))

  def generate_position(self):
    self.position = (random.randint(0, SCREEN_WIDTH - FOOD_SIZE), random.randint(0, SCREEN_HEIGHT - FOOD_SIZE))

# 定义游戏函数
def draw_game():
  # 清除屏幕
  screen.fill((0, 0, 0))

  # 绘制蛇
  for i, segment in enumerate(snake.body):
    if i == 0:
      color = (255, 0, 0)
    else:
      color = (0, 255, 0)
    pygame.draw.rect(screen, color, (segment[0], segment[1], SNAKE_SIZE, SNAKE_SIZE))

  # 绘制食物
  pygame.draw.rect(screen, (255, 255, 0), (food.position[0], food.position[1], FOOD_SIZE, FOOD_SIZE))

  # 更新屏幕
  pygame.display.update()

def handle_events():
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      exit()

    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_UP:
        snake.turn('up')
      elif event.key == pygame.K_DOWN:
        snake.turn('down')
      elif event.key == pygame.K_LEFT:
        snake.turn('left')
      elif event.key == pygame.K_RIGHT:
        snake.turn('right')

# 初始化游戏
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# 创建游戏对象
snake = Snake()
food = Food()

# 游戏循环
while True:
  # 处理事件
  handle_events()

  # 更新游戏状态
  snake.move()

  # 绘制游戏画面
  draw_game()

  # 限制游戏速度
  clock.tick(10)
