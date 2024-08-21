import pygame
import sys

# 초기화
pygame.init()

# 화면 크기 설정
WIDTH, HEIGHT = 800, 1000
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Ping Pong Game')

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
SKYBLUE = (0, 255, 255)

# 패들 및 공 속성
PADDLE_WIDTH, PADDLE_HEIGHT = 100, 15
BALL_SIZE = 20
INITIAL_LIVES = 3

# 패들 및 공의 초기 위치
paddle = pygame.Rect((WIDTH - PADDLE_WIDTH) // 2, HEIGHT - PADDLE_HEIGHT - 10, PADDLE_WIDTH, PADDLE_HEIGHT)
ball = pygame.Rect(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)

# 패들 및 공의 속도
paddle_speed = 15
ball_speed_x, ball_speed_y = 8, 8

# 게임 상태 변수
lives = INITIAL_LIVES
score = 0
font = pygame.font.Font(None, 36)

def draw_score_lives():
    score_text = font.render(f'Score: {score}', True, WHITE)
    lives_text = font.render(f'Lives: {lives}', True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (10, 50))

def draw_game_over():
    game_over_text = font.render('Game Over', True, RED)
    restart_text = font.render('Press R to Restart', True, WHITE)
    screen.blit(game_over_text, (WIDTH // 2 - 100, HEIGHT // 2 - 50))
    screen.blit(restart_text, (WIDTH // 2 - 150, HEIGHT // 2 + 10))

def reset_game():
    global paddle, ball, ball_speed_x, ball_speed_y, lives, score
    paddle = pygame.Rect((WIDTH - PADDLE_WIDTH) // 2, HEIGHT - PADDLE_HEIGHT - 10, PADDLE_WIDTH, PADDLE_HEIGHT)
    ball = pygame.Rect(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)
    ball_speed_x, ball_speed_y = 8, 8
    lives = INITIAL_LIVES
    score = 0

# 게임 루프
clock = pygame.time.Clock()
game_over = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if not game_over:
        # 패들 조작
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and paddle.left > 0:
            paddle.x -= paddle_speed
        if keys[pygame.K_RIGHT] and paddle.right < WIDTH:
            paddle.x += paddle_speed

        # 공 움직임
        ball.x += ball_speed_x
        ball.y += ball_speed_y

        # 공과 화면 경계 충돌
        if ball.top <= 0:
            ball_speed_y = -ball_speed_y
            score += 1  # 천장을 칠 때 점수 증가
        if ball.bottom >= HEIGHT:
            ball_speed_y = -ball_speed_y
            lives -= 1
            ball.x = WIDTH // 2 - BALL_SIZE // 2
            ball.y = HEIGHT // 2 - BALL_SIZE // 2
            if lives <= 0:
                game_over = True

        if ball.left <= 0 or ball.right >= WIDTH:
            ball_speed_x = -ball_speed_x

        # 공과 패들 충돌
        if ball.colliderect(paddle):
            ball_speed_y = -ball_speed_y

        # 화면 그리기
        screen.fill(BLACK)
        pygame.draw.rect(screen, WHITE, paddle)
        pygame.draw.ellipse(screen, SKYBLUE, ball)
        draw_score_lives()

    else:
        draw_game_over()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            reset_game()
            game_over = False

    pygame.display.flip()
    clock.tick(60)
