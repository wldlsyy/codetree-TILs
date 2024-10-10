# 유적지 5X5 격자 형태
import copy
from collections import deque

Treasure = []
# 유물 총 7가지 종류 (1~7)

# 입력
K, M = map(int, input().split()) # K: 탐사 반복 횟수, M: 벽면에 적힌 유물 조각 개수 (새로운 조각)
for _ in range(5):
    Treasure.append(list(map(int, input().split())))

new_treasure = deque()
for t in list(map(int, input().split())): # 벽면에 적혀있는 보물
    new_treasure.append(t)

# print(new_treasure)

# 방향 배열: 북, 동, 남, 서
dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]

# 디버깅 함수
def printMap():
    for i in range(5):
        for j in range(5):
            print(Treasure[i][j], end=" ")
        print()

#printMap()
def printArray(array, n):
    for i in range(n):
        for j in range(n):
            print(array[i][j], end=" ")
        print()


# def treasureSearch():
#     # 유물 연쇄 획득

def replaceT(x, y, array, temp):
    # transposed에 회전된 영역 놓기
    for i in range(3):
        for row in array[x - 1 + i:x + i]:
            row[y - 1:y + 2] = temp[i]

    #printArray(array, 5)
    return array


def rotate(x, y, turn, array):
    #print(f'중심좌표 {x, y}, {turn}도 각도 회전 수행')
    transposed = copy.deepcopy(array) # 반환할 회전된 배열
    temp = [[0 for _ in range(3)] for _ in range(3)] # 임시 배열
    # 중심 좌표를 기준으로, 유물지도에서 회전할 영역 복사
    square = [row[y-1:y+2] for row in array[x-1:x+2]]
    # 회전할 부분이 맞는지 체크
    #printMap()
    #print('회전하기 전')
    #printArray(square, 3)

    if turn == 90: # 90도 회전
        #print('회전한 후')
        for i in range(3):
            for j in range(3):
                temp[j][2-i] = square[i][j]
        # 회전 잘 됐는지 체크
        #printArray(temp, 3)
        # transposed에 회전된 영역 놓기
        result = replaceT(x, y, transposed, temp)

    elif turn == 180: # 180도 회전
        #print('회전한 후')
        for i in range(3):
            for j in range(3):
                temp[2-i][2-j] = square[i][j]
        # 회전 잘 됐는지 체크
        #printArray(temp, 3)
        # transposed에 회전된 영역 놓기
        result = replaceT(x, y, transposed, temp)

    else: # 270도 회전
        #print('회전한 후')
        for i in range(3):
            for j in range(3):
                temp[2-j][i] = square[i][j]
        # 회전 잘 됐는지 체크
        #printArray(temp, 3)
        # transposed에 회전된 영역 놓기
        result = replaceT(x, y, transposed, temp)

    return result


def searchTreasure(start, treasure, visited):
    #print('유물 1차 획득 가치 찾기 수행')
    q, trace = deque(), deque()  # trace 안에 조각들 위치 저장
    q.append(start)
    trace.append(start)
    cnt = 1  # 시작 지점도 카운트에 포함

    while q:
        cx, cy = q.popleft()
        #print(f'현재 위치: {cx, cy}')
        visited[cx][cy] = 1

        for i in range(4):
            nx = cx + dx[i]
            ny = cy + dy[i]

            # 경계 검사
            if nx < 0 or ny < 0 or nx >= 5 or ny >= 5:
                continue
            # 이미 방문한 적 있거나 비어있으면
            if visited[nx][ny] == 1 or treasure[nx][ny] != treasure[cx][cy]:
                continue

            # 조건을 다 충족하면 다음 위치 append
            #print(f'{nx, ny}로 이동 가능')
            q.append([nx, ny])
            trace.append([nx, ny])
            visited[nx][ny] = 1
            cnt += 1

    if cnt < 3:
        cnt = 0
        #print(f'{start} 지점에서 유물 부족: {cnt}개, 유물 사라지지 않음')
    else:
        #print(f'{start} 지점에서 탐색한 유물 개수: {cnt}, 유물 사라짐')
        for x, y in trace:  # 탐색한 자리는 0으로 변경
            treasure[x][y] = 0

    #printArray(treasure, 5)

    return cnt, treasure

