#!/usr/bin/env python

from img2ascii import Img2ascii
import curses
import os


class Display:
    def __init__(self, rows, columns):
        self._show_width = int(columns)
        self._show_height = int(rows)//5*4
        self.show_win = curses.newwin(self._show_height, self._show_width, 0, 0)
        # why calling box will crash python on Mac?
        # self.show_win.box(0, 0)
        self.show_win.refresh()

        self.cmd_line = curses.newwin(1, self._show_width, self._show_height, 0)
        self.cmd_line.bkgd(' ', curses.color_pair(8))
        self.cmd_line.addstr('q to quit; o to open graph; +/- to resize; c to \
clean; d to dump; hjkl/arrow keys to move around; r to move back')
        self.cmd_line.refresh()

        self.cmd_win = curses.newwin(int(rows)-self._show_height-1,
                                     self._show_width, self._show_height+1, 0)
        self.cmd_win.keypad(1)
        self.cmd_win.scrollok(True)
        self.cmd_win.refresh()

        self.pad = curses.newpad(1200, 1920)
        self.pad.refresh(0, 0, 1, 1, self._show_height-2, self._show_width-2)
        self._y = 0
        self._x = 0

        self._graph = None
        # number as precent
        self._ratio = 100

    def _update_pad(self, key=0):
        if key == 1 and self._y > 0:
            self._y -= 1
        elif key == 2 and self._y < 1199:
            self._y += 1
        elif key == 3 and self._x > 0:
            self._x -= 1
        elif key == 4 and self._x < 1919:
            self._x += 1

        self.pad.refresh(self._y, self._x, 1, 1, self._show_height-2,
                         self._show_width-2)

    def _clear_pad(self):
        self.pad.erase()
        self.pad.refresh(0, 0, 1, 1, self._show_height-2, self._show_width-2)

    def _update_cmd(self):
        self.cmd_win.refresh()

    def _draw_ascii(self):
        if self._graph is None:
            return
        self._clear_pad()
        for line in self._graph.get_data(self._ratio/100):
            self.pad.addstr(line)
            self.pad.addstr("\n")
        self._update_pad()
        self.cmd_win.addstr("zoom to %d%%\n" % self._ratio)

    def _input_file(self):
        self.cmd_win.addstr('input image file name: ')
        curses.echo()
        self._file_name = self.cmd_win.getstr()
        self._update_cmd()
        curses.noecho()
        try:
            self._graph = Img2ascii(self._file_name)
            self._ratio = 100
        except Exception:
            self._graph = None

        self._draw_ascii()

    def _dump_file(self):
        if self._graph is None:
            return
        with open(self._file_name.decode('utf-8') + '.txt', 'w') as f:
            for line in self._graph.get_data(self._ratio/100):
                print(line, file=f)
            self.cmd_win.addstr('dumped ascii file as ' + f.name + '\n')
            self._update_cmd()

    def _update_size(self):
        rows, columns = os.popen('stty size', 'r').read().split()
        self._show_width = int(columns)
        self._show_height = int(rows)//5*4

        self.show_win.resize(self._show_height, self._show_width)
        self.show_win.mvwin(0, 0)
        self.show_win.refresh()
        self.cmd_line.resize(1, self._show_width)
        self.cmd_line.mvwin(self._show_height, 0)
        self.cmd_line.refresh()
        self.cmd_win.resize(int(rows)-self._show_height-1, self._show_width)
        self.cmd_win.mvwin(self._show_height+1, 0)
        self.cmd_win.refresh()

        self._draw_ascii()

    def main_loop(self):
        while True:
            c = self.cmd_win.getch()
            if c == ord('q'):
                break
            elif c == ord('o'):
                self._input_file()
            elif c == ord('c'):
                self._graph = None
                self._clear_pad()
            elif c == ord('r'):
                self._x = self._y = 0
                self._update_pad()
            elif c == ord('+'):
                if self._ratio < 10:
                    self._ratio += 1
                elif self._ratio < 200:
                    self._ratio += 10
                self._draw_ascii()
            elif c == ord('-'):
                if self._ratio > 1 and self._ratio <= 10:
                    self._ratio -= 1
                elif self._ratio > 10:
                    self._ratio -= 10
                self._draw_ascii()
            elif c == curses.KEY_UP or c == ord('k'):
                self._update_pad(1)
            elif c == curses.KEY_DOWN or c == ord('j'):
                self._update_pad(2)
            elif c == curses.KEY_LEFT or c == ord('h'):
                self._update_pad(3)
            elif c == curses.KEY_RIGHT or c == ord('l'):
                self._update_pad(4)
            elif c == ord('d'):
                self._dump_file()
            elif c == curses.KEY_RESIZE:
                self._update_size()


def init_settings():
    curses.curs_set(0)
    curses.use_default_colors()
    for i in range(curses.COLORS):
        curses.init_pair(i, i, -1)
    curses.init_pair(8, curses.COLOR_WHITE, curses.COLOR_BLUE)


def main(stdscr):
    init_settings()
    rows, columns = os.popen('stty size', 'r').read().split()

    display = Display(rows, columns)
    display.main_loop()


if __name__ == '__main__':
    curses.wrapper(main)
