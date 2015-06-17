#!/usr/bin/env python

from img2ascii import Img2ascii
import curses
import os


class Display:
    def __init__(self, rows, columns):
        self.show_width = int(columns)
        self.show_height = int(rows)//5*4
        self.show_win = curses.newwin(self.show_height, self.show_width, 0, 0)
        self.show_win.box(0, 0)
        self.show_win.refresh()

        self.cmd_line = curses.newwin(1, self.show_width, self.show_height, 0)
        self.cmd_line.bkgd(' ', curses.color_pair(8))
        self.cmd_line.addstr('q for quit; o to input graph; +/- to resize graph\
; r to clean')
        self.cmd_line.refresh()

        self.cmd_win = curses.newwin(int(rows)-self.show_height-1,
                                     self.show_width, self.show_height+1, 0)
        self.cmd_win.keypad(1)
        self.cmd_win.scrollok(True)
        self.cmd_win.refresh()

        self.pad = curses.newpad(1200, 1920)
        self.pad.refresh(0, 0, 1, 1, self.show_height-2, self.show_width-2)

        self.graph = None

    def update_pad(self, key=0):
        self.pad.refresh(0, 0, 1, 1, self.show_height-2, self.show_width-2)

    def clear_pad(self):
        self.pad.erase()
        self.pad.refresh(0, 0, 1, 1, self.show_height-2, self.show_width-2)

    def getch(self):
        return self.cmd_win.getch()

    def _update_cmd(self):
        self.cmd_win.refresh()

    def draw_ascii(self, ratio=1.0):
        if self.graph is None:
            return
        self.clear_pad()
        for line in self.graph.get_data(ratio):
            self.pad.addstr(line)
            self.pad.addstr("\n")
        self.update_pad()
        self.ratio = ratio

    def input_file(self):
        self.cmd_win.addstr('input image file name: ')
        curses.echo()
        name = self.cmd_win.getstr()
        self._update_cmd()
        curses.noecho()
        try:
            self.graph = Img2ascii(name)
        except Exception:
            self.graph = None

        self.draw_ascii()


def init_settings():
    curses.curs_set(0)
    curses.use_default_colors()
    for i in range(curses.COLORS):
        curses.init_pair(i, i, -1)
    curses.init_pair(8, curses.COLOR_WHITE, curses.COLOR_BLUE)


def main_loop(display):
    while True:
        c = display.getch()
        if c == ord('q'):
            break
        elif c == ord('o'):
            display.input_file()
        elif c == ord('r'):
            display.clear_pad()
        elif c == ord('+'):
            display.ratio += 0.1
            display.draw_ascii(display.ratio)
        elif c == ord('-'):
            display.ratio -= 0.1
            display.draw_ascii(display.ratio)
        elif c == curses.KEY_UP:
            display.update_pad(c)
        elif c == curses.KEY_DOWN:
            display.update_pad(c)
        elif c == curses.KEY_LEFT:
            display.update_pad(c)
        elif c == curses.KEY_RIGHT:
            display.update_pad(c)


def main(stdscr):
    init_settings()
    rows, columns = os.popen('stty size', 'r').read().split()

    display = Display(rows, columns)

    main_loop(display)


if __name__ == '__main__':
    curses.wrapper(main)
