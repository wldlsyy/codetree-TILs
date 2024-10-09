from collections import deque

# 숲의 크기: (R x C), 정령 개수: K
R, C, K = map(int, input().split())
# 정령의 최종 위치를 표시할 배열 선언
forest = [[0 for _ in range(C)] for _ in range(R+3)]
# 0~2번 행 (3줄)은 숲으로 들어오기 전 골렘을 위치하기 위해 'x'로 표시
for i in range(3):
    for j in range(C):
        forest[i][j] = -1

# 북, 동, 남, 서 (인덱스가 곧 방향)
dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]


# 디버깅을 위한 함수
def printGolemStatus(golem):
    print(f'현재 골렘의 중앙: {golem.center}')
    print(f'현재 골렘의 왼쪽: {golem.left}')
    print(f'현재 골렘의 오른쪽: {golem.right}')
    print(f'현재 골렘의 위: {golem.up}')
    print(f'현재 골렘의 아래: {golem.down}')
    print(f'현재 골렘의 출구 방향: {golem.d}')


def printForest():
    for i in range(R+3):
        for j in range(C):
            if forest[i][j] == -1:
                value = 'x'
            else:
                value = forest[i][j]
            print(value, end=" ")
        print()

def printVisited(visited):
    for i in range(R+3):
        for j in range(C):
            print(visited[i][j], end=" ")
        print()

# 골렘 객체
class Golem():
    def __init__(self, c, d, id):
        self.center = [1, c-1]
        self.left = [1, c-2]
        self.right = [1, c]
        self.up = [0, c-1]
        self.down = [2, c-1]
        self.d = d # 출구 방향
        self.id = id # 골렘의 고유번호

    def checkAround(self, dir):
        x = self.center[0] + dx[dir]
        y = self.center[1] + dy[dir]
        #print(f'기준: {x, y}')
        # dir == 1 -> check right
        # dir == 2 -> check down
        # dir == 3 -> check left
        if dir == 1: # check right
            check = [0, 1, 2]
        elif dir == 2: # check down
            check = [1, 3, 2]
        else: # check left
            check = [0, 3, 2]

        for i in check:
            # 경계 벗어났는지 체크
            if x + dx[i] < 0 or x + dx[i] > R + 2 or y + dy[i] < 0 or y + dy[i] > C - 1:
                #print('Out of Bound')
                return False

            if forest[x + dx[i]][y + dy[i]] > 0:
                #print('다른 정령 있음')
                return False
            else:
                continue

        return True

    # 출구방향 시계방향 회전
    def rotateExitCW(self):
        self.d = (self.d + 1) % 4

    # 출구방향 반시계방향 회전
    def rotateExitCCW(self):
        self.d = (self.d + 3) % 4

    def move(self, dir):
        # dir == 1 -> move right
        # dir == 2 -> move down
        # dir == 3 -> move left

        #print(f'---이동하기 전---')
        #printGolemStatus(self)

        self.center[0] += dx[dir]
        self.center[1] += dy[dir]
        self.left[0] += dx[dir]
        self.left[1] += dy[dir]
        self.right[0] += dx[dir]
        self.right[1] += dy[dir]
        self.up[0] += dx[dir]
        self.up[1] += dy[dir]
        self.down[0] += dx[dir]
        self.down[1] += dy[dir]

        # print(f'---이동한 후---')
        # printGolemStatus(self)

def checkInBound(golem):
    # 골렘이 숲 바운더리 안에 있는지 확인
    # 골렘의 5칸 모두 숲 안으로 들어와 있어야 됨.
    if golem.up[0] >= 3 and golem.left[0]  >= 4 and golem.right[0] >= 4 and golem.down[0] >= 5:
        return True
    else:
        return False

def cleanForest():
    global forest
    forest = [[0 for _ in range(C)] for _ in range(R + 3)]
    # 0~2번 행 (3줄)은 숲으로 들어오기 전 골렘을 위치하기 위해 'x'로 표시
    for i in range(3):
        for j in range(C):
            forest[i][j] = -1

def markOnForest(golem):
    forest[golem.center[0]][golem.center[1]] = golem.id
    forest[golem.left[0]][golem.left[1]] = golem.id
    forest[golem.right[0]][golem.right[1]] = golem.id
    forest[golem.up[0]][golem.up[1]] = golem.id
    forest[golem.down[0]][golem.down[1]] = golem.id

