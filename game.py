from graphics import *
from random import randint, uniform
import time

# collector used for managing windows
wins = []

# this custom class inheriting from Graphwin is to provide an easy way to create buttons
class ButtonWin(GraphWin):
    def __init__(self, *args, **kwargs):
        self.buttons = {}
        super().__init__(*args, **kwargs)

    # overrides graphwin method to remove key delays
    def getKey(self):
        self.lastKey = ""
        while self.lastKey == "":
            self.update()

        key = self.lastKey
        self.lastKey = ""
        return key

    def createtxt(self, pt, text, color="white", size=15):
        t = Text(pt, text)
        t.setFill(color)
        t.setSize(size)
        t.setFace("courier")
        t.setStyle("bold")
        t.draw(self)

    def createbut(self, p1: Point, p2: Point, action, text) -> Rectangle:
        self.buttons[(p1, p2)] = action
        rect = Rectangle(p1, p2)
        rect.setOutline("#F7F9F9")
        rect.setFill("#707B7C")
        rect.draw(self)

        if text:
            self.createtxt(Point((p1.x + p2.x) / 2, (p1.y + p2.y) / 2), text)

        return rect

    def checkButtonClick(self, click):
        for k, v in self.buttons.items():
            if k[0].x < click.x < k[1].x and k[0].y < click.y < k[1].y:
                globals()[v]()

# a manager class to handle a game
class GameManager:
    def __init__(self, notescount: int = 30):
        self.starttime = None
        self.notescount = notescount

    def genBoard(self, win):
        def buildRect(r=0, c=0):
            x = c * 75
            y = 600 - r * 150
            rect = Rectangle(Point(x, y), Point(x + 75, y - 150))
            rect.setFill("white")
            rect.setOutline("#bfbfbf")
            rect.draw(win)
            return rect

        self.board = [[buildRect(r, c) for c in range(4)] for r in range(4)]

    def updateBoard(self):
        [[ce.setFill("#4f4f4f") if ci+1 == self.notes[ri] else ce.setFill("white") for ci, ce in enumerate(re)] for ri, re in enumerate(self.board)]

    def genNotes(self):
        self.notes = [randint(1, 4) for _ in range(self.notescount)] + [5 for _ in range(4)]

    def getnote(self, key) -> bool:
        if key == self.notes[0]:
            self.notes.pop(0)
            return True
        else:
            self.board[0][key-1].setFill("red")
            time.sleep(0.2)
            self.board[0][key-1].setFill("white")
            return False

    def isEnd(self) -> bool:
        return len(self.notes) == 4

    def startTime(self):
        if not self.starttime:
            self.starttime = time.time()
        return self.starttime
    def endTime(self):
        self.endtime = time.time()
        return self.endtime

    @property
    def calTime(self) -> float:
        return self.endtime - self.starttime


# below are the functions as button callables
def play():
    for win in wins:
        win.close()
    win_game = ButtonWin(title="GAME ON", width=300, height=600)
    wins.append(win_game)

    gm = GameManager(notescount=20)
    gm.genNotes()
    gm.genBoard(win_game)
    gm.updateBoard()

    for i in range(1, 5):
        win_game.createtxt(Point(75*i-35, 525), f"{i}", size=25)

    while not gm.isEnd():
        k = win_game.getKey()
        gm.startTime()

        if k.isdigit() and 1 <= int(k) <= 4 and gm.getnote(int(k)):
            gm.updateBoard()

    gm.endTime()
    win_game.createtxt(
        Point(150, 260),
        "You have completed the game\n Your time is:\n\n\n\n\nNice Work! Try again?",
        color="black", size=12)
    win_game.createtxt(Point(150, 265), f"{gm.calTime:.2f}", "black", 25)
    win_game.createbut(Point(50, 400), Point(250, 450), action="play", text="Try Again")
    win_game.createbut(Point(50, 480), Point(250, 530), action="quit", text="Quit Game")

    while True:
        try:
            win_game.checkButtonClick(win_game.getMouse())
        except GraphicsError:
            quit()

def help():
    try:
        win_help = ButtonWin(title="Help", width=320, height=280)
        wins.append(win_help)
        win_help.setBackground("#FDFEFE")
        buildBG(win_help, 20, (-40, 360), (-40, 320))
        win_help.createtxt(Point(130, 150), """
        Piano key is a game of speed
        Simply Press 1, 2, 3, 4 on keyboard
        Play the notes as fast as possible!
        Time starts when you hit the first key!
        The faster you complete the game
        the higher score you will get!

        Click window to go back:
        """, color='black', size=10)

        win_help.getMouse()
        wins.remove(win_help)
        win_help.close()

    except GraphicsError:
        pass

def quit():
    sys.exit()

# purely for aesthetics
def buildBG(win, count: int, xrange: tuple, yrange: tuple):
    for _ in range(count):
        x = randint(xrange[0], xrange[1])
        y = randint(yrange[0], yrange[1])
        size = uniform(0.8, 1.2)
        rect = Rectangle(Point(x, y), Point(x + int(75 * size), y + int(150 * size)))

        # kinda proud of this random color generator
        color = str(hex(randint(210, 240)))[2:]
        rect.setFill(f"#{color}{color}{color}")
        rect.setOutline(f"#{color}{color}{color}")
        rect.draw(win)

def main():
    win_start = ButtonWin(title="Piano Key", width=300, height=600)
    wins.append(win_start)
    win_start.setBackground("#FDFEFE")
    buildBG(win_start, 30, xrange=(-20, 320), yrange=(-20, 620))
    win_start.createtxt(Point(150, 200), "P I A N O\nK E Y", color="black", size=36)

    win_start.createbut(Point(50, 380), Point(250, 430), action="play", text="Play")
    win_start.createbut(Point(50, 450), Point(250, 500), action="help", text="Help")
    win_start.createbut(Point(50, 520), Point(250, 570), action="quit", text="Exit Game")

    while True:
        try:
            win_start.checkButtonClick(win_start.getMouse())
        except GraphicsError:
            quit()

if __name__ == '__main__':
    main()