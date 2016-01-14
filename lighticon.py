#!/usr/bin/python2
##############################################################################
##############################################################################
## Light Icon, similar to volume icon, displays a system tray icon to manage
## brightness levels
## Thank to FSX and Gattaka (https://bbs.archlinux.org/viewtopic.php?id=77440)
## FSX and Gattaka's version was intended for volume management
## This version is for brightness management
## Dependencies include light (https://haikarainen.github.io/light/)
## For Arch Linux (https://aur.archlinux.org/packages/light/)
##############################################################################
##############################################################################
import gtk, subprocess, os

class light_control():
    window_position = (0, 0)
    light_adjust = range(0, 100)

    def __init__(self):
        # Icons/systemtray
        self.staticon = gtk.StatusIcon()
        DIR=os.path.dirname(os.path.realpath(os.sys.argv[0]))
        self.staticon.set_from_file(DIR+"/lighticon.png")
        self.staticon.connect('scroll_event', self.scroll_event)
        # Menu
        menu = gtk.Menu()
        menu_about = gtk.ImageMenuItem(gtk.STOCK_ABOUT)
        menu_about.connect('button-press-event', self.show_about_dialog)
        menu_quit = gtk.ImageMenuItem(gtk.STOCK_QUIT)
        menu_quit.connect('button-press-event', gtk.main_quit)
        menu.append(menu_about)
        menu.append(menu_quit)

        # Events
        self.staticon.connect('activate', self.cb_activate_icon)
        self.staticon.connect('popup-menu', self.cb_tray_popup, menu)

        # Initialize
        self.slider_window()

    #
    # The light slider window
    #
    def slider_window(self):
        # Window
        self.window = gtk.Window(gtk.WINDOW_POPUP)
        self.window.set_size_request(44, 171)

        # Frame
        frame = gtk.Frame()
        frame.set_border_width(1)

        # Slider
        self.slider = gtk.VScale()
        self.slider.set_inverted(True)
        self.slider.set_range(0, 100)
        self.slider.set_increments(1, 10)
        self.slider.set_digits(0)
        self.slider.set_size_request(34, 160)
        self.slider.set_value_pos(gtk.POS_BOTTOM)
        self.slider.set_value(self.get_master_light())

        # Events
        self.window.connect('destroy', gtk.main_quit)
        self.slider.connect('value-changed', self.cb_slider_change)

        # Add widgets
        fixed_slider = gtk.Fixed()
        fixed_slider.put(self.slider, 3, 5)
        frame.add(fixed_slider)
        self.window.add(frame)

    #
    # Scroll event
    #
    def scroll_event(self,param2,event):
        if event.direction == gtk.gdk.SCROLL_UP:
            if self.slider.get_value() < 100:
                self.slider.set_value(self.slider.get_value() + 1)
        if event.direction == gtk.gdk.SCROLL_DOWN:
            if self.slider.get_value() > 0:
                self.slider.set_value(self.slider.get_value() - 1)
        self.cb_slider_change(self.slider)

    #
    #  Tray icon click
    #
    def cb_activate_icon(self, widget, data=None):
        if self.window.get_property('visible'):
            self.window.hide()
        else:
            self.set_window_position()
            self.window.move(self.window_position[0], self.window_position[1])
            self.window.show_all()
            self.window.present()

    #
    #  System tray menu
    #
    def cb_tray_popup(self, widget, button, time, data = None):
        if button == 3:
            if data:
                data.show_all()
                data.popup(None, None, None, 3, time)

    #
    #  Set brightness through light module
    #
    def cb_slider_change(self, widget):
        val = widget.get_value()

        if (val) in self.light_adjust:
            proc = subprocess.Popen('/usr/bin/light' + ' -S ' + str(val), shell=True, stdout=subprocess.PIPE)
            #print("Brightness Level: {}".format(val))
            proc.wait()

    #
    #  Set window position (just above the system tray icon)
    #
    def set_window_position(self):
        staticon_geometry = self.staticon.get_geometry()[1]

        if staticon_geometry.y <= 200:
            y_coords = staticon_geometry.y
        else:
            y_coords = staticon_geometry.y-180

        self.window_position = (staticon_geometry.x-13, y_coords)

    #
    #  Get current brightness value
    #
    def get_master_light(self):
        proc = subprocess.Popen('/usr/bin/light', shell=True, stdout=subprocess.PIPE)
        amixer_stdout = proc.communicate()[0]
        proc.wait()

        return float(amixer_stdout)

    #
    #  About dialog
    #
    def show_about_dialog(self, widget, data=None):
        about = gtk.AboutDialog()
        about.set_program_name('Light Icon')
        about.set_version('1.0')
        about.set_comments('Light Icon is a simple tool to adjust your brightness. It uses "light" module to set and get the brightness.\n\nWritten by FSX and Himanshu')
        about.run()
        about.destroy()

light_control()
gtk.main()
