##############################################################################
#  FILE: constants.py
# WRITERS: Eldan Chodorov, eldan, 201335965
#          and Keren Meron, keren.meron, 200039626
# EXERCISE: intro2cs ex12 2016-2016
# DESCRIPTION: contains constants used in clieny.py and client_connection.py
##############################################################################

CANVAS_PARAM = (500, 400, 12, 'groove', 'w') #width, height, font size,
                                             #relief, anchor
CLR_BTN_SIZE = (15, 100, 5) #button size, frame size, border width
SHP_BTN_SIZE = (5, 15, 75, 8) #button size, frame width, height, border width
SHP_BTN_PROPS = ('top', 12) #placement, font size
ERR_PARAM = (100, 'top', 45, True) #size, placement, close btn size, expand
HELP_PARAM = (100, 45, 'top', True) #label size, btn size, placement, expand
MEMBER_size = 5
BTN_FILL = 'x'
LST_FILL = 'y'
WIN_FILL = 'both'
BTN_CLICK = '<Button-1>'

NUM_ARGS = 5
RUN_ERROR = 'Check again parameters...\nPlease enter username, group name, ' \
            'host and port.'
BUFF_SIZE = 1024
MSG_DELIMITER = "\n"
MSG_JOIN = 'join'
MSG_USERS = 'users'
MSG_SHAPE = 'shape'
MSG_LEAVE = 'leave'
MSG_ERROR = 'error'
SEP1 = ';'
SEP2 = ','
MSG_JOIN = 'join'
MSG_SHAPE = 'shape'
MSG_LEAVE = 'leave'
MSG_ERROR = 'error'
MSG_USERS = 'users'
TRIANGLE = 'triangle'
RECTANGLE = 'rectangle'
HELP_TITLE = 'HELP'
OVAL = 'oval'
LINE = 'line'
SEP1 = ';'
SEP2 = ','
HELP_CLOSE = 'Got it'
HELP_MSG = 'This is a draw interface. \n You are connected to group %s. \nIn'\
           'order to draw on the screen, please select shape and color by ' \
           'clicking on relevant button. \n After selection, you must click '\
           'on screen:\n Line: Twice for line vertex. \n Rectangle: Twice ' \
           'for the diagonal in rectangle. \n Oval: Twice for rectangle ' \
           'which bounds an oval. \n Triangle: Thrice for vertexes. \nYour '\
           'drawing will have a tag in your name and will appear on all ' \
           'boards of your group members. \n You will also see on your ' \
           'board all drawings made by other group members. \n On the left ' \
           'there is a list of group members besides yourself. \n To exit ' \
           '(no reason for that) simply press the X button on the top right.'\
           ' Knock yourself out!'
DEFAULT_HOST = 'localhost'
DEFAULT_PORT = 5678
LINE_FILE = 'line.gif'
OVAL_FILE = 'oval.gif'
RECT_FILE = 'rectangle.gif'
TRIANGLE_FILE = 'triangle.gif'
COLOR1 = "black"
COLOR2 = "violet"
COLOR3 = "yellow"
COLOR4 = "green"
COLOR5 = "red"
COLOR6 = "blue"
COLOR7 = "orange"
HEADER_BG_COLOR = 'white'
HEADER_COLOR = 'blue'
DEFAULT_FONT = 'Helvetica'
COLORS_HEADER = 'colors'
COLOR_CHOICE_TITLE = 'Color: '
SHAPE_CHOICE_TITLE = 'Shape: '
CURR_CHOICES = 'Current Choices:'
TRI_MOUSE = 3
RECT_LINE_OVAL_MOUSE = 2
ERROR_CLOSE = 'OK'
RECEIVE_TIMER = 100
SELECT_RCV_TIMER = 0.01
ERR_OVERLOAD = "TOO MANY SHAPES ON SCREEN! PLEASE EXIT AND CREATE NEW " \
               "GROUP. HAVE A NICE DAY. YOUR COMPUTER WILL EXPLODE IN" \
               " 10 SECONDS."
NAME_ERR_MSG = "Name and group name must contain only english characters" \
               "and numbers, and must be no longer than 20 characters."
LEGAL_NAME = '[A-Za-z0-9_]*$'
MAXNAMELEN = 20