def moveRobot(golem):
    visited = [[0 for _ in range(C)] for _ in range(R+3)]
    # start: 골렘의 center
    q = deque()
    q.append(golem.center)

    max_row = 0
    while q:
        cx, cy = q.popleft()
        # print(f'현재 큐: {q}')
        # print(f'현재 정령 위치: {cx, cy}')
        id = forest[cx][cy]
        exitx = klist[id].center[0] + dx[klist[id].d]
        exity = klist[id].center[1] + dy[klist[id].d]
        # print(f'현재 골렘의 출구 위치: {exitx, exity}')

        # 현재 위치가 방문한 적 없으면 방문 처리
        if not visited[cx][cy]:
            visited[cx][cy] = 1
            if cx >= max_row:
                max_row = cx

            for i in range(4):
                nx = cx + dx[i]
                ny = cy + dy[i]
                # print(f'확인할 다음 위치: {nx, ny}')

                # 경계 체크
                if nx < 3 or nx > R + 2 or ny < 0 or ny > C - 1:
                    # print('Out of Bound')
                    # print('-----')
                    continue

                # 방문한 적 있거나 빈칸이면 pass
                if visited[nx][ny] or forest[nx][ny] == 0:
                    # print('방문한 적 있거나 빈칸임')
                    # print('-----')
                    continue

                # forest에서 다음으로 갈 정령의 위치가 현재 골렘의 id값과 같으면 이동
                if forest[cx][cy] == forest[nx][ny]:
                    # print('같은 골렘 내로 이동 가능')
                    q.append([nx, ny])
                    # print('-----')
                # 만약 다르면, 현재 위치가 출구이면서, 그 출구 주변에 다른 id값의 골렘이 인접해 있는지
                elif (cx == exitx and cy == exity) and forest[nx][ny] != forest[cx][cy]:
                    # print(f'출구와 인접한 골렘 발견: {forest[nx][ny]}번 골렘으로 이동')
                    q.append([nx, ny])
                    # print('-----')

    return max_row-2


# 정령 객체를 담을 배열 선언
klist = [0]
# 골렘이 출발하는 열 (c), 골렘의 출구 방향 정보 (d)
for k in range(K):
    c, d = map(int, input().split())
    golem = Golem(c, d, k+1)
    klist.append(golem)

maxrow_list =[]
#for id in range(1, 4):
for id in range(1, len(klist)):
    # print(f'{id}번째 골렘 이동')
    current_golem = klist[id]
    #printGolemStatus(klist[id])
    # print('---')

    cnt = 0
    left_trial = False
    right_trial = False
    while True:
    #while cnt<=30:
        cnt += 1

        # 동작 1: 남쪽으로 한칸 내려간다
        if current_golem.checkAround(2): # move down
            # print('아래로 이동 가능')
            current_golem.move(2)

        # 맨 아래에 도달하면 더 이상 보지 않는다.
        elif current_golem.down[0] == R+2:
            break

        # 동작 2: 서쪽 방향으로 회전하면서 내려간다
        elif current_golem.checkAround(3) and not left_trial:
            # print('왼쪽으로 회전 시도')
            current_golem.move(3)
            if current_golem.checkAround(2): # 회전 후 아래로 이동 가능
                # print('골렘 아래로 이동')
                current_golem.move(2)
                # print('출구 방향 반시계 회전')
                current_golem.rotateExitCCW()
                left_trial = False
            else:
                # print('왼쪽으로 회전 불가. 원상 복구')
                current_golem.move(1)
                left_trial = True

        # 동작 3: 동쪽 방향으로 회전하면서 내려간다
        elif current_golem.checkAround(1) and not right_trial:
            # print('오른쪽으로 회전 시도')
            current_golem.move(1)
            if current_golem.checkAround(2):
                # print('골렘 아래로 이동')
                current_golem.move(2)
                # print('출구 방향 시계 회전')
                current_golem.rotateExitCW()
                right_trial = False
            else:
                # print('오른쪽으로 회전 불가. 원상 복구')
                current_golem.move(3)
                right_trial = True

        # 더이상 이동 불가
        else:
            # print('더이상 이동 불가능')
            break


    # 이동이 끝난 후 범위 체크
    if checkInBound(current_golem):
        markOnForest(current_golem)
        #printForest()
        # 정령 이동
        maxrow = moveRobot(current_golem)
        maxrow_list.append(maxrow)

    else:
        # print('골렘이 범위를 벗어남')
        # 표시했던 모든 골렘 제거
        cleanForest()
        # print('---제거 완료---')

    # print('-----------------')

# print(maxrow_list)
print(sum(maxrow_list))