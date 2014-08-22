#!/usr/bin/env python3

from gi.repository import Gtk, Gdk, cairo
import math

clicks = [];

def text_extent(cairo_context, font, font_size, text):
    # surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 0, 0)
    # ctx = cairo.Context(surface)
    cairo_context.select_font_face(font)
    cairo_context.set_font_size(font_size)
    
    return cairo_context.text_extents(text)
# end text_entent()

class CellType:
    WHEAT   = 0
    WOOD    = 1
    ROCK    = 2
    SHEEP   = 3
    BRICK   = 4
    DESERT  = 5
    SEA     = 6
    
    COLOR   = [(1.0000, 0.8431, 0.0000),    # WHEAT
               (0.1333, 0.5451, 0.1333),    # WOOD
               (0.3000, 0.3000, 0.3000),    # ROCK
               (0.4431, 0.7373, 0.4706),    # SHEEP
               (0.6980, 0.1333, 0.1333),    # BRICK
               (0.7647, 0.6902, 0.6902),    # DESERT
               (0.0000, 0.5294, 0.7411),]   # SEA
# end class CellType

class HexCell:
    def __init__(self, x, y):
        self.x     = x
        self.y     = y
        self.value = 0
        self.terrain  = CellType.SEA
    # end __init__()
    
    def SetValue(self, value):
        self.value = value
        # print('%d,%d = %d' % (self.x, self.y, self.value))
    # end SetValue()
    
    def SetTerrain(self, terrain):
        self.terrain = terrain
    # end SetTerrain()
# end class HexCell

class MyApp(Gtk.Window):
    HEX_EDGE_LEN = 50
    HEX_HEIGHT   = 20
    HEX_WIDTH    = 20
    HEX_CENTER_X = -1 * (HEX_HEIGHT + 1) * HEX_EDGE_LEN
    HEX_CENTER_Y = HEX_EDGE_LEN
    # HEX_CENTER_X = 0
    # HEX_CENTER_Y = 0

    KEY_LEFT  = 65361
    KEY_UP    = 65362
    KEY_RIGHT = 65363
    KEY_DOWN  = 65364

    KEY_2     = ord(u'2')
    KEY_3     = ord(u'3')
    KEY_4     = ord(u'4')
    KEY_5     = ord(u'5')
    KEY_6     = ord(u'6')
    KEY_7     = ord(u'7')
    KEY_8     = ord(u'8')
    KEY_9     = ord(u'9')
    KEY_A     = ord(u'a')
    KEY_B     = ord(u'b')
    KEY_C     = ord(u'c')
    
    KEY_Q     = ord(u'q')
    KEY_W     = ord(u'w')
    KEY_E     = ord(u'e')
    KEY_R     = ord(u'r')
    KEY_T     = ord(u't')
    KEY_Y     = ord(u'y')
    KEY_U     = ord(u'u')  
    KEY_S     = ord(u'S')  
      
    
    KEY_2_ALT = 65456 + 2
    KEY_3_ALT = 65456 + 3
    KEY_4_ALT = 65456 + 4
    KEY_5_ALT = 65456 + 5
    KEY_6_ALT = 65456 + 6
    KEY_7_ALT = 65456 + 7
    KEY_8_ALT = 65456 + 8
    KEY_9_ALT = 65456 + 9
    
    KEY_LIST = [KEY_LEFT, KEY_UP, KEY_RIGHT, KEY_DOWN, KEY_2, KEY_3, KEY_4, KEY_5, KEY_6, KEY_7, KEY_8, KEY_9, KEY_A, KEY_B, KEY_C, KEY_2_ALT, KEY_3_ALT, KEY_4_ALT, KEY_5_ALT, KEY_6_ALT, KEY_7_ALT, KEY_8_ALT, KEY_9_ALT, KEY_Q, KEY_W, KEY_E, KEY_R, KEY_T, KEY_Y, KEY_U, KEY_S]
    
    def __init__(self):
        Gtk.Window.__init__(self, title="Draw on button press")
        self.set_size_request(800, 800)
        self.connect('delete-event', Gtk.main_quit)

        self.drawing_area = Gtk.DrawingArea()
        self.drawing_area.add_events(Gdk.EventMask.BUTTON_PRESS_MASK) 
        self.drawing_area.connect('draw', self.on_drawing_area_draw)
        self.drawing_area.connect('button-press-event', self.on_drawing_area_button_press)
        self.drawing_area.show()
        self.add(self.drawing_area)

        self.current_loc = (0,0)   

        self.connect('key_release_event', self.on_key_press_event)     
    
        self.HexGrid = list()

        for ix in range(0, self.HEX_WIDTH):
            hex_line = list()
            for iy in range(0, self.HEX_HEIGHT):
                hex_line.append(HexCell(ix, iy))
            # end for
            
            self.HexGrid.append(hex_line)
        # end for

        self.show_all()
    # end __init__()
    
    def Save(self):
        pass
    # end Save()
    
    def IsNumber(self, keyval):
        is_number = keyval in [self.KEY_2, self.KEY_3, self.KEY_4, self.KEY_5, self.KEY_6, self.KEY_7, self.KEY_8, self.KEY_9, self.KEY_A, self.KEY_B, self.KEY_C, self.KEY_2_ALT, self.KEY_3_ALT, self.KEY_4_ALT, self.KEY_5_ALT, self.KEY_6_ALT, self.KEY_7_ALT, self.KEY_8_ALT, self.KEY_9_ALT] 
        # print('is_number ', is_number)
        return (is_number)
    # end IsNumber()
    
    def UnicodeToVal(self, keyval):
        if (keyval >= self.KEY_2) and (keyval <= self.KEY_9):
            return (2 + keyval - self.KEY_2)
        elif (keyval >= self.KEY_A) and (keyval <= self.KEY_C):
            return (10 + keyval - self.KEY_A)
        elif (keyval >= self.KEY_2_ALT) and (keyval <= self.KEY_9_ALT):
            return (2 + keyval - self.KEY_2_ALT)
        # end if
    # end UnicodeToVal()
    
    def process_key(self, keyval):
        if (keyval == self.KEY_LEFT):
            self.current_loc = (self.current_loc[0] - 1 , self.current_loc[1]) 
        elif (keyval == self.KEY_UP):
            self.current_loc = (self.current_loc[0], self.current_loc[1] - 1)
        elif (keyval == self.KEY_RIGHT):
            self.current_loc = (self.current_loc[0] + 1 , self.current_loc[1])  
        elif (keyval == self.KEY_DOWN):
            self.current_loc = (self.current_loc[0], self.current_loc[1] + 1)
        elif (self.IsNumber(keyval)):
            value = self.UnicodeToVal(keyval)
            self.HexGrid[self.current_loc[0]][self.current_loc[1]].SetValue(value)
        elif (keyval == self.KEY_Q):
            self.HexGrid[self.current_loc[0]][self.current_loc[1]].SetTerrain(CellType.WHEAT)
        elif (keyval == self.KEY_W):
            self.HexGrid[self.current_loc[0]][self.current_loc[1]].SetTerrain(CellType.WOOD)
        elif (keyval == self.KEY_E):
            self.HexGrid[self.current_loc[0]][self.current_loc[1]].SetTerrain(CellType.ROCK)
        elif (keyval == self.KEY_R):
            self.HexGrid[self.current_loc[0]][self.current_loc[1]].SetTerrain(CellType.SHEEP)
        elif (keyval == self.KEY_T):
            self.HexGrid[self.current_loc[0]][self.current_loc[1]].SetTerrain(CellType.BRICK)
        elif (keyval == self.KEY_Y):
            self.HexGrid[self.current_loc[0]][self.current_loc[1]].SetTerrain(CellType.DESERT)
        elif (keyval == self.KEY_U):
            self.HexGrid[self.current_loc[0]][self.current_loc[1]].SetTerrain(CellType.SEA)
        elif (keyval == self.KEY_S):
            self.Save()
        # end if
        
        self.drawing_area.queue_draw()
    # end process_key()

    def on_key_press_event(self, widget, event):
        if (event.keyval in self.KEY_LIST):
            # print('on_key_press_event %d' % event.keyval)
            self.process_key(event.keyval)
        # end if
    # end on_key_press_event()
        

    def on_drawing_area_button_press(self, widget, event):
        
        # clicks.append([event.x, event.y])
        
        
        # q = 2/3 * event.x / self.HEX_EDGE_LEN
        # r = (1/3*math.sqrt(3) * event.y - 1/3 * event.x) / self.HEX_EDGE_LEN

        # print("Mouse clicked... at ", event.x, ", ", event.y)
        # print("HexCell...       at ", q, ", ", r)

        # self.current_loc = (r,q)

        # self.drawing_area.queue_draw()

        return True
    # end on_drawing_area_button_press()

    def draw_hex_at_center(self, cairo_context, center_x, center_y, size, fill_color):
        trace = []
    
        for ia in range(0,7):
            angle = 2 * math.pi / 6 * ia
            x_i = float(center_x + size * math.cos(angle))
            y_i = float(center_y + size * math.sin(angle))

            trace.append((x_i, y_i))
            # previous_point = (x_i, y_i)
        # end for
        
        for trace_ix in range(0, len(trace)):
            trace_element = trace[trace_ix]
            
            if (trace_ix is 0):
                cairo_context.move_to(trace_element[0], trace_element[1])
            else:
                cairo_context.line_to(trace_element[0], trace_element[1])
            # end if
        # for
        
        cairo_context.set_source_rgb(fill_color[0], fill_color[1], fill_color[2])
        cairo_context.fill()
        
        for trace_ix in range(0, len(trace)):
            trace_element = trace[trace_ix]
            
            if (trace_ix is 0):
                cairo_context.move_to(trace_element[0], trace_element[1])
            else:
                cairo_context.line_to(trace_element[0], trace_element[1])
            # end if
        # for
        
        cairo_context.set_source_rgb(0.0, 0.0, 0.0)
        cairo_context.stroke()
    # end draw_hex_at_center()
    
    def draw_value(self, cairo_context, value, center_x, center_y):
        FONT_SIZE = 24
        
        if (value is not 0):
            text = str(value)
        else:
            return
        # end if
        
        cairo_context.set_font_size(FONT_SIZE)
        
        
        (x_bearing, y_bearing, text_width, text_height,  x_advance, y_advance) = text_extent(cairo_context, 'Sans', FONT_SIZE, text)
        
        cairo_context.move_to(center_x + x_bearing - text_width / 2 , center_y - y_bearing / 2)
        
        if (value == 6) or (value == 8):
            cairo_context.set_source_rgb(1.0, 0.0, 0.0)
        else:
            cairo_context.set_source_rgb(0.0, 0.0, 0.0)
        # end if
        
        cairo_context.text_path(text)
        cairo_context.stroke()
    # end draw_value()

    def on_drawing_area_draw(self, drawing_area, cairo_context):
        # print('#' * 80)
        previous_point = (self.HEX_CENTER_X, self.HEX_CENTER_Y)

        for row in self.HexGrid:
            for cell in row:
                center_x = self.HEX_CENTER_X + 3 * (self.HEX_EDGE_LEN * cell.x + self.HEX_EDGE_LEN * cell.y / 2)
                center_y = self.HEX_CENTER_Y + math.sqrt(3.0) * self.HEX_EDGE_LEN * cell.y / 2.0

                self.draw_hex_at_center(cairo_context, center_x, center_y, self.HEX_EDGE_LEN, CellType.COLOR[cell.terrain])
                
                if (cell.x is int(self.current_loc[0])) and (cell.y is int(self.current_loc[1])):
                    self.draw_hex_at_center(cairo_context, center_x, center_y, self.HEX_EDGE_LEN/2, (1.0, 1.0, 1.0))
                # end if
                
                self.draw_value(cairo_context, cell.value, center_x, center_y)
            # end for
        # end for

        # cairo_context.stroke()

        return False
    # end on_drawing_area_draw()

# end class MyApp

app = MyApp()
Gtk.main()
