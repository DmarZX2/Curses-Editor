import curses
import subprocess

class tui(object):

    def __init__(self):
        pass

    def setup(self, stdscr):
        self.stdscr = stdscr
        curses.use_default_colors()
        curses.init_pair(1, curses.COLOR_WHITE, -1)
        self.maxY, self.maxX = self.stdscr.getmaxyx()
        try:
            curses.curs_set(0)
        except:
            pass
        self.win = curses.newwin(self.maxY, self.maxX, 0, 0)
        self.stdscr.nodelay(0)
        self.draw()
        while True:
            try:
                c = self.win.getch()
                ret = self.keypress(c)
                if (ret == -1):
                    return
            except KeyboardInterrupt:
                break


    def draw(self):
        self.win.erase()
        self.win = curses.newwin(self.maxY, self.maxX, 0, 0)
        self.win.box()
        self.win.refresh()


    def nano(self):
        curses.savetty()
        subprocess.run("nano")
        curses.resetty()
        curses.curs_set(0)

    def less(self):
        curses.savetty()
        subprocess.run(["less", "/etc/fstab"])
        curses.resetty()
        curses.curs_set(0)



    def keypress(self, char):
        if char == curses.KEY_EXIT or char == ord('q'):
            return -1

        if char == ord('e'):
            self.nano()
            self.draw()
            return

        if char == ord('l'):
            self.less()
            self.draw()
            return

if __name__ == '__main__':
    mytui = tui()
    curses.wrapper(mytui.setup)