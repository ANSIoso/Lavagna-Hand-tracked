import cv2
import copy
import numpy as np

from model.MenuOptions import MenuOptions


class Board:
    # class responsible for register the drawings

    def __init__(self):
        # the drawing will be stored as a canvas
        self.canvas = None
        self.mode = "draw"

        # it will be possible to go back to old instances of the drawing
        # (a new instance of the drawing will be created each time that a line is "closed")
        self.old_me = []
        self.new_thing = False

        # each line of the drawing will be composed by a series of points connected by lines
        self.x1, self.y1 = 0, 0
        self.x2, self.y2 = 0, 0

        # it is possible modify dimension of the lines and color of the modifying this fields
        self.color = MenuOptions.white[1]
        self.dimension = 20

    def init_board(self, img):
        # the dimensions of the canvas will be set as the dimension of the image where draw on
        if self.canvas is not None:
            return

        self.canvas = np.zeros_like(img)

        # a first instance of the drawing is added to the story
        self.old_me.append(copy.deepcopy(self.canvas))

    def finger_on_board(self, pos_x, pos_y):
        # method that is used to register a new position of the finger
        # on the board to continue or start a line

        if self.canvas is None:
            return False

        # each time that this method is called means that there is new things to register
        self.new_thing = True

        self.x2 = pos_x
        self.y2 = pos_y

        # if the last position is (0,0) means that a new line is created
        # so the old and the actual point will be the same
        if self.x1 == 0 and self.y1 == 0:
            self.x1, self.y1 = self.x2, self.y2
            return True

        # depending on the mode:
        # - draw (a line will be written on the canvas from the last position registered to the actual)
        # - delete (the content on the canvas at the actual position of the finger will be deleted)
        if self.mode == "draw":
            cv2.line(self.canvas, (self.x1, self.y1), (self.x2, self.y2), self.color, self.dimension)
        else:
            cv2.circle(self.canvas, (self.x1, self.y1), self.dimension, (0, 0, 0), -1)

        # the actual point will be registered as next old point
        self.x1, self.y1 = self.x2, self.y2
        return True

    def finger_off_board(self):
        # calling this method the old position of the finger will be retested to zero

        self.x1, self.y1 = 0, 0

        if self.canvas is None:
            return

        # if new things are existing this stance of the drawing will be added the history
        # (the stance is saved so is set that there aren't new things)
        if self.new_thing:
            self.old_me.append(copy.deepcopy(self.canvas))
            self.new_thing = False

    def undo(self):
        # method used to load old versions of the drawing
        # an old version of the drawing can be loaded only if there is an older version of it in the story
        if len(self.old_me) <= 1:
            return

        # the actual version of the drawing is deleted
        self.old_me.pop()
        self.canvas = None

        # the old version of the drawing is loaded as actual
        self.canvas = copy.deepcopy(self.old_me[-1])

    def change_mode(self):
        # method used to switch from drawing to deleting in the canvas

        if self.mode == "draw":
            self.mode = "delete"
        else:
            self.mode = "draw"