def startSearch(array):
    info = []
    for x in range(1, 4):  # 회전 가능한 중심 좌표만 가지고 수행
        for y in range(1, 4):
            #print(f'회전 가능한 중심: {x, y}')
            turn = [90, 180, 270]
            max_cnt = -1
            max_t = 0

            for t in turn:
                transposed = rotate(x, y, t, array)
                visited = [[0 for _ in range(5)] for _ in range(5)]
                total_cnt = 0

                for i in range(5):
                    for j in range(5):
                        start = [i, j]
                        if not visited[i][j]:
                            cnt, after_first_search = searchTreasure(start, transposed, visited)
                            total_cnt += cnt

                #print(f'{x, y} 중심에서 {t}도 회전한 결과 유물 1차 획득 가치: {total_cnt}')
                if total_cnt > max_cnt:  # 가장 큰 유물 획득 가치를 기록
                    max_cnt = total_cnt
                    max_t = t

                #print(f'-----------------{x, y} {max_t}도 회전 탐색 끝')
            info.append([max_cnt, max_t, [x, y]])

    return info

def findSearchSpace(search_list):
    result = min(
        search_list,
        key=lambda x: (-x[0], x[1], x[2][1], x[2][0])  # maxCnt를 최대화하고, 나머지는 최소화
    )
    return result[0], result[1], result[2][0], result[2][1]

def fillTreasureMap(board):
    # 열이 작고 행이 큰 우선순위로 채우기
    for i in range(5):
        for j in reversed(range(5)):
            if board[j][i] == 0:
                board[j][i] = new_treasure.popleft()
    return board

# 메인
# 최대 K번의 탐사과정을 거칩니다.
current_treasure = Treasure  # 첫 탐사는 원본 Treasure를 사용
for k in range(K):
    #print('---------------------------')
    # print(f'{k+1}번째 턴')
    maxScore = 0
    search_list = startSearch(current_treasure) # 유물가치, 회전 각도, 중심좌표 담을 배열 반환
    # print(search_list)
    first_search_cnt, rotate_num, center_x, center_y = findSearchSpace(search_list)

    # 회전을 통해 더 이상 유물을 획득할 수 없는 경우 탐사를 종료합니다.
    if first_search_cnt == 0:
        break

    # print(f'최종---{center_x, center_y} 중심 {rotate_num}도 회전 진행')
    transposed_treasure = rotate(center_x, center_y, rotate_num, current_treasure)
    total_score = 0

    while True:
        visited = [[0 for _ in range(5)] for _ in range(5)]
        new_score = 0
        for i in range(5):
            for j in range(5):
                start = [i, j]
                if not visited[i][j]:
                    cnt, after_first_search = searchTreasure(start, transposed_treasure, visited)
                    new_score += cnt
                    transposed_treasure = after_first_search

        total_score += new_score  # 전체 점수에 이번 회차 점수를 더함
        # print(f"이번 탐색에서 획득한 점수: {new_score}, 누적 점수: {total_score}")
        #printArray(transposed_treasure, 5)

        # 빈칸을 채우는 로직을 실행
        # print(new_treasure)
        transposed_treasure = fillTreasureMap(transposed_treasure)
        # print(new_treasure)
        #printArray(transposed_treasure, 5)

        # 더 이상 유물을 찾을 수 없는 경우 반복 종료
        if new_score == 0:
            # print('cannot find more')
            break
    # 이번 탐사에서 최종 탐사된 배열을 다음 탐사에서 사용
    current_treasure = transposed_treasure
    print(total_score, end=" ")
    #print('---------------------------')