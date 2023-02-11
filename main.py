"""Packages required"""
# python3-gi
# python3-gi-cairo
# gir1.2-gtk-3.0
# gir1.2-glib-2.0
# gir1.2-gtksource-3.0
# gir1.2-pango-1.0

import sys
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('GtkSource', '3.0')
gi.require_version('Gio', '2.0')
gi.require_version('Pango', '1.0')
gi.require_version('Gdk', '3.0')
gi.require_version('GdkPixbuf', '2.0')

from gi.repository import Gtk, Gio, Gdk, Pango, GtkSource, GdkPixbuf

from data.gui_config import *
from data.gnome_themes import *

from client_test import *
import client_core

"""BEGINNING OF GUI"""
# mode - decides the current function of program: FUNCTION[mode]
# signal - sent to server, representing the current mode
# mode = 1: TRANSLATOR       ->  signal = 0
# mode = 2: GRAMMAR CHECKER  ->  signal = 1
# Initially: mode = 1: TRANSLATOR

mode = 1

input_area = GtkSource.View()
output_area = GtkSource.View()
function_list = Gtk.ListBox()
activation_button = Gtk.Button()

# TODO: add theme choosing menu
settings = Gtk.Settings.get_default()
# THEME[11] is the default theme
current_theme = 11
settings.set_property('gtk-theme-name', THEMES[current_theme])
# settings.set_property('gtk-application-prefer-dark-theme', False)

class MainWindow(Gtk.ApplicationWindow):
    def theme_button_clicked(self, button):
        global current_theme
        if current_theme == 29:
            current_theme = 0
        else:
            current_theme += 1
        settings.set_property('gtk-theme-name', THEMES[current_theme])
        
    def handle_input(self, input_str):
        """ Main function of program to handle input and show output data.
        Called from 'on_button_clicked()' when user clicks the 'Translate/Grammer Check' button.
        """
        
        signal = str(mode-1)
        self.client.send_message(input_str, signal)
        return self.client.receive_message()
        
    def __init__(self, app, client):
        """Create the top-level window"""
        Gtk.ApplicationWindow.__init__(self, application=app)
        self.border_width = 10
        self.window_position = Gtk.WindowPosition.CENTER # not work 
        self.props.resizable = False
        self.set_default_size(MIN_WIDTH, MIN_HEIGHT)
        
        self.client = client

        #Create a grid to arrange the widgets
        grid = Gtk.Grid()
        self.add(grid)
        
        # Set margins for the main window
        #     top    = row_spacing    + empty_box_v1.height
        #     bottom = row_spacing    + empty_box_v3.height
        #     left   = column_spacing + empty_box_h1.width
        #     right  = column_spacing + empty_box_h1.width
        
        grid.props.row_spacing    = 7
        grid.props.column_spacing = 12
        empty_box_v1 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, vexpand=False, hexpand=False, spacing=0)
        empty_box_v1.set_size_request(0, 8)
        empty_box_v2 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, vexpand=False, hexpand=False, spacing=0)
        empty_box_v2.set_size_request(0, 0)
        empty_box_v3 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, vexpand=False, hexpand=False, spacing=0)
        empty_box_v3.set_size_request(0, 8)
        grid.attach(empty_box_v1, 0, 0, 1, 1)
        grid.attach(empty_box_v2, 0, 2, 1, 1)
        grid.attach(empty_box_v3, 0, 4, 1, 1)
        empty_box_h1 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, vexpand=False, hexpand=False, spacing=0)
        empty_box_h1.set_size_request(3, 0)
        empty_box_h2 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, vexpand=False, hexpand=False, spacing=0)
        empty_box_h2.set_size_request(4, 0)
        grid.attach(empty_box_h1, 0, 1, 1, 1)
        grid.attach(empty_box_h2, 4, 1, 1, 1)
        
        """Create the header bar"""
        headerbar = Gtk.HeaderBar()
        headerbar.props.show_close_button = True
        headerbar.props.title             = PROGRAM_NAME
        headerbar.props.spacing           = 0
        self.set_titlebar(headerbar)
        
        # Header bar: Theme choosing menu, Undo and Redo buttons
        theme_choosing_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, vexpand=False, hexpand=False, spacing=5)
        theme_choosing_box.props.margin_start = 10
        
        theme_choosing_button = Gtk.Button()
        theme_choosing_button.props.label = 'Theme'
        
        theme_choosing_button.connect("clicked", self.theme_button_clicked)
        theme_choosing_menu = Gtk.Menu()
        
        theme_choosing_box.add(theme_choosing_button)
        
        undo_button = Gtk.Button()
        redo_button = Gtk.Button()
        undo_button.props.label = 'Undo'
        redo_button.props.label = 'Redo'
        theme_choosing_box.add(undo_button)
        theme_choosing_box.add(redo_button)
        
        undo_button.connect("clicked", self._on_Undo_clicked)
        redo_button.connect("clicked", self._on_Redo_clicked)
        headerbar.pack_start(theme_choosing_box)
        
        # Header bar: Preferences menu
        preferences_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, vexpand=False, hexpand=False, spacing=6)
        preferences_box.props.margin_end = 22
        menu_button_01 = Gtk.MenuButton()
        menu_button_01.add(Gtk.Image.new_from_icon_name('open-menu-symbolic', Gtk.IconSize.MENU))
        
        primary_menu = Gio.Menu()
        
        self.create_action('preferences', self.on_preferences_action)
        self.create_action('help', self.on_help_action, ['F1'])
        self.create_action('about', self.on_about_action)
        self.create_action('quit', self.on_quit_action, ['<primary>q'])
        
        section_01 = Gio.Menu()
        section_01.append_item(Gio.MenuItem.new('_Preferences', 'app.preferences'))
        
        section_02 = Gio.Menu()
        section_02.append_item(Gio.MenuItem.new('_Keyboard Shortcuts', 'win.show-help-overlay'))
        section_02.append_item(Gio.MenuItem.new('_Help', 'app.help'))
        section_02.append_item(Gio.MenuItem.new('_About '+PROGRAM_NAME, 'app.about'))
        
        section_03 = Gio.Menu()
        section_03.append_item(Gio.MenuItem.new('_Quit', 'app.quit'))
        
        
        primary_menu.append_section(None, section_01)
        primary_menu.append_section(None, section_02)
        primary_menu.append_section(None, section_03)
        menu_button_01.props.menu_model = primary_menu
        
        preferences_box.pack_end(menu_button_01, False, False, 0)
        
        # Header bar: 'Save output to text file' button
        menu_button_02 = Gtk.MenuButton()
        menu_button_02.add(Gtk.Image.new_from_icon_name('document-save-symbolic', Gtk.IconSize.MENU))
        preferences_box.pack_end(menu_button_02, False, False, 0)
        
        headerbar.pack_end(preferences_box)

        """Create the left sidebar"""
        sidebar = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, vexpand=True, hexpand=False, spacing=10)
        sidebar.props.homogeneous = False
        sidebar.set_size_request(200, 500)
        grid.attach(sidebar, 1, 1, 1, 1)

        # Add functions to the sidebar     
        function_list.connect('row_activated', self.on_row_activated)
        row1 = Gtk.ListBoxRow()
        row2 = Gtk.ListBoxRow()
        row3 = Gtk.ListBoxRow()
        row4 = Gtk.ListBoxRow()
        
        frame1 = Gtk.Frame()
        frame2 = Gtk.Frame()
        frame3 = Gtk.Frame()
        frame4 = Gtk.Frame()
        
        frame1.add(Gtk.Label(label=FUNCTION_LIST[1]))
        row1.add(frame1)
        row1.set_size_request(200, 50)
        
        frame2.add(Gtk.Label(label=FUNCTION_LIST[2]))
        row2.add(frame2)
        row2.set_size_request(200, 50)
        
        frame3.add(Gtk.Label(label=FUNCTION_LIST[3]))
        row3.add(frame3)
        row3.set_size_request(200, 50)
        
        frame4.add(Gtk.Label(label=FUNCTION_LIST[4]))
        row4.add(frame4)
        row4.set_size_request(200, 50)
        
        function_list.add(row1)
        function_list.add(row2)
        #function_list.add(row3)
        #function_list.add(row4)
        sidebar.add(function_list)
        
        """Create a separator line between the left sidebar and main view area"""
        separator = Gtk.Separator(orientation=Gtk.Orientation.VERTICAL)
        grid.attach(separator, 2, 1, 1, 1)
        
        """Create the main view area"""
        main_view = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, vexpand=False, hexpand=True, spacing=10)
        grid.attach(main_view, 3, 1, 1, 1)
        
        # Main view area: Create option bar to choose language
        option_bar = Gtk.EventBox()
        option_bar.props.visible = False
        option_bar_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, vexpand=False, hexpand=False, spacing=0)
        option_bar.add(option_bar_box)
        main_view.pack_start(option_bar, False, False, 0)
        
        input_language_store = Gtk.ListStore(str)
        for input_language in LANGUAGE:
            input_language_store.append([input_language])
        input_language_combo = Gtk.ComboBox.new_with_model(input_language_store)
        input_renderer_text = Gtk.CellRendererText()
        input_language_combo.pack_start(input_renderer_text, True)
        input_language_combo.add_attribute(input_renderer_text, 'text', 0)
        input_language_combo.props.active = True
        option_bar_box.pack_start(input_language_combo, False, False, 0)
        
        output_language_store = Gtk.ListStore(str)
        for output_language in LANGUAGE:
            output_language_store.append([output_language])
        output_language_combo = Gtk.ComboBox.new_with_model(output_language_store)
        output_renderer_text = Gtk.CellRendererText()
        output_language_combo.pack_start(output_renderer_text, True)
        output_language_combo.add_attribute(output_renderer_text, 'text', 0)
        output_language_combo.props.active = False
        option_bar_box.pack_end(output_language_combo, False, False, 0)
        
        # Main view area: Input/Output
        paned = Gtk.Paned()
        main_view.pack_start(paned, True, True, 0)
        paned.props.position = 472
        IO_MARGIN = 15
        LARGER_MARGIN_SCALE = 1.5
        
        # Main view area: Input
        input_frame = Gtk.Frame()
        paned.add1(input_frame)
        input_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, vexpand=True, hexpand=True, spacing=10)
        input_frame.add(input_box)
        
        input_scrollable_area = Gtk.ScrolledWindow()
        input_scrollable_area.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        
        input_area.props.top_margin      = IO_MARGIN
        input_area.props.bottom_margin   = IO_MARGIN
        input_area.props.left_margin     = LARGER_MARGIN_SCALE*IO_MARGIN
        input_area.props.right_margin    = IO_MARGIN
        input_area.props.wrap_mode       = Gtk.WrapMode.WORD
        input_area.props.editable        = True
        input_area.props.cursor_visible  = True
        
        input_scrollable_area.add(input_area)
        input_box.pack_start(input_scrollable_area, True, True, 0)
        
        self.connect("key-press-event", self._key_press_event_Redo)

        # Main view area: Output
        output_frame = Gtk.Frame()
        paned.add2(output_frame)
        output_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, vexpand=True, hexpand=True, spacing=10)
        output_frame.add(output_box)
        
        output_scrollable_area = Gtk.ScrolledWindow()
        output_scrollable_area.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        
        output_area.props.top_margin     = IO_MARGIN
        output_area.props.bottom_margin  = IO_MARGIN
        output_area.props.left_margin    = LARGER_MARGIN_SCALE*IO_MARGIN
        output_area.props.right_margin   = IO_MARGIN
        output_area.props.wrap_mode      = Gtk.WrapMode.WORD
        output_area.props.editable       = True
        output_area.props.cursor_visible = False
        
        self.set_default_output_if_input_empty()
        
        output_scrollable_area.add(output_area)
        output_box.pack_start(output_scrollable_area, True, True, 0)
        
        # TODO: change the background and text color of TextView
        IO_OPACITY = 0.05
        input_area.override_background_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(1,1,1,IO_OPACITY))
        output_area.override_background_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(1,1,1,IO_OPACITY))
        
        """Add a button to activation the _action"""
        activation_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, vexpand=True, hexpand=True, spacing=10)
        activation_box.set_size_request(0, 50)
        grid.attach(activation_box, 3, 3, 1, 1)
        
        activation_button.props.label = FUNCTION[mode]
        activation_button.connect('clicked', self.on_button_clicked)
        activation_box.pack_start(activation_button, True, True, 350)
    
    
    def set_default_output_if_input_empty(self, activated=False):
        """Set default text for output, if the input is empty.
        Called when the input or mode is changed.
        """
        activated = True
        if not activated:
            return
        input_buffer = input_area.get_buffer()

        if input_buffer.get_start_iter().get_offset() == input_buffer.get_end_iter().get_offset():
            output_buffer = GtkSource.Buffer()
            output_buffer.props.text = DEFAULT_OUTPUT[mode]
            italic_tag = output_buffer.create_tag("italic", style=Pango.Style.ITALIC)
            output_buffer.apply_tag(italic_tag, output_buffer.get_start_iter(), output_buffer.get_end_iter())
            output_area.set_buffer(output_buffer)
            
    def _key_press_event_Redo(self, widget, event):
        """"Add shortcut Ctr+Y for Redo"""
        keyval_name = Gdk.keyval_name(event.keyval)
        ctrl = (event.state & Gdk.ModifierType.CONTROL_MASK)
        textbuffer = input_area.get_buffer()
        if ctrl and keyval_name == 'y':
            if textbuffer.can_redo():
                textbuffer.do_redo(textbuffer)
                
    def _on_Undo_clicked(self, button):
        """Called when user clicks the Undo button"""
        textbuffer = input_area.get_buffer()
        if textbuffer.can_undo():
            textbuffer.undo()
            
    def _on_Redo_clicked(self, button):
        """Called when user clicks the Redo button"""
        textbuffer = input_area.get_buffer()
        if textbuffer.can_redo():
            textbuffer.redo()  
            
    def on_row_activated(self, list_box, row):
        """Set mode for program.
        Called when the user chooses the function on the left sidebar.
        """
        current_row = function_list.get_selected_row()
        global mode
        mode = 1+current_row.get_index()
        activation_button.props.label = FUNCTION[mode]
        activation_button.show_all()
        self.set_default_output_if_input_empty()
    	
    def on_button_clicked(self, widget):
        """Get input and show output.
        Called when user clicks the 'Translate/Grammar Check' button.
        """
        input_buffer = input_area.get_buffer()
        text_input = input_buffer.get_text(input_buffer.get_start_iter(), input_buffer.get_end_iter(), False)
        output_buffer = output_area.get_buffer()
        output_buffer.remove_all_tags(output_buffer.get_start_iter(), output_buffer.get_end_iter())
        text_output = self.handle_input(text_input)
        print(text_output)
        output_buffer.props.text = text_output
        self.set_default_output_if_input_empty()        
    
    def on_preferences_action(self, widget, _):
        """Callback for the app.preferences action."""
        print('Preferences action activated')
        
    def on_about_action(self, widget, _):
        """Callback for the app.about action."""
        about_dialog = Gtk.AboutDialog()
        about_dialog.props.program_name = PROGRAM_NAME
        about_dialog.props.version      = CURRENT_VERSION
        
        program_logo = GdkPixbuf.Pixbuf.new_from_file("/home/daonguyen/Projects/Languator/data/icons/hicolor_01.svg")
        
        about_dialog.run()
        about_dialog.destroy()
        print('About action activated')
        
        
    def on_help_action(self, widget, _):
        """Callback for the app.help action."""
        print('Help action activated')
        
    def on_quit_action(self, widget, _):
        """Callback for the app.quit action."""
        app.quit()
        
    def create_action(self, name, callback, shortcuts=None):
        """Add an application action.
        Args:
            + name:      the name of the action
            + callback:  the function to be called when the action is activated
            + shortcuts: an optional list of accelerators
        """
        action = Gio.SimpleAction.new(name, None)
        action.connect('activate', callback)
        app.add_action(action)
        if shortcuts:
            app.set_accels_for_action(f'app.{name}', shortcuts)
     
"""ENDING OF GUI"""

class LanguatorApplication(Gtk.Application):
    """The main application singleton class."""
    
    def __init__(self, client):
        Gtk.Application.__init__(self, application_id='org.gnome.languator', flags=Gio.ApplicationFlags.FLAGS_NONE)
        window = None

    def do_activate(self):
        """Called when the application is activated."""
        # We only allow a single window and raise any existing ones
        window = self.props.active_window
        if not window:
            window = MainWindow(self, client)
            window.show_all()
        window.present()

"""The application's entry point."""
if __name__ == "__main__":
    client = Client(client_core.SERVER_IP, client_core.SERVER_PORT)
    app = LanguatorApplication(client)
    app.run(sys.argv)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
