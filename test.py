import curses
<<<<<<< HEAD
import time
from curses import textpad

def main(self):
    stdscr = curses.initscr()
    curses.start_color()
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)

    y, x = stdscr.getmaxyx()
    x_center = x//2
    y_center = y//2
    half_win_height = y-3
    half_win_length = x_center -4
    stdscr.bkgd(' ',curses.color_pair(1))

    title = "Fenêtre de Titre"
    stdscr.chgat(curses.A_REVERSE)
    stdscr.addstr(0, (x_center -len(title)//2), title, curses.A_REVERSE)
    stdscr.addstr(curses.LINES -1, 0, "Type Q to quit" )

    left_window = curses.newwin(half_win_height, half_win_length, 1, 2)
    left_window.box()
    inner_left_window = left_window.subwin(half_win_height -2, half_win_length -2,2,3)
    left_window.noutrefresh()

    right_window = curses.newwin(half_win_height, half_win_length, 1, x_center +3)
    right_window.box()
    inner_right_window = right_window.subwin(half_win_height -2, half_win_length -2,2,x_center +4)
    right_window.noutrefresh()

    stdscr.refresh()

    with open("Documentation/texte_T&C.txt", "rb") as file:
        inner_left_window.addstr(1,0,"Please first scroll down the Terms and Conditions!")
        inner_left_window.addstr(2,0,"You can press any key")
        inner_left_window.refresh()
        inner_right_window.scrollok(True)
        curses.curs_set(1)
        file = file.readlines()
        inner_right_window.addstr(file[0])
        inner_right_window.refresh()
        for line in file[1:]:
            inner_right_window.scrollok(1)
            c = inner_right_window.getkey()
            inner_right_window.addstr(line)
            inner_right_window.refresh()

    inner_left_window.clear()
    inner_left_window.addstr('Fichier terminé')
    inner_left_window.keypad(True)
    y = 0
    while True:
        key = inner_left_window.getch()
        curs_y, curs_x = inner_left_window.getyx()
        if key == ord('q'):
            inner_left_window.addstr(curs_y+1,0,"Curses is about to leave")
            inner_left_window.noutrefresh()
            curses.doupdate()
            time.sleep(3)
            curses.echo()
            curses.cbreak()
            stdscr.keypad(True)
            curses.curs_set(0)
            curses.endwin()
            exit()

        elif key == ord('t'):
            inner_left_window.clear()  
            inner_left_window.addstr(curs_y-1,0,"Textpad will be displayed here\n")
            coord = ' y : {}, x : {}.'.format(curs_y, curs_x)
            inner_left_window.addstr(coord)
            editwin = inner_left_window.subwin(1 ,10, curs_y+4, 4)
            textpad.rectangle(inner_left_window, curs_y+1, 0, curs_y+3, 12)
            inner_left_window.refresh()
            box = curses.textpad.Textbox(editwin, insert_mode = True)
            contents = box.edit()
            inner_left_window.addstr(curs_y+4, 0,"Text entered in the box\n")
            inner_left_window.addstr(repr(contents))
            inner_left_window.addstr(' ')
            stdscr.refresh()
            

        elif key != ord('q'):
            inner_left_window.addstr(curs_y+1,0,"Waiting for instruction")
            inner_left_window.noutrefresh()
            curses.doupdate()
            time.sleep(1)

       
            
if __name__ == "__main__":
    curses.wrapper(main)

=======
from curses import textpad as tp
import config
import time

def main(self):
    stdscr = curses.initscr()
    stdscr.addstr(0,0, "Waiting for ending the program")
    stdscr.refresh()
    win = curses.newwin(10,10,10,20)
    win.addstr(1,1, "Test \n il s'agit d'un test plutôt long")
    win.refresh()
    time.sleep(3)

if __name__ == "__main__":
    curses.wrapper(main)
>>>>>>> d98a87a2854a09812d1bcf0b543c6aa822ddc6e9
