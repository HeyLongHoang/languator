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

import sys
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gio', '2.0')

import random

from gi.repository import Gtk, Gio

from data.window import *
from client import *
import client_core as core

class LanguatorApplication(Gtk.Application):
    """The main application singleton class."""

    def __init__(self, current_client, session):
        super().__init__(application_id='org.gnome.languator'+session, flags=Gio.ApplicationFlags.FLAGS_NONE)
        window = None
        self.client = current_client

        """error_no - represents the current state of program.
        Changed each time user clicks the 'Translate/Grammar Check' button.
        """
        # error_no = 0 - program is working normally, output area is empty
        # error_no = 1 - program is working normally, output area is not empty
        # error_no = 2 - program got an error and stopped
        # Initially: error_no = 0

        self.error_no = 0

        """mode - decides the current function of program: FUNCTION[mode]
        Changed when user chooses the function of program (on the left side bar).
        """
        # signal - sent to server, representing the current mode
        # mode = 1: TRANSLATOR       ->  signal = 0
        # mode = 2: GRAMMAR CHECKER  ->  signal = 1
        # Initially: mode = 1: TRANSLATOR

        self.mode = 1

    def do_activate(self):
        """Called when the application is activated."""
        # We only allow a single window and raise any existing ones
        window = self.props.active_window
        if not window:
            window = MainWindow(self)
            window.show_all()
        window.present()

    def create_action(self, name, callback, shortcuts=None):
        """Add an application action.
        Args:
            + name:      the name of the action
            + callback:  the function to be called when the action is activated
            + shortcuts: an optional list of accelerators
        """
        action = Gio.SimpleAction.new(name, None)
        action.connect('activate', callback)
        self.add_action(action)
        if shortcuts:
            self.set_accels_for_action(f'app.{name}', shortcuts)

    def handle_input(self, input_str, source_lang_label, target_lang_label):
        """ Main function of program to handle input and show output data.
        Called from 'on_button_clicked()' when user clicks the 'Translate/Grammer Check' button.
        """
        signal = str(self.mode-1)
        source_lang_no = core.LANG_STOI[source_lang_label]
        target_lang_no = core.LANG_STOI[target_lang_label]
        self.client.send_message(input_str, signal, source_lang_no, target_lang_no)
        output_str = self.client.receive_message()
        if output_str != None:
            if output_str.strip() == '':
                self.error_no = 0
            else:
                self.error_no = 1
        else:
            self.error_no = 2
            output_str = ''
        return output_str.strip()

    def on_quit_action(self, widget, _):
        """Callback for the app.quit action."""
        self.quit()

"""The application's entry point."""
if __name__ == "__main__":
    client_01 = Client(core.SERVER_IP, core.SERVER_PORT)
    session = str(random.randint(0,99))
    app_01 = LanguatorApplication(client_01, session)
    app_01.run(sys.argv)