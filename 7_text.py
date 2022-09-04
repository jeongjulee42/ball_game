from cProfile import run
from encodings import utf_8
import pygame

# 게임속에 이미지 부르기

pygame.init()
# 초기화. pygame import시 반드시 호출해준다.

# 화면 크기 설정
screen_width = 480  # 가로 크기
screen_height = 640  # 세로 크기
screen = pygame.display.set_mode((screen_width, screen_height))

# 배경화면
background = pygame.image.load(
    "/Users/jeongju/Desktop/coding/python/proj/pygame_basic/background.png")
# 화면 타이틀 설정
pygame.display.set_caption("Nado Game")

# fps
clock = pygame.time.Clock()


# 스프라이트 불러오기 (캐릭터)
character = pygame.image.load(
    "/Users/jeongju/Desktop/coding/python/proj/pygame_basic/character.png")
character_size = character.get_rect().size  # 이미지 크기를 구해옴
character_width = character_size[0]  # 캐릭터의 가로크기
character_height = character_size[1]  # 캐릭터의 세로크기
character_x_pos = screen_width / 2 - character_width/2  # 화면 가로의 절반 크기에 해당하는 곳에 위치
character_y_pos = screen_height - character_height  # 화면 세로의 크기에 해당하는 곳에 위치

# 이동속도
character_speed = 0.6
# 이후 character xpos, ypos에 dt를 곱해주면 된다.

# 적 캐릭터
enemy = pygame.image.load(
    "/Users/jeongju/Desktop/coding/python/proj/pygame_basic/enemy.png")
enemy_size = enemy.get_rect().size  # 이미지 크기를 구해옴
enemy_width = enemy_size[0]  # 캐릭터의 가로크기
enemy_height = enemy_size[1]  # 캐릭터의 세로크기
enemy_x_pos = screen_width / 2 - enemy_width/2  # 화면 가로의 절반 크기에 해당하는 곳에 위치
enemy_y_pos = screen_height/2 - enemy_height / 2  # 화면 세로의 크기에 해당하는 곳에 위치


# 이동할 좌표
to_x = 0
to_y = 0


# 폰트 정의
game_font = pygame.font.Font(None, 40)
# 폰트 객체 생성(폰트, 크기)

# 총 시간
total_time = 10

# 시작 시간 정보
start_ticks = pygame.time.get_ticks()  # 시작 tick을 받아옴


# 프로그램 종료되지 않도록 대기
# 이벤트 루프
running = True  # 게임이 진행중인지 확인하는 변수
while running:
    dt = clock.tick(60)  # 30 frame 으로 게임 화면의 초당 프레임 수를 설정

    # 현재는 프레임이 달라지면 게임에서 이동 속도 또한 달라진다.
    # 캐릭터가 100만큼 이동을 해야함
    # 10fps: 1초동안 10번 동장 - 한번에 10만큼이동해야함
    # 2pfps: 1초동안 20번 동작 - 한번에 5만큼 이동해야함

    # print("fps : " + str(clock.get_fps())) # 프레임 확인

    for event in pygame.event.get():  # 어떤 이벤트가 발생 하였는가?
        if event.type == pygame.QUIT:  # 창이 닫히는 이벤트가 발생 하였는가?
            running = False  # 게임이 진행중이 아니게됨

        if event.type == pygame.KEYDOWN:  # 키가 눌러 졌는지 확인
            if event.key == pygame.K_LEFT:  # 캐릭터를 왼쪽으로
                to_x -= character_speed
            elif event.key == pygame.K_RIGHT:
                to_x += character_speed
            elif event.key == pygame.K_UP:
                to_y -= character_speed
            elif event.key == pygame.K_DOWN:
                to_y += character_speed

        if event.type == pygame.KEYUP:  # 방향키를 뗴면 멈추도록
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                to_x = 0
            elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                to_y = 0

    character_x_pos += to_x * dt
    character_y_pos += to_y * dt

    # 화면 밖으로 못벗어나도록 조정
    if character_x_pos < 0:
        character_x_pos = 0
    elif character_x_pos > screen_width - character_width:
        character_x_pos = screen_width - character_width

    if character_y_pos < 0:
        character_y_pos = 0
    elif character_y_pos > screen_height - character_height:
        character_y_pos = screen_height - character_height

    # 충돌 처리를 위한 rect 정보 업데이트
    character_rect = character.get_rect()
    character_rect.left = character_x_pos
    character_rect.top = character_y_pos

    enemy_rect = enemy.get_rect()
    enemy_rect.left = enemy_x_pos
    enemy_rect.top = enemy_y_pos

    # 충돌 체크
    if character_rect.colliderect(enemy_rect):  # 사각형 기준으로 충돌을 확인
        print("collide")
        running = False

    screen.blit(background, (0, 0))  # 사진와 좌표 설정, 배경 그리기

    screen.blit(character, (character_x_pos, character_y_pos))

    screen.blit(enemy, (enemy_x_pos, enemy_y_pos))

    # 타이머 집어넣기
    # 경과 시간 계산
    elapsed_time = (pygame.time.get_ticks() - start_ticks) / \
        1000  # 경과 시간(ms 단위)을 1000으로 나누어 초 단위로 표시

    timer = game_font.render(
        str(int(total_time - elapsed_time)), True, (255, 255, 255))
    # 시간 정보(출력할 글자), True, 글자 색상

    screen.blit(timer, (10, 10))

    # 만약 시간이 0 이하이면 게임 종료
    if total_time - elapsed_time <= 0:
        print("time out")
        running = False

    pygame.display.update()  # 화면을 한 프레임마다 다시 그린다.

# 종료되기 직전 잠시 대기하는 코드
pygame.time.delay(2000)  # 2sec hold

# pygame 종료
pygame.quit()
