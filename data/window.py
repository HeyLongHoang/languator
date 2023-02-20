"""Packages required:
python3-gi
python3-gi-cairo
gir1.2-gtk-3.0
gir1.2-glib-2.0
gir1.2-gtksource-3.0
gir1.2-pango-1.0

sudo apt update
sudo apt install python3-gi python3-gi-cairo gir1.2-gtk-3.0 gir1.2-glib-2.0 gir1.2-gtksource-3.0 gir1.2-pango-1.0
"""

import os
import sys
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('GtkSource', '3.0')
gi.require_version('Gio', '2.0')
gi.require_version('Pango', '1.0')
gi.require_version('Gdk', '3.0')
gi.require_version('GdkPixbuf', '2.0')

from gi.repository import Gtk, Gio, Gdk, Pango, GtkSource, GdkPixbuf

from data.gnome_themes import *
from data.gui_core import *
from data.app_about import *

class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, current_app):
        """Create the top-level window"""
        super().__init__(application=current_app)
        self.border_width = 10
        self.props.window_position = Gtk.WindowPosition.CENTER # not work
        self.props.resizable = False
        self.set_default_size(MIN_WIDTH, MIN_HEIGHT)

        self.app = current_app

        # Set default dark theme for the program
        self.settings = Gtk.Settings.get_default()
        self.current_theme = 0
        self.dark_theme = True
        self.settings.set_property('gtk-theme-name', THEMES[0][True])

        # Create a grid to arrange the widgets
        grid = Gtk.Grid()
        self.add(grid)

        # Set margins for the main window
        #     top    = row_spacing    + empty_box_v1.height
        #     bottom = row_spacing    + empty_box_v3.height
        #     left   = column_spacing + empty_box_h1.width
        #     right  = column_spacing + empty_box_h1.width

        Row_Spc, Col_Spc = 7, 12
        grid.props.row_spacing    = Row_Spc
        grid.props.column_spacing = Col_Spc
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

        # Header bar: Theme choosing menu
        theme_choosing_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, vexpand=False, hexpand=False, spacing=6)
        theme_choosing_box.props.margin_start = 10
        theme_choosing_box.props.margin_end = 570 #481.5 #610

        self.dark_theme_button = Gtk.Button()
        self.dark_theme_button.props.image = Gtk.Image.new_from_icon_name('weather-clear-night-symbolic', Gtk.IconSize.MENU)

        # Header bar: New Window button
        new_window_button = Gtk.Button()
        new_window_button.props.image = Gtk.Image.new_from_icon_name('window-new-symbolic', Gtk.IconSize.BUTTON)

        theme_choosing_box.add(new_window_button)
        theme_choosing_box.add(self.dark_theme_button)

        # Header bar: Preferences menu
        self.preferences_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, vexpand=False, hexpand=False, spacing=6)
        #self.preferences_box.props.margin_start = 865
        self.preferences_box.props.margin_end = 22

        main_menu_button = Gtk.MenuButton()
        main_menu_button.props.image = Gtk.Image.new_from_icon_name('open-menu-symbolic', Gtk.IconSize.MENU)
        primary_menu = Gio.Menu()

        self.app.create_action('refresh',           self.on_Refresh_clicked, ['F5'])
        self.app.create_action('new_window',        self.start_new_window,   ['<primary>n'])
        self.app.create_action('preferences',       self.on_preferences_action)
        self.app.create_action('keyboard_shortcut', self.help_overlay)
        self.app.create_action('help',              self.on_help_action,     ['F1'])
        self.app.create_action('about',             self.show_about)
        self.app.create_action('quit',              self.app.on_quit_action, ['<primary>q'])

        section_00 = Gio.Menu()
        section_00.append_item(Gio.MenuItem.new('_New Window', 'app.new_window'))

        section_01 = Gio.Menu()
        section_01.append_item(Gio.MenuItem.new('_Refresh', 'app.refresh'))

        section_02 = Gio.Menu()
        section_02.append_item(Gio.MenuItem.new('_Preferences', 'app.preferences'))

        section_03 = Gio.Menu()
        section_03.append_item(Gio.MenuItem.new('_Keyboard Shortcuts', 'app.keyboard_shortcut'))
        section_03.append_item(Gio.MenuItem.new('_Help', 'app.help'))
        section_03.append_item(Gio.MenuItem.new('_About '+PROGRAM_NAME, 'app.about'))

        section_04 = Gio.Menu()
        section_04.append_item(Gio.MenuItem.new('_Quit', 'app.quit'))

        primary_menu.append_section(None, section_00)
        primary_menu.append_section(None, section_01)
        primary_menu.append_section(None, section_02)
        primary_menu.append_section(None, section_03)
        primary_menu.append_section(None, section_04)
        main_menu_button.props.menu_model = primary_menu

        # Header bar: 'Save output to text file' button
        self.saving_button = Gtk.Button()
        self.saving_button.props.image = Gtk.Image.new_from_icon_name('document-save-symbolic', Gtk.IconSize.MENU)
        self.saving_button_inactive = Gtk.MenuButton()
        self.saving_button_inactive.props.image = Gtk.Image.new_from_icon_name('document-save-symbolic', Gtk.IconSize.MENU)

        self.preferences_box.pack_end(main_menu_button, False, False, 0)
        #self.preferences_box.pack_end(self.refresh_button, False, False, 0)
        self.preferences_box.pack_end(self.saving_button_inactive, False, False, 0)

        # Header bar: Refresh button
        self.refresh_button = Gtk.Button()
        self.refresh_button.props.image = Gtk.Image.new_from_icon_name('view-refresh-symbolic', Gtk.IconSize.BUTTON)
        #theme_choosing_box.add(self.refresh_button)
        #self.preferences_box.pack_end(self.refresh_button, False, False, 0)

        headerbar.pack_start(theme_choosing_box)
        headerbar.pack_end(self.preferences_box)

        """Create the left sidebar"""
        sidebar = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, vexpand=True, hexpand=False, spacing=10)
        sidebar.props.homogeneous = False
        sidebar.set_size_request(200, 500)
        grid.attach(sidebar, 1, 1, 1, 1)

        self.function_list = Gtk.ListBox()

        # Add functions to the sidebar
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

        self.function_list.add(row1)
        self.function_list.add(row2)
        #self.function_list.add(row3)
        #self.function_list.add(row4)
        sidebar.add(self.function_list)

        """Create a separator line between the left sidebar and main view area"""
        separator = Gtk.Separator(orientation=Gtk.Orientation.VERTICAL)
        grid.attach(separator, 2, 1, 1, 1)

        """Create the main view area"""
        main_view = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, vexpand=False, hexpand=True, spacing=10)
        grid.attach(main_view, 3, 1, 1, 1)

        # Main view area: Create an option bar to choose language
        option_bar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, vexpand=False, hexpand=False, spacing=0)
        option_bar.props.homogeneous = True

        self.ob_left_space   = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, vexpand=False, hexpand=False, spacing=0)
        self.ob_middle_space = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, vexpand=False, hexpand=False, spacing=0)
        self.ob_right_space  = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, vexpand=False, hexpand=False, spacing=0)

        main_view.pack_start(option_bar, expand=False, fill=False, padding=0)

        """Add elements if mode == 1: TRANSLATOR"""
        self.source_lang_box = Gtk.Box()
        self.target_lang_box = Gtk.Box()

        default_inp_lang_no  = LANGUAGES.index('English')
        default_outp_lang_no = LANGUAGES.index('Vietnamese')

        # Add a variable to store the current source language and current target language
        self.current_pair_lang = [LANGUAGES_LABEL[default_inp_lang_no], LANGUAGES_LABEL[default_outp_lang_no]]

        input_lang_store = Gtk.ListStore(str)
        for input_lang in LANGUAGES:
            input_lang_store.append([input_lang])
        self.input_lang_combo = Gtk.ComboBox.new_with_model(input_lang_store)
        input_renderer_text = Gtk.CellRendererText()
        self.input_lang_combo.pack_start(input_renderer_text, True)
        self.input_lang_combo.add_attribute(input_renderer_text, 'text', 0)
        self.input_lang_combo.props.active = default_inp_lang_no

        output_lang_store = Gtk.ListStore(str)
        for output_lang in LANGUAGES:
            output_lang_store.append([output_lang])
        self.output_lang_combo = Gtk.ComboBox.new_with_model(output_lang_store)
        output_renderer_text = Gtk.CellRendererText()
        self.output_lang_combo.pack_start(output_renderer_text, True)
        self.output_lang_combo.add_attribute(output_renderer_text, 'text', 0)
        self.output_lang_combo.props.active = default_outp_lang_no

        self.source_lang_box.add(self.input_lang_combo)
        self.target_lang_box.add(self.output_lang_combo)

        # Option bar: 'Swap languages' button
        self.swap_lang_button = Gtk.Button()
        self.swap_lang_button.props.image = Gtk.Image.new_from_file(ICONS['swap-dark'])

        # Option bar: Undo and Redo buttons
        self.undo_button = Gtk.Button()
        self.undo_button.props.image = Gtk.Image.new_from_icon_name('edit-undo-symbolic', Gtk.IconSize.BUTTON)
        self.redo_button = Gtk.Button()
        self.redo_button.props.image = Gtk.Image.new_from_icon_name('edit-redo-symbolic', Gtk.IconSize.BUTTON)

        self.undo_times = 0
        self.undo_button_unavailable = Gtk.MenuButton()
        self.undo_button_unavailable.props.image = Gtk.Image.new_from_icon_name('edit-undo-symbolic', Gtk.IconSize.BUTTON)
        self.redo_button_unavailable = Gtk.MenuButton()
        self.redo_button_unavailable.props.image = Gtk.Image.new_from_icon_name('edit-redo-symbolic', Gtk.IconSize.BUTTON)

        self.undo_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, vexpand=False, hexpand=False, spacing=0)
        self.redo_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, vexpand=False, hexpand=False, spacing=0)
        self.undo_box.add(self.undo_button_unavailable)
        self.redo_box.add(self.redo_button_unavailable)

        # Option bar: 'Clear all source text' button
        self.clear_all_button = Gtk.Button()
        self.clear_all_button.props.image = Gtk.Image.new_from_icon_name('edit-delete-symbolic', Gtk.IconSize.BUTTON)
        self.clear_button_unavailable = Gtk.MenuButton()
        self.clear_button_unavailable.props.image = Gtk.Image.new_from_icon_name('edit-delete-symbolic', Gtk.IconSize.BUTTON)

        self.clear_all_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, vexpand=False, hexpand=False, spacing=0)
        self.clear_all_box.add(self.clear_button_unavailable)

        self.ob_left_space.pack_start(self.undo_box, expand=False, fill=False, padding=0)
        self.ob_left_space.pack_start(self.redo_box, expand=False, fill=False, padding=6)

        self.ob_middle_space.pack_start(self.source_lang_box,  expand=False, fill=False, padding=0)
        self.ob_middle_space.pack_start(self.swap_lang_button, expand=False, fill=False, padding=20)
        self.ob_middle_space.pack_end(self.target_lang_box,    expand=False, fill=False, padding=0)

        self.ob_right_space.pack_end(self.clear_all_box, expand=False, fill=False, padding=0)

        option_bar.pack_start(self.ob_left_space,   expand=True,  fill=True,  padding=0)
        option_bar.pack_start(self.ob_middle_space, expand=False, fill=False, padding=0)
        option_bar.pack_start(self.ob_right_space,  expand=True,  fill=True,  padding=0)

        # Main view area: Input/Output
        self.paned = Gtk.Paned()
        main_view.pack_start(self.paned, True, True, 0)
        self.Paned_Pos = (MIN_WIDTH-4*Row_Spc-200-26)//2
        self.paned.props.position = self.Paned_Pos
        IO_MARGIN = 15
        LARGER_MARGIN_SCALE = 1.5

        # Main view area: Input
        input_frame = Gtk.Frame()
        self.paned.add1(input_frame)
        input_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, vexpand=True, hexpand=True, spacing=10)
        input_frame.add(input_box)

        input_scrollable_area = Gtk.ScrolledWindow()
        input_scrollable_area.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)

        self.input_area = GtkSource.View()
        self.input_area.props.top_margin      = IO_MARGIN
        self.input_area.props.bottom_margin   = IO_MARGIN
        self.input_area.props.left_margin     = LARGER_MARGIN_SCALE*IO_MARGIN
        self.input_area.props.right_margin    = IO_MARGIN
        self.input_area.props.wrap_mode       = Gtk.WrapMode.WORD
        self.input_area.props.editable        = True
        self.input_area.props.cursor_visible  = True
        #self.input_area.props.tab_width       = 4
        #self.input_area.insert_spaces_instead_of_tabs = False

        self.input_area.props.auto_indent     = True
        self.input_area.props.indent_on_tab   = True

        input_scrollable_area.add(self.input_area)
        input_box.pack_start(input_scrollable_area, True, True, 0)

        input_buffer = self.input_area.get_buffer()
        input_buffer.connect('changed', self.on_input_buffer_changed)

        # Main view area: Output
        output_frame = Gtk.Frame()
        self.paned.add2(output_frame)
        output_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, vexpand=True, hexpand=True, spacing=10)
        output_frame.add(output_box)

        output_scrollable_area = Gtk.ScrolledWindow()
        output_scrollable_area.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)

        self.output_area = GtkSource.View()
        self.output_area.props.top_margin     = IO_MARGIN
        self.output_area.props.bottom_margin  = IO_MARGIN
        self.output_area.props.left_margin    = LARGER_MARGIN_SCALE*IO_MARGIN
        self.output_area.props.right_margin   = IO_MARGIN
        self.output_area.props.wrap_mode      = Gtk.WrapMode.WORD
        self.output_area.props.editable       = False
        self.output_area.props.cursor_visible = False
        #self.output_area.props.tab_width      = 4
        #self.output_area.insert_spaces_instead_of_tabs = False

        output_scrollable_area.add(self.output_area)
        output_box.pack_start(output_scrollable_area, True, True, 0)

        self.print_error_to_IO()

        # TODO: change the background and text color of TextView
        IO_OPACITY = 0.05
        self.input_area.override_background_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(1, 1, 1, IO_OPACITY))
        self.output_area.override_background_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(1, 1, 1, IO_OPACITY))

        """Add a button to trigger the action of program"""
        activation_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, vexpand=True, hexpand=True, spacing=10)
        activation_box.set_size_request(0, 50)
        grid.attach(activation_box, 3, 3, 1, 1)

        self.activation_button = Gtk.Button()
        self.activation_button.props.label = FUNCTION[self.app.mode]
        self.activation_button.connect('clicked', self.on_button_clicked)
        activation_box.pack_start(self.activation_button, True, True, 350)

        """Store the current status of each modes"""
        self.previous_mode = 1
        # Editing buttons - default state
        self.button_state_1 = {'save': False, 'undo-time': self.undo_times, 'undo': False, 'redo': False, 'clear-all': False}
        self.button_state_2 = {'save': False, 'undo-time': self.undo_times, 'undo': False, 'redo': False, 'clear-all': False}

        # [input_buffer, output_buffer, paned_position, error_no]
        self.IO_history_1 = [GtkSource.Buffer(), GtkSource.Buffer(), self.Paned_Pos, 0]
        self.IO_history_1[0].connect('changed', self.on_input_buffer_changed)
        self.IO_history_2 = [GtkSource.Buffer(), GtkSource.Buffer(), self.Paned_Pos, 0]
        self.IO_history_2[0].connect('changed', self.on_input_buffer_changed)

        """Create shortcuts"""
        self.app.create_action('save_to_text_file', self.on_save_to_file_clicked, ['<primary>s'])
        self.app.create_action('lang-swap',         self.on_Swap_clicked,         ['<primary><shift>s'])
        self.app.create_action('undo',              self.on_Undo_clicked,         ['<primary>z'])
        self.app.create_action('redo',              self.on_Redo_clicked,         ['<primary>y'])
        self.app.create_action('trigger_action_1',  self.on_button_clicked,       ['<shift>Return'])
        self.app.create_action('trigger_action_2',  self.on_button_clicked,       ['<primary>Return'])

        """Connect widgets to function"""
        self.dark_theme_button .connect('clicked',       self.dark_theme_button_clicked)
        self.saving_button     .connect('clicked',       self.on_save_to_file_clicked)
        self.function_list     .connect('row_activated', self.on_row_activated)
        self.input_lang_combo  .connect('changed',       self.on_input_lang_changed)
        self.output_lang_combo .connect('changed',       self.on_output_lang_changed)
        self.swap_lang_button  .connect('clicked',       self.on_Swap_clicked)
        self.undo_button       .connect('clicked',       self.on_Undo_clicked)
        self.redo_button       .connect('clicked',       self.on_Redo_clicked)
        self.refresh_button    .connect('clicked',       self.on_Refresh_clicked)
        self.clear_all_button  .connect('clicked',       self.on_Clear_all_clicked)
        new_window_button      .connect('clicked',       self.start_new_window)

    """Feature: Display default output or error notifications"""
    def print_error_to_IO(self, activated=True, same_IO=False):
        """Set default text for output, if the input is empty, or if program gets an error.
        Called when the input buffer or mode (left sidebar) is changed.
        Set activated to False if you want to turn off this feature.
        """
        if not activated: return   
        if self.app.error_no == 1 and same_IO == False:
            self.set_Save_button_active(True)
            return

        temp_buffer = GtkSource.Buffer()
        italic_tag = temp_buffer.create_tag('italic', style=Pango.Style.ITALIC)

        if self.app.error_no == 0 or same_IO == True:
            self.set_Save_button_active(False)
            temp_buffer.props.text = DEFAULT_OUTPUT[self.app.mode]
            temp_buffer.apply_tag(italic_tag, temp_buffer.get_start_iter(), temp_buffer.get_end_iter())
            self.output_area.set_buffer(temp_buffer)
        elif self.app.error_no == 2:
            self.set_Save_button_active(False)
            temp_buffer.props.text = ERROR_NOTIF['connection_prob']
            temp_buffer.apply_tag(italic_tag, temp_buffer.get_start_iter(), temp_buffer.get_end_iter())
            #temp_buffer.connect('changed', self.on_input_buffer_changed)
            self.input_area.set_buffer(temp_buffer)
            self.input_area.props.editable        = False
            self.input_area.props.cursor_visible  = False
            self.paned.props.position = 2*self.Paned_Pos+20
            self.output_set_text('')
            #self.client.connect()

            self.set_Undo_button_active(False)
            self.set_Redo_button_active(False)
            self.set_Clear_all_button_active(False)

    '''
    #self.connect('key-press-event', self.key_press_event_Redo)
    # This function is replaced by app.create_action(name, callback, shortcuts)
    def key_press_event_Redo(self, widget, event):
        """Add shortcut Ctr+Y for Redo"""
        keyval_name = Gdk.keyval_name(event.keyval)
        ctrl = (event.state & Gdk.ModifierType.CONTROL_MASK)
        text_buffer = self.input_area.get_buffer()
        if ctrl and keyval_name == 'y':
            if text_buffer.can_redo():
                text_buffer.do_redo(text_buffer)
    '''

    """Feature: Set state 'turn on' - 'turn off' for Editing buttons"""
    def set_Save_button_active(self, turn_on):
        if turn_on == True:
            if self.saving_button_inactive in self.preferences_box:
                self.preferences_box.remove(self.saving_button_inactive)
            if self.saving_button not in self.preferences_box:
                self.preferences_box.add(self.saving_button)
        else:
            if self.saving_button in self.preferences_box:
                self.preferences_box.remove(self.saving_button)
            if self.saving_button_inactive not in self.preferences_box:
                self.preferences_box.add(self.saving_button_inactive)
        self.preferences_box.show_all()

    def set_Undo_button_active(self, turn_on):
        if turn_on == True:
            if self.undo_button_unavailable in self.undo_box:
                self.undo_box.remove(self.undo_button_unavailable)
            if self.undo_button not in self.undo_box:
                self.undo_box.add(self.undo_button)
        else:
            if self.undo_button in self.undo_box:
                self.undo_box.remove(self.undo_button)
            if self.undo_button_unavailable not in self.undo_box:
                self.undo_box.add(self.undo_button_unavailable)
        self.undo_box.show_all()

    def set_Redo_button_active(self, turn_on):
        if turn_on == True:
            if self.redo_button_unavailable in self.redo_box:
                self.redo_box.remove(self.redo_button_unavailable)
            if self.redo_button not in self.redo_box:
                self.redo_box.add(self.redo_button)
        else:
            if self.redo_button in self.redo_box:
                self.redo_box.remove(self.redo_button)
            if self.redo_button_unavailable not in self.redo_box:
                self.redo_box.add(self.redo_button_unavailable)
        self.redo_box.show_all()

    def set_Clear_all_button_active(self, turn_on):
        if turn_on == True:
            if self.clear_button_unavailable in self.clear_all_box:
                self.clear_all_box.remove(self.clear_button_unavailable)
            if self.clear_all_button not in self.clear_all_box:
                self.clear_all_box.add(self.clear_all_button)
        else:
            if self.clear_all_button in self.clear_all_box:
                self.clear_all_box.remove(self.clear_all_button)
            if self.clear_button_unavailable not in self.clear_all_box:
                self.clear_all_box.add(self.clear_button_unavailable)
        self.clear_all_box.show_all()

    def set_Editing_buttons_active(self, state):
        self.set_Save_button_active(state['save'])
        self.undo_times = state['undo-time']
        self.set_Undo_button_active(state['undo'])
        self.set_Redo_button_active(state['redo'])
        self.set_Clear_all_button_active(state['clear-all'])

    def get_Editing_buttons_state(self):
        state = {'save': False, 'undo-time': self.undo_times, 'undo': False, 'redo': False, 'clear-all': False}
        state['save']      = self.saving_button    in self.preferences_box
        state['undo-time'] = self.undo_times
        state['undo']      = self.undo_button      in self.undo_box
        state['redo']      = self.redo_button      in self.redo_box
        state['clear-all'] = self.clear_all_button in self.clear_all_box
        return state

    """Features: Undo-Redo"""
    def on_input_buffer_changed(self, input_buffer):
        self.set_Undo_button_active(True)
        if input_buffer.props.text == '':
            self.set_Clear_all_button_active(False)
        else:
            self.set_Clear_all_button_active(True)

    def on_Undo_clicked(self, button, _ = None):
        """Called when user clicks the Undo button"""
        text_buffer = self.input_area.get_buffer()
        if text_buffer.can_undo():
            text_buffer.undo()
            self.undo_times += 1
        else:
            self.set_Undo_button_active(False)

        #print(self.undo_times)
        if self.undo_times != 0:
            self.set_Redo_button_active(True)
        else:
            self.set_Redo_button_active(False)

    def on_Redo_clicked(self, button, _ = None):
        """Called when user clicks the Redo button"""
        text_buffer = self.input_area.get_buffer()
        if text_buffer.can_redo():
            text_buffer.redo()
            self.undo_times -= 1
        else:
            self.undo_times = 0

        #print(self.undo_times)
        if self.undo_times != 0:
            self.set_Redo_button_active(True)
        else:
            self.set_Redo_button_active(False)

    """Feature: Refresh"""
    def on_Refresh_clicked(self, button, _ = None):
        """Called when user clicks the Redo button"""
        self.paned.props.position = self.Paned_Pos
        if self.app.error_no != 0:
            self.on_button_clicked()

    """Feature: Clear all source text"""
    def on_Clear_all_clicked(self, button):
        """Called when user clicks the 'Clear all source text' button"""
        self.input_set_text('')
        if self.app.error_no == 0 or self.app.error_no == 1:
            self.app.error_no = 0
            if self.app.mode == 1:
                self.check_IO_lang_supported()

    """Feature: Save output to text file"""    
    def on_save_to_file_clicked(self, widget, _ = None):
        """Called when user clicks the 'Save output to text file' menu button"""
        if self.app.error_no == 0 or self.app.error_no == 2:
            return
        save_buffer = self.output_area.get_buffer()
        save_text = save_buffer.get_text(save_buffer.get_start_iter(), save_buffer.get_end_iter(), False)

        # Open a FileChooserDialog to create a new file to save output to
        dialog = Gtk.FileChooserDialog(title='Export output to a file', parent=self, action=Gtk.FileChooserAction.SAVE)
        dialog.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_SAVE, Gtk.ResponseType.OK)
        # Todo: change the color of the SAVE button

        dialog.set_default_size(800, 400)
        dialog.set_transient_for(self)
        dialog.set_current_name('untitled.txt')

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            # Save output to the text file
            filename = dialog.get_filename()
            with open(filename, 'a') as f:
                f.write(save_text+'\n')
        dialog.destroy()

    """Feature: TRANSLATOR - Input language choosing"""
    def get_current_lang(self, combobox):
        tree_iter = combobox.get_active_iter()
        if tree_iter is not None:
            curr_model = combobox.get_model()
            lang = curr_model[tree_iter][0]
            lang_no = LANGUAGES.index(lang)
            return LANGUAGES_LABEL[lang_no]
        return None

    def on_input_lang_changed(self, combobox):
        """Called when user choose the language to translate from."""
        self.current_pair_lang[0] = self.get_current_lang(combobox)
        #print(self.current_pair_lang)
        self.check_IO_lang_supported()

    """Feature: TRANSLATOR - Output language choosing"""
    def on_output_lang_changed(self, combobox):
        """Called when user choose the language to translate to."""
        self.current_pair_lang[1] = self.get_current_lang(combobox)
        #print(self.current_pair_lang)
        self.check_IO_lang_supported()

    """Feature: TRANSLATOR - Input-output languages swap"""
    def on_Swap_clicked(self, widget, _ = None):
        """Called when user clicks the 'Swap' button."""
        inp_lang_no  = LANGUAGES_LABEL.index(self.get_current_lang(self.input_lang_combo))
        outp_lang_no = LANGUAGES_LABEL.index(self.get_current_lang(self.output_lang_combo))

        inp_lang_no, outp_lang_no = outp_lang_no, inp_lang_no
        self.input_lang_combo.props.active = inp_lang_no
        self.output_lang_combo.props.active = outp_lang_no
        #print(self.current_pair_lang)
        self.check_IO_lang_supported()

    def check_IO_lang_supported(self):
        """Handles choosed input-output languages, determines if the choosing is supported by program.
        Called when input or output language or when mode of program is changed.
        Args: current_pair_lang[curr_inp_lang, curr_outp_lang]
        """
        if self.app.error_no != 2:
            inp_lang = self.current_pair_lang[0]
            outp_lang = self.current_pair_lang[1]

            if inp_lang == outp_lang or (inp_lang, outp_lang) in SUPPORTED_TRANS:
                self.input_area.props.editable        = True
                self.input_area.props.cursor_visible  = True
                self.print_error_to_IO(same_IO=(inp_lang == outp_lang))
                return True

            ERR_notification =  ERROR_NOTIF['unsupported_lang_01'] + LANGUAGES[LANGUAGES_LABEL.index(inp_lang)]
            ERR_notification += ERROR_NOTIF['unsupported_lang_02'] + LANGUAGES[LANGUAGES_LABEL.index(outp_lang)]
            ERR_notification += ERROR_NOTIF['unsupported_lang_03']

            temp_buffer = GtkSource.Buffer()
            italic_tag = temp_buffer.create_tag('italic', style=Pango.Style.ITALIC)
            temp_buffer.props.text = ERR_notification
            temp_buffer.apply_tag(italic_tag, temp_buffer.get_start_iter(), temp_buffer.get_end_iter())
            self.output_area.set_buffer(temp_buffer)
            self.input_area.props.editable        = False
            self.input_area.props.cursor_visible  = False
            return False
        else:
            self.print_error_to_IO()
            return False

    """Feature: Handle input and display output"""
    def input_set_text(self, str = ''):
        input_buffer = self.input_area.get_buffer()
        input_buffer.remove_all_tags(input_buffer.get_start_iter(), input_buffer.get_end_iter())
        input_buffer.props.text = str

    def output_set_text(self, str = ''):
        output_buffer = self.output_area.get_buffer()
        output_buffer.remove_all_tags(output_buffer.get_start_iter(), output_buffer.get_end_iter())
        output_buffer.props.text = str

    """Feature: Program funtions choosing"""        
    def on_row_activated(self, widget, _):
        """Set mode for program.
        Called when the user chooses the function on the left sidebar.
        """
        current_row = self.function_list.get_selected_row()
        self.app.mode = 1+current_row.get_index()
        self.activation_button.props.label = FUNCTION[self.app.mode]
        self.activation_button.show_all()
        #self.print_error_to_IO()
        if self.app.mode == 1:
            if self.previous_mode == 2:
                self.button_state_2 = self.get_Editing_buttons_state()
                self.set_Editing_buttons_active(self.button_state_1)
                self.IO_history_2 = [self.input_area.get_buffer(), self.output_area.get_buffer(), self.paned.props.position, self.app.error_no]
                self.input_area.set_buffer (self.IO_history_1[0])
                self.output_area.set_buffer(self.IO_history_1[1])
                self.paned.props.position = self.IO_history_1[2]
                self.app.error_no         = self.IO_history_1[3]
                self.previous_mode = 1
            self.ob_middle_space.show()
            #self.current_pair_lang[0] = self.get_current_lang(self.input_lang_combo)
            #self.current_pair_lang[1] = self.get_current_lang(self.output_lang_combo)
            self.check_IO_lang_supported()
        elif self.app.mode == 2:
            if self.previous_mode == 1:
                self.button_state_1 = self.get_Editing_buttons_state()
                self.set_Editing_buttons_active(self.button_state_2)
                self.IO_history_1 = [self.input_area.get_buffer(), self.output_area.get_buffer(), self.paned.props.position, self.app.error_no]
                self.input_area.set_buffer (self.IO_history_2[0])
                self.output_area.set_buffer(self.IO_history_2[1])
                self.paned.props.position = self.IO_history_2[2]
                self.app.error_no         = self.IO_history_2[3]
                self.previous_mode = 2
            if self.app.error_no != 2:
                self.input_area.props.editable        = True
                self.input_area.props.cursor_visible  = True
                #self.output_set_text('')
            self.ob_middle_space.hide()
            self.print_error_to_IO()

    def on_button_clicked(self, widget = None, _ = None):
        """Get data from input buffer and display result to output buffer.
        Called when user clicks the 'Translate/Grammar Check' button.
        """
        if self.app.error_no != 2:
            if self.app.mode == 1:
                if self.check_IO_lang_supported() == False:
                    return

            self.current_pair_lang[0] = self.get_current_lang(self.input_lang_combo)
            self.current_pair_lang[1] = self.get_current_lang(self.output_lang_combo)

            input_buffer = self.input_area.get_buffer()
            raw_text_input = input_buffer.get_text(input_buffer.get_start_iter(), input_buffer.get_end_iter(), False)
            # Handle raw text_input
            text_input = raw_text_input.strip()

            if text_input == '':
                self.app.error_no = 0
                raw_text_output = text_input
            else:
                if self.app.mode == 1 and self.current_pair_lang[0] == self.current_pair_lang[1]:
                    self.app.error_no = 1
                    raw_text_output = text_input
                else:
                    raw_text_output = self.app.handle_input(text_input, self.current_pair_lang[0], self.current_pair_lang[1])

            # Handle raw text_output
            text_output = raw_text_output.strip()
            self.output_set_text(text_output)

        self.print_error_to_IO()

    """Feature: Choosing dark mode/ligth mode for UI"""   
    def dark_theme_button_clicked(self, button):
        """Called when user click the dark theme button"""
        self.dark_theme = not self.dark_theme
        self.settings.set_property('gtk-theme-name', THEMES[self.current_theme][self.dark_theme])
        if self.dark_theme == 1:
            self.swap_lang_button.props.image = Gtk.Image.new_from_file(ICONS['swap-dark'])
            self.dark_theme_button.props.image = Gtk.Image.new_from_icon_name('weather-clear-night-symbolic', Gtk.IconSize.MENU)
        else:
            self.swap_lang_button.props.image = Gtk.Image.new_from_file(ICONS['swap-light'])
            self.dark_theme_button.props.image = Gtk.Image.new_from_file(ICONS['light-mode'])

    """Feature: New Window"""
    def start_new_window(self, widget, _ = None):
        POSSIBLE_NAMES = ['main', 'languator*', 'LANGUATOR*', 'Languator*']
        run_in_bg      = ' & disown'
        rm_errs_noti   = ' >/dev/null 2>&1'
        
        for curr_prog_name in POSSIBLE_NAMES:
            os.system('python3 ' + curr_prog_name + '.py'  + rm_errs_noti + run_in_bg + rm_errs_noti)
            os.system('./'       + curr_prog_name          + rm_errs_noti + run_in_bg + rm_errs_noti)
            os.system('./'       + curr_prog_name + '.bin' + rm_errs_noti + run_in_bg + rm_errs_noti)
            os.system('./'       + curr_prog_name + '.run' + rm_errs_noti + run_in_bg + rm_errs_noti)
        # updating ...

    """Feature: Show Shortcuts window"""
    def help_overlay(self, widget, _):
        """Callback for the app.keyboard_shorcuts action."""
        shortcut_window = Gtk.ShortcutsWindow()
        shortcut_window.show_all()

    """Feature: Program settings"""
    def on_preferences_action(self, widget, _):
        """Callback for the app.preferences action."""
        print('Preferences action activated')

    """Feature: Show Help window"""
    def on_help_action(self, widget, _):
        """Callback for the app.help action."""
        print('Help action activated')

    """Feature: Show About window"""
    def show_about(self, widget, _):
        """Callback for the app.about action."""
        about_dialog = Gtk.AboutDialog()
        PROGRAM_LOGO = GdkPixbuf.Pixbuf.new_from_file(LOGO['book'])
        about_dialog.props.logo          = PROGRAM_LOGO
        about_dialog.props.program_name  = PROGRAM_NAME
        about_dialog.props.comments      = DESCRIPTION
        about_dialog.props.version       = CURRENT_VERSION
        about_dialog.props.website_label = 'Website'
        about_dialog.props.website       = WEBSITE
        about_dialog.props.copyright     = COPYRIGHT
        about_dialog.props.license_type  = Gtk.License.GPL_2_0
        about_dialog.props.authors       = AUTHORS

        about_dialog.set_transient_for(self)
        about_dialog.run()
        about_dialog.destroy()
