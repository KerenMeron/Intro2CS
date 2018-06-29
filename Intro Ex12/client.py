################################################################
# FILE: client.py
# WRITERS: Eldan Chodorov, eldan, 201335965
#          and Keren Meron, keren.meron, 200039626
# EXERCISE: intro2cs ex12 2016-2016
# DESCRIPTION: runs a GUI which user can draw on.
################################################################

import tkinter as tki
import client_connection
from constants import *
import sys, re

class Interface:
    '''This class holds all information for the GUI Object.'''

    def __init__(self, parent, client_name, client_group, host, port):
        '''
        Initializes all of the containers needed for this class to work.
        Creates gui with all buttons, labels etc, creates client, and handles
        drawings on screen. Parameters: parent(tki), client_name(str),
        client_group(str), host(int), port(int) - to connect to.
        '''

        self.__parent = parent
        self.__frame1 = ""
        self.__name = client_name
        self.__group = client_group

        self.__image_1 = tki.PhotoImage(file=LINE_FILE)
        self.__image_2 = tki.PhotoImage(file=OVAL_FILE)
        self.__image_3 = tki.PhotoImage(file=RECT_FILE)
        self.__image_4 = tki.PhotoImage(file=TRIANGLE_FILE)
        self.__image_list = [self.__image_1, self.__image_2, self.__image_3,
                             self.__image_4]
        self.__canvas = tki.Canvas(self.__parent, bg=HEADER_BG_COLOR,
                            width=CANVAS_PARAM[0], height=CANVAS_PARAM[1])
        self.__colors = [COLOR1, COLOR2, COLOR3,COLOR4,COLOR5, COLOR6, COLOR7]
        self.__shapes = [LINE, OVAL, RECTANGLE, TRIANGLE]
        self.__current_color = COLOR1
        self.__current_shape = LINE
        self.__shape_text = tki.StringVar()
        self.__shape_text.set(SHAPE_CHOICE_TITLE + self.__current_shape)
        self.__color_text = tki.StringVar()
        self.__color_text.set(COLOR_CHOICE_TITLE + self.__current_color)

        self.__click_count = 0
        self.__listbox = ""
        self.__help_frame = ""
        self.__mouse_coords = []
        self.__group_members = [""]
        self.__group_members_text = tki.StringVar()
        self.__members_label = None
        self.__client = client_connection.Client(host, port, client_name,
                                                 client_group)
        self.receive_info()
        self.init_design()
        self.__parent.protocol('WM_DELETE_WINDOW', self.leave)


    def __set_color_func(self, color):
        '''Returns a function that sets the curr color to param color(str).'''

        def set_color():
            self.__color_text.set(COLOR_CHOICE_TITLE + color)
            self.__current_color = color
        return set_color

    def __set_shape_func(self, shape):
        '''Returns a function that sets current shape to param shape(str).'''

        def set_current_shape():
            self.__shape_text.set(SHAPE_CHOICE_TITLE + shape)
            self.__current_shape = shape
        return set_current_shape

    def create_color_buttons(self):
        '''Creates color buttons, which change the current color saved.'''

        group_color = tki.LabelFrame(self.__parent, text=COLORS_HEADER,
                                padx=CLR_BTN_SIZE[0], pady=CLR_BTN_SIZE[0])
        group_color.pack(padx=CLR_BTN_SIZE[1], pady=CLR_BTN_SIZE[0],
                                                        side=tki.BOTTOM)
        for color in self.__colors:
            color_Buttons = tki.Button(group_color, bg=color,
                                padx=CLR_BTN_SIZE[0], pady=CLR_BTN_SIZE[0],
                                borderwidth=CLR_BTN_SIZE[2],
                                command=self.__set_color_func(color))
            color_Buttons.pack(side=tki.LEFT)

    def create_shape_buttons(self):
        '''Creates shape buttons which change the current shape saved.'''

        group_shape = tki.LabelFrame(self.__parent, text=MSG_SHAPE,
                                padx=SHP_BTN_SIZE[0], pady=SHP_BTN_SIZE[0])
        group_shape.pack(padx=SHP_BTN_SIZE[1], pady=SHP_BTN_SIZE[2],
                                                            side=tki.RIGHT)
        for i, shape in enumerate(self.__shapes):
            image_shape = self.__image_list[i]
            shape_buttons = tki.Button(group_shape, text=shape, image=
                    image_shape, compound =SHP_BTN_PROPS[0], borderwidth=
                    SHP_BTN_SIZE[3], font=(DEFAULT_FONT, SHP_BTN_PROPS[1]),
                    command=self.__set_shape_func(shape))
            shape_buttons.pack(fill = BTN_FILL)

    def create_member_List(self):
        '''Creates member list which will show each user's name in group.'''

        group_members = tki.LabelFrame(self.__parent, text=self.__group,
                                        padx=MEMBER_size, pady=MEMBER_size)
        group_members.pack(fill=LST_FILL, side=tki.LEFT)
        scrollbar = tki.Scrollbar(self.__parent)
        scrollbar.pack(side=tki.LEFT, fill=LST_FILL)
        self.__listbox = tki.Listbox(group_members,
                                            yscrollcommand=scrollbar.set)
        self.__listbox.pack(side=tki.LEFT, fill=LST_FILL)
        scrollbar.config(command=self.__listbox.yview)
        self.__members_label = self.__listbox


    def shows_current_choices(self):
        '''Creates frame on screen which shows the current shape and color.'''

        current_choices = tki.LabelFrame(self.__parent, text=CURR_CHOICES)
        current_choices.pack(fill = BTN_FILL,side = tki.TOP)
        current_color = tki.Label(current_choices, textvariable=
                                self.__color_text, anchor = CANVAS_PARAM[4])
        current_shape = tki.Label(current_choices, textvariable=
                                self.__shape_text ,anchor = CANVAS_PARAM[4])
        current_color.pack(side = tki.TOP, fill = BTN_FILL)
        current_shape.pack(side = tki.TOP, fill = BTN_FILL)


    def help_func(self):
        '''Creates a help button on screen which displays a help message.'''

        self.__help_frame = tki.Toplevel()
        self.__help_frame.wm_title(HELP_TITLE)
        help_label = tki.Label(self.__help_frame, text=HELP_MSG %self.__group)
        help_label.pack(side=HELP_PARAM[2], fill=WIN_FILL, expand=
                    HELP_PARAM[3], padx=HELP_PARAM[0], pady=HELP_PARAM[0])
        button = tki.Button(self.__help_frame, text=HELP_CLOSE, padx=
                            HELP_PARAM[1], command=self.__help_frame.destroy)
        button.pack()

    def init_design(self):
        '''Handles the interface design and creation.'''

        self.__frame1 = tki.Label(self.__parent, text=self.__name,
                        bg=HEADER_BG_COLOR, fg=HEADER_COLOR, font=
                        (DEFAULT_FONT, CANVAS_PARAM[2]),
                        relief=CANVAS_PARAM[3], anchor = CANVAS_PARAM[4])
        self.__frame1.pack(fill = BTN_FILL)
        self.__help_button = tki.Button(self.__frame1, text=HELP_TITLE,
                bg=HEADER_BG_COLOR, fg=HEADER_COLOR, command=self.help_func)
        self.__help_button.pack(side=tki.RIGHT)
        self.shows_current_choices()
        self.create_color_buttons()
        self.create_shape_buttons()
        self.create_member_List()
        self.__canvas.pack()
        self.__canvas.bind(BTN_CLICK, self.handle_mouse_drawing)


    def msg_shape_handler(self, msg):
        '''Draws shape on canvas. parameter msg(str): user name(str),
        shape type(str), coordinates(str) and color(str).'''

        user = msg[1][0]
        shape_type = msg[1][1]
        coords = msg[1][2].split(SEP2)
        coords = [float(i) for i in coords]
        color = msg[1][3]

        if shape_type in [LINE, OVAL, RECTANGLE]:
            self.draw(user, shape_type, [(coords[0], coords[1]), (coords[2],
                                                    coords[3])], color)
        else:
            self.draw(user, shape_type, [(coords[0], coords[1]),(coords[2],
                                coords[3]), (coords[4], coords[5])], color)

    def msg_users_handler(self, msg):
        '''Adds all user names (in param msg, str) to group members list.'''
        user_list = []
        users = msg[1]
        users.remove(self.__name)
        for user in users:
            user_list.append(user)
            self.__members_label.insert(tki.END, user)
        self.__group_members = user_list

    def msg_join_handler(self, msg):
        '''Adds new member's name (in param msg, str) to members list.'''

        if msg[1] != self.__name:
            self.__group_members.append(msg[1][0])
            self.__members_label.insert(tki.END, msg[1][0])

    def msg_leave_handler(self, msg):
        '''Removes leaving user's name from group members list.'''

        if msg[1][0] in self.__group_members:
            index = self.__group_members.index(msg[1][0])
            self.__group_members.pop(index)
            self.__members_label.delete(index)

    def msg_error_handler(self, msg):
        '''Shows user an error message (param msg, str).'''

        error_msg = tki.Toplevel()
        error_msg.wm_title(MSG_ERROR)
        error_label = tki.Label(error_msg, text = msg[1])
        error_label.pack(side=ERR_PARAM[1], expand=ERR_PARAM[3],
                         padx=ERR_PARAM[0], pady=ERR_PARAM[0])
        close_button = tki.Button(error_msg, text=ERROR_CLOSE,
                                padx=ERR_PARAM[2], command=error_msg.destroy)
        close_button.pack()


    def receive_info(self):
        '''Receives data from client and handles each message type.
        Repeats function every set cycle of seconds.'''

        info_list =  self.__client.receive()
        if info_list:
            for msg in info_list:
                if msg[0] == MSG_SHAPE:
                    self.msg_shape_handler(msg)
                elif msg[0] == MSG_USERS:
                    self.msg_users_handler(msg)
                elif msg[0] == MSG_JOIN:
                    self.msg_join_handler(msg)
                elif msg[0] == MSG_LEAVE:
                    self.msg_leave_handler(msg)
                elif msg[0] == MSG_ERROR:
                    self.msg_error_handler(msg)

        self.__parent.after(RECEIVE_TIMER, self.receive_info)

    def get_draw_func(self, shape):
        '''Returns a function which draws the param shape(str).'''

        def draw_shape():
            self.draw(self.__name, shape, self.__mouse_coords,
                      self.__current_color, True)
            self.__mouse_coords = []
            self.__click_count = 0
        return draw_shape()

    def handle_mouse_drawing(self, event):
        '''Draws shape on canvas according to mouse clicks.'''

        self.__click_count += 1
        self.__mouse_coords.append((event.x, event.y))

        if self.__click_count == RECT_LINE_OVAL_MOUSE and \
                                            self.__current_shape != TRIANGLE:
            self.get_draw_func(self.__current_shape)
        elif self.__click_count == TRI_MOUSE and \
                                            self.__current_shape == TRIANGLE:
                self.get_draw_func(TRIANGLE)


    def coords_transform(self, coords):
        '''changes coords from list with tuples, to list of strings.'''

        new_coords = []
        for element in coords:
            new_coords.append(str(element[0]))
            new_coords.append(str(element[1]))

        return new_coords

    def draw(self, user, type, coords, color, private=False):
        '''
        Adds shape to GUI.
        param user(str): name of user who drew the shape.
        param type(str): triangle / line / rectangle / oval.
        param coords(list of tuples of ints): each tuple is x,y coordinate.
        param color (str): color to draw shape in.
        param private(bool): True if current user drew shape, False if shape
                                was drawn by other member of group.
        '''

        coord1_x, coord1_y = coords[0][0], coords[0][1]
        coord2_x, coord2_y = coords[1][0], coords[1][1]
        if len(coords) == 3:
            coord3_x, coord3_y = coords[2][0], coords[2][1]

        if type == LINE:
            self.__canvas.create_line(coord1_x, coord1_y, coord2_x, coord2_y,
                                                            fill=color)
        elif type == RECTANGLE:
            self.__canvas.create_rectangle(coord1_x, coord1_y, coord2_x,
                                                   coord2_y, fill=color)
        elif type == OVAL:
            self.__canvas.create_oval(coord1_x, coord1_y, coord2_x, coord2_y,
                                                                fill=color)
        elif type == TRIANGLE:
            self.__canvas.create_polygon(coord1_x, coord1_y, coord2_x,
                                coord2_y, coord3_x, coord3_y, fill=color)
        self.__canvas.create_text(coord1_x, coord1_y, text=user)

        if private:
            coords = SEP2.join(self.coords_transform(coords))
            msg = MSG_SHAPE, SEP1, type, SEP1, coords , SEP1, color
            self.__client.send(msg)


    def leave(self):
        '''closes gui and connection and sends message to server.'''

        self.__client.send(MSG_LEAVE)
        self.__client.close_connection()
        self.__parent.destroy()


def checkname(name):
    '''Checks if name has less than 20 characters and only english
    letters and numbers. If yes returns True, otherwise returns False.'''
    return len(name) <= MAXNAMELEN and bool(re.match(LEGAL_NAME, name))

def main(name, group, host, port):
    '''Creates a Graphic User Interface and connects user to server.
    User joins a group, whose members all draw on a canvas.'''

    root = tki.Tk()
    Interface(root, name, group, host, port)
    root.mainloop()


if __name__ == '__main__':
    if not checkname(sys.argv[1]) or not checkname((sys.argv[2])):
        print(NAME_ERR_MSG)
    elif len(sys.argv) == NUM_ARGS:
        name = sys.argv[1]
        group = sys.argv[2]
        host = sys.argv[3]
        port = int(sys.argv[4])
        main(name, group, host, port)
    else:
        print(RUN_ERROR)


