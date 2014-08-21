#!/usr/bin/env python3

from gi.repository import Gtk, Gdk, cairo
import math

clicks = [];

class MyApp(Gtk.Window):
    HEX_EDGE_LEN = 50
    HEX_HEIGHT   = 20
    HEX_WIDTH    = 20
    HEX_CENTER_X = -1 * (HEX_HEIGHT + 1) * HEX_EDGE_LEN
    HEX_CENTER_Y = HEX_EDGE_LEN
    
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

        self.show_all()
    # end __init__()
        

    def on_drawing_area_button_press(self, widget, event):
        # print("Mouse clicked... at ", event.x, ", ", event.y)
        clicks.append([event.x, event.y])
        self.drawing_area.queue_draw()

        return True
    # end on_drawing_area_button_press()

    def draw_hex_at_center(self, cairo_context, center_x, center_y):
        for ia in range(0,7):
            angle = 2 * math.pi / 6 * ia
            x_i = float(center_x + self.HEX_EDGE_LEN * math.cos(angle))
            y_i = float(center_y + self.HEX_EDGE_LEN * math.sin(angle))

            # print('%d,%d'%(int(x_i,), int(y_i)))

            if (ia is 0):
                cairo_context.move_to(x_i, y_i)
            else:
                # print('previous_point = ', previous_point)
                # print('(x_i, y_i) = ',   (x_i, y_i))
                cairo_context.line_to(x_i, y_i)
            # end if

            previous_point = (x_i, y_i)
        # end for
    # end draw_hex_at_center()

    def on_drawing_area_draw(self, drawing_area, cairo_context):
        # print('#' * 80)
        previous_point = (self.HEX_CENTER_X, self.HEX_CENTER_Y)

        for ix in range(0, self.HEX_WIDTH):
            for iy in range(0, self.HEX_HEIGHT):
                center_x = self.HEX_CENTER_X + 3 * (self.HEX_EDGE_LEN * ix + self.HEX_EDGE_LEN * iy / 2)
                center_y = self.HEX_CENTER_Y + math.sqrt(3.0) * self.HEX_EDGE_LEN * iy / 2.0

                self.draw_hex_at_center(cairo_context, center_x, center_y)
                # print()
            # end for
        # end for

        cairo_context.stroke()

        return False
    # end on_drawing_area_draw()

# end class MyApp

app = MyApp()
Gtk.main()
