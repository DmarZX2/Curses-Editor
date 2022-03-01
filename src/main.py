import curses
from curses import textpad
import textwrap
from textstat import textstat
import os
from autocorrect import Speller

# ---- init ----

check = Speller(lang='en')
os.system('color')

def main(stdscr):
    # ---- init ----
    global textbox_win, text_border, text
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)
    curses.curs_set(0)
    while 1:
        try:
            stdscr.refresh()
            y, x = stdscr.getmaxyx()
            curses.curs_set(1)

            #---- Text Box and border ----
            controlwin = curses.newwin(1,x, y-1, 0)
            status = "Press Ctrl + G to exit editor"
            bartxt = f"Cant exit while editing | Status : {status}"
            controlwin.clear()
            controlwin.addstr(0, (x//2)-len(bartxt)//2, bartxt,curses.color_pair(1))
            controlwin.refresh()


            text_border = curses.newwin(y-1, x//2, 0, 0)
            text_border.box()
            text_border.addstr(0,2, "Edit:")
            text_border.refresh()
            textbox_win = curses.newwin(y-3, (x//2)-2, 1,1)
            tb = curses.textpad.Textbox(textbox_win)
            text = tb.edit()
            curses.curs_set(0)


            text_border.refresh()
            y2, x2 = text_border.getyx()
            stdscr.refresh()

            textbox_win.addstr(1,1,check(text))
            text_border.refresh()

            # ----stats windows init----
            statswin = curses.newwin((y // 2) - 1, (x - x2) // 2, 0, (x // 2))
            statswin.box()
            statswin.addstr(1,1,f"Word Count: {str(textstat.lexicon_count(text, removepunct=True))} Words")
            statswin.addstr(2,1,f"Character Count: {str(textstat.char_count(text)-1)} Characters")
            statswin.addstr(3,1,f"Reading time: {str(textstat.reading_time(text, ms_per_char=25))} Seconds")
            statswin.addstr(4,1,f"Total score: {str(textstat.text_standard(text))}")
            statswin.addstr(5,1,f"Syllables Count: {str(textstat.syllable_count(text))} Syllables")


            statswin.refresh()
            #---
            text_border.box()
            controlwin.clear()
            status = "Press any button to start"
            text_border.addstr(0,2, "Edit:")
            bartxt = f"Press q to exit | Status : {status} | Press c twice to AutoCorrect (Experimental)"
            controlwin.addstr(0, (x // 2) - len(bartxt)//2, bartxt, curses.color_pair(1))
            controlwin.refresh()

            #  text_border.refresh()




        finally:
            while 1:
                if stdscr.getkey() == 'q':
                    curses.endwin()
                    quit()
                elif stdscr.getkey() == 'c':
                    text_border.addstr(0, 2, "AutoCorrect Preview:")
                    hs = text_border.subwin(1,1)
                    hs.addstr(1,1,textwrap.fill(check(text)))
                    text_border.refresh()

                else:
                    break


if __name__ == "__main__":
    curses.wrapper(main)