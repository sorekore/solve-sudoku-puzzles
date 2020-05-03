#-------------------------------------------------------------------------------
# Name:        sudoku_main.py
# Purpose:
#
# Author:      sorekore
#
# Created:     25/04/2020
# Copyright:   sorekore
# Licence:
#-------------------------------------------------------------------------------

import csv

# Windows用
file_path = 'C:\\Users\\mytoshiba\\Desktop\\git\\solve-sudoku-puzzles\\'
# Mac用
# file_path = '/home/jovyan/work/solve-sudoku-puzzles/'
# ファイル名
file_name = 'mondai.csv'

temp_table_data = [[[] for i in range(9)] for j in range(9)]
update_flg = 1


# 問題をcsv形式で取り込む
def import_csv(file_path, file_name):
    csv_file = open(file_path + file_name)
    csv_reader = csv.reader(csv_file)
    table_data = list(csv_reader)

    # 文字から数字に変換する
    for i in range(len(table_data)):
        for j in range(len(table_data[i])):
            if table_data[i][j] != '':
                table_data[i][j]= int(table_data[i][j])

    return table_data


# 現在のマスの入力状態を9*9で出力
def table_print(table_data):
    row_num = 0
    print('┏━┳━┳━┳━┳━┳━┳━┳━┳━┓')

    # 1行ずつ読み込み
    for row_data in table_data:
        # 列をリセット
        row = ''

        # 左から1マズずつ出力
        for num in row_data:
            row += '┃'
            if num == '':
                row += ' '
            else:
                row += str(num)
        row += '┃'
        print(row)

        row_num += 1

        # 行と行の間の罫線を出力
        if row_num == 9:
            print('┗━┻━┻━┻━┻━┻━┻━┻━┻━┛')
        else:
            print('┣━╋━╋━╋━╋━╋━╋━╋━╋━┫')


# 空白のマスに入る数字の候補を探す。
def table_space_check(table_data):
    temp_table_data = [[[] for i in range(9)] for j in range(9)]

    for row_num, row in enumerate(table_data):
        for col_num, box in enumerate(row):
            if box == '':
                temp_table_input(row_num, col_num)


# 数字の候補を探す処理。
def temp_table_input(row_num, col_num):

    # 該当のマスに1から9まで入力可能かをチェック
    for i in range(1,10):
        hantei_flg = 0

        # 行のチェック
        if i not in table_data[row_num]:
            # 列のチェック
            for j in range(0,9):
                if table_data[j][col_num] != i:
                    pass
                else:
                    hantei_flg = 1
                    break
            # 3*3のマスのチェック
            else:
                start_row = row_num //3 * 3
                start_col = col_num //3 * 3

                for k in range(start_row, start_row+3):
                    for m in range(start_col, start_col+3):
                        if table_data[k][m] != i:
                            pass
                        else:
                            hantei_flg = 1
                            break
                    else:
                        continue
                    break
        else:
            hantei_flg = 1

        if hantei_flg == 0:
            temp_table_data[row_num][col_num].append(i)


# 入力できる数字を探す(1)
def table_input(update_flg):
    update_flg= 0

    # 1から9まで入力可能かをチェック
    for i in range(1,10):

        # 各行に対して、入力可能なマスが1か所でないかを確認
        for j in range(0,9):
            hantei_flg = 0
            for k in range(0,9):
                if i in temp_table_data[j][k]:
                    temp_num = i
                    temp_num_place = [j,k]
                    hantei_flg += 1

                if hantei_flg >= 2:
                    break

            else:
                if hantei_flg == 1:
                    table_data[temp_num_place[0]][temp_num_place[1]] = temp_num
                    update_flg = 1

        # 列
        for j in range(0,9):
            hantei_flg = 0
            for k in range(0,9):
                if i in temp_table_data[k][j]:
                    temp_num = i
                    temp_num_place = [k,j]
                    hantei_flg += 1

                if hantei_flg >= 2:
                    break

            else:
                if hantei_flg == 1:
                    table_data[temp_num_place[0]][temp_num_place[1]] = temp_num
                    update_flg = 1

        # 3*3のマスのチェック
        for j in range(0,8,3):
            for k in range(0,8,3):
                hantei_flg = 0
                for m in range(0,3):
                    for n in range(0,3):
                        if i in temp_table_data[j+m][k+n]:
                            temp_num = i
                            temp_num_place = [j+m,k+n]
                            hantei_flg += 1

                        if hantei_flg >= 2:
                            break

                    if hantei_flg >= 2:
                        break

                else:
                    if hantei_flg == 1:
                        table_data[temp_num_place[0]][temp_num_place[1]] = temp_num
                        update_flg = 1

    return update_flg

# 入力できる数字を探す(2)
def table_input2(update_flg):

    # 入力候補が一つしかないマスを入力する。
    for i in range(0,9):
        for j in range(0,9):
            if len(temp_table_data[i][j]) == 1:
                table_data[i][j] = temp_table_data[i][j][0]

    return update_flg


# 入力候補の数字を減らす(1)
def remove_temp_table_data():

    # 入力候補が二つのマスのペアを探す。
    # 行に対して確認
    for i in range(0,9):
        for j in range(0,9):
            # 入力候補が二つのマスか。ペアが存在するか。
            if len(temp_table_data[i][j]) == 2 and \
                temp_table_data[i].count(temp_table_data[i][j]) == 2:
                    # 他のマスの入力候補から削除する。
                    for k in range(0,9):
                        if temp_table_data[i][k] == temp_table_data[i][j]:
                            pass
                        else:
                            temp_table_data[i][k] = list(set(temp_table_data[i][k]) - set(temp_table_data[i][j]))


    # 入力候補が二つのマスのペアを探す。
    # 列に対して確認
    for i in range(0,9):
        # 作業用リストに列を格納
        work_col = []
        for j in range(0,9):
            work_col.append(temp_table_data[j][i])


        for j in range(0,9):
            # 入力候補が二つのマスか。ペアが存在するか。
            if len(work_col[j]) == 2 and \
                work_col.count(work_col[j]) == 2:
                    # 他のマスの入力候補から削除する。
                    for k in range(0,9):
                        if work_col[k] == work_col[j]:
                            pass
                        else:
                            temp_table_data[k][i] = list(set(work_col[k]) - set(work_col[j]))


################################################################################

# 前処理
table_data = import_csv(file_path,file_name)
table_print(table_data)


# チェック、入力
while update_flg == 1:
    temp_table_data = [[[] for i in range(9)] for j in range(9)]
    table_space_check(table_data)
    remove_temp_table_data()
    print(temp_table_data)
    update_flg = table_input(update_flg)
    update_flg = table_input2(update_flg)
    table_print(table_data)

# 完成 or 未完成の判定
for row in table_data:
    for box in row:
        if box == '':
            print('Oh no, unfinished...')
            break
        else:
            pass
    else:
        continue
    break
else:
    print('Finish!!')
