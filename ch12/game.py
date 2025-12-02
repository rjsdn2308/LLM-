import pygame
import random

# 게임 설정
WIDTH, HEIGHT = 300, 600
BLOCK_SIZE = 30
FPS = 10

# 색상 정의
COLORS = [
    (0, 0, 0),   # 배경
    (255, 0, 0), # 빨간색
    (0, 255, 0), # 초록색
    (0, 0, 255), # 파란색
    (255, 255, 0), # 노란색
    (255, 165, 0), # 주황색
    (128, 0, 128), # 보라색
]

# Tetrimino 모양 정의
TETROMINOS = [
    [[1, 1, 1, 1]],                 # I 모양
    [[1, 1, 1], [0, 1, 0]],         # T 모양
    [[1, 1], [1, 1]],               # O 모양
    [[0, 1, 1], [1, 1, 0]],         # S 모양
    [[1, 1, 0], [0, 1, 1]],         # Z 모양
    [[1, 0, 0], [1, 1, 1]],         # L 모양
    [[0, 0, 1], [1, 1, 1]],         # J 모양
]

class Tetris:
    def __init__(self):
        self.board = [[0] * (WIDTH // BLOCK_SIZE) for _ in range(HEIGHT // BLOCK_SIZE)]
        self.current_tetromino = self.new_tetromino()
        self.score = 0
        
    def new_tetromino(self):
        shape = random.choice(TETROMINOS)
        return {'shape': shape, 'x': WIDTH // BLOCK_SIZE // 2 - len(shape[0]) // 2, 'y': 0}

    def rotate_tetromino(self):
        self.current_tetromino['shape'] = [list(row) for row in zip(*self.current_tetromino['shape'][::-1])]

    def move_tetromino(self, dx, dy):
        self.current_tetromino['x'] += dx
        self.current_tetromino['y'] += dy

    def drop_tetromino(self):
        self.current_tetromino['y'] += 1

    def clear_lines(self):
        lines_to_clear = [i for i, row in enumerate(self.board) if all(row)]
        for i in lines_to_clear:
            del self.board[i]
            self.board.insert(0, [0] * (WIDTH // BLOCK_SIZE))
            self.score += 100

    def game_over(self):
        return any(self.board[0])

def draw_board(screen, board):
    for y, row in enumerate(board):
        for x, cell in enumerate(row):
            pygame.draw.rect(screen, COLORS[cell], (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    game = Tetris()

    running = True
    while running:
        screen.fill(COLORS[0])
        draw_board(screen, game.board)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            game.move_tetromino(-1, 0)
        if keys[pygame.K_RIGHT]:
            game.move_tetromino(1, 0)
        if keys[pygame.K_DOWN]:
            game.drop_tetromino()
        if keys[pygame.K_UP]:
            game.rotate_tetromino()

        game.clear_lines()
        draw_board(screen, game.board)

        pygame.display.flip()
        clock.tick(FPS)

        if game.game_over():
            running = False

    pygame.quit()

if __name__ == "__main__":
    main()