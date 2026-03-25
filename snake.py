#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
贪吃蛇游戏 - 使用 Python curses 库实现
控制方式：WASD 或方向键移动蛇
游戏规则：吃到食物得分，碰到墙壁或自己身体游戏结束
"""

import curses
import random
import time


def main(stdscr):
    """主游戏函数"""
    # 初始化 curses
    curses.curs_set(0)  # 隐藏光标
    stdscr.nodelay(1)   # 非阻塞输入
    stdscr.timeout(100) # 刷新间隔（毫秒）

    # 获取窗口大小
    sh, sw = stdscr.getmaxyx()

    # 创建游戏窗口
    win = curses.newwin(sh, sw, 0, 0)
    win.keypad(1)   # 启用键盘输入
    win.timeout(100) # 刷新间隔

    # 游戏主循环
    while True:
        # 初始化蛇的位置（屏幕中央）
        snake_y = sh // 2
        snake_x = sw // 4
        snake = [
            [snake_y, snake_x],
            [snake_y, snake_x - 1],
            [snake_y, snake_x - 2]
        ]

        # 初始化食物位置
        food = [sh // 2, sw // 2]
        win.addch(food[0], food[1], 'O')  # 用 'O' 表示食物

        # 初始移动方向：向右
        key = curses.KEY_RIGHT

        # 游戏分数
        score = 0

        # 游戏进行中的标志
        game_over = False

        # 游戏循环
        while not game_over:
            # 显示分数
            win.addstr(0, 2, f'分数: {score} ')
            win.addstr(0, sw // 2 - 10, '贪吃蛇 - WASD/方向键控制')

            # 获取下一个按键
            next_key = win.getch()

            # 如果有按键输入，更新方向
            # 防止蛇反向移动（不能直接掉头）
            if next_key != -1:
                if next_key == curses.KEY_UP or next_key == ord('w') or next_key == ord('W'):
                    if key != curses.KEY_DOWN:
                        key = curses.KEY_UP
                elif next_key == curses.KEY_DOWN or next_key == ord('s') or next_key == ord('S'):
                    if key != curses.KEY_UP:
                        key = curses.KEY_DOWN
                elif next_key == curses.KEY_LEFT or next_key == ord('a') or next_key == ord('A'):
                    if key != curses.KEY_RIGHT:
                        key = curses.KEY_LEFT
                elif next_key == curses.KEY_RIGHT or next_key == ord('d') or next_key == ord('D'):
                    if key != curses.KEY_LEFT:
                        key = curses.KEY_RIGHT

            # 计算蛇头的新位置
            head = snake[0].copy()

            if key == curses.KEY_UP:
                head[0] -= 1
            elif key == curses.KEY_DOWN:
                head[0] += 1
            elif key == curses.KEY_LEFT:
                head[1] -= 1
            elif key == curses.KEY_RIGHT:
                head[1] += 1

            # 检查是否撞墙
            if head[0] <= 0 or head[0] >= sh - 1:
                game_over = True
            elif head[1] <= 0 or head[1] >= sw - 1:
                game_over = True

            # 检查是否撞到自己
            if head in snake:
                game_over = True

            if game_over:
                break

            # 将新头部插入蛇身
            snake.insert(0, head)

            # 检查是否吃到食物
            if snake[0] == food:
                score += 1  # 增加分数

                # 生成新的食物位置（不能在蛇身上）
                while True:
                    food = [
                        random.randint(2, sh - 2),
                        random.randint(2, sw - 2)
                    ]
                    if food not in snake:
                        break

                win.addch(food[0], food[1], 'O')
            else:
                # 没吃到食物，移除蛇尾
                tail = snake.pop()
                win.addch(tail[0], tail[1], ' ')

            # 绘制蛇头
            win.addch(snake[0][0], snake[0][1], '#')

            # 绘制边框
            win.border(0)

            win.refresh()

        # 游戏结束处理
        win.clear()
        win.border(0)

        # 显示游戏结束信息
        game_over_msg = '游戏结束!'
        final_score_msg = f'最终分数: {score}'
        restart_msg = '按 空格键 重新开始，按 Q 退出'

        win.addstr(sh // 2 - 2, (sw - len(game_over_msg) * 2) // 2, game_over_msg)
        win.addstr(sh // 2, (sw - len(final_score_msg) * 2) // 2, final_score_msg)
        win.addstr(sh // 2 + 2, (sw - len(restart_msg) * 2) // 2, restart_msg)

        win.nodelay(0)  # 阻塞等待输入
        win.refresh()

        # 等待玩家选择重新开始或退出
        while True:
            retry_key = win.getch()

            # 空格键重新开始
            if retry_key == ord(' '):
                win.clear()
                win.nodelay(1)
                win.timeout(100)
                break
            # Q 键退出游戏
            elif retry_key == ord('q') or retry_key == ord('Q'):
                return


if __name__ == '__main__':
    # 启动游戏
    curses.wrapper(main)
