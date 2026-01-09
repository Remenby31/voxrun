#!/usr/bin/env python3
"""Modern minimal overlay for Voxtral - layer-shell for proper positioning."""

import sys
import os

# Force layer-shell to load first
os.environ['LD_PRELOAD'] = '/usr/lib/libgtk4-layer-shell.so'

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Gtk4LayerShell', '1.0')
from gi.repository import Gtk, GLib, Gdk, Gtk4LayerShell

CSS = """
window {
    background-color: transparent;
}
.overlay-box {
    background-color: alpha(#1e1e2e, 0.92);
    border-radius: 10px;
    padding: 14px 24px;
    border: 1px solid alpha(#45475a, 0.6);
}
.recording .overlay-box {
    border: 1px solid alpha(#f38ba8, 0.5);
}
.processing .overlay-box {
    border: 1px solid alpha(#fab387, 0.5);
}
.title {
    color: #cdd6f4;
    font-size: 14px;
    font-weight: 500;
}
.subtitle {
    color: #6c7086;
    font-size: 11px;
    margin-top: 2px;
}
.recording .dot { color: #f38ba8; }
.processing .dot { color: #fab387; }
"""


class VoxtralOverlay(Gtk.Application):
    def __init__(self, text: str, status: str = "result", duration: int = 5000):
        super().__init__(application_id=None)
        self.text = text
        self.status = status
        self.duration = duration

    def do_activate(self):
        css_provider = Gtk.CssProvider()
        css_provider.load_from_string(CSS)
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

        window = Gtk.ApplicationWindow(application=self)
        window.set_decorated(False)
        window.add_css_class(self.status)

        # Layer shell - overlay that doesn't block input
        Gtk4LayerShell.init_for_window(window)
        Gtk4LayerShell.set_layer(window, Gtk4LayerShell.Layer.OVERLAY)
        Gtk4LayerShell.set_anchor(window, Gtk4LayerShell.Edge.BOTTOM, True)
        Gtk4LayerShell.set_margin(window, Gtk4LayerShell.Edge.BOTTOM, 40)
        Gtk4LayerShell.set_keyboard_mode(window, Gtk4LayerShell.KeyboardMode.NONE)
        Gtk4LayerShell.set_exclusive_zone(window, -1)  # Don't reserve space

        # Content
        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        box.add_css_class("overlay-box")

        if self.status == "recording":
            dot = Gtk.Label(label="●")
            dot.add_css_class("dot")
            dot.add_css_class("title")
            box.append(dot)

            text_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
            title = Gtk.Label(label="Enregistrement")
            title.add_css_class("title")
            title.set_halign(Gtk.Align.START)
            text_box.append(title)

            sub = Gtk.Label(label="Appuyez pour transcrire")
            sub.add_css_class("subtitle")
            sub.set_halign(Gtk.Align.START)
            text_box.append(sub)
            box.append(text_box)

        elif self.status == "processing":
            dot = Gtk.Label(label="◐")
            dot.add_css_class("dot")
            dot.add_css_class("title")
            box.append(dot)

            title = Gtk.Label(label="Transcription...")
            title.add_css_class("title")
            box.append(title)

        else:
            title = Gtk.Label(label=self.text)
            title.add_css_class("title")
            title.set_wrap(True)
            title.set_max_width_chars(50)
            title.set_halign(Gtk.Align.CENTER)
            box.append(title)

        window.set_child(box)
        window.present()

        if self.status == "result":
            GLib.timeout_add(self.duration, self.quit)


def main():
    if len(sys.argv) < 2:
        print("Usage: voxtral_overlay.py <text> [status] [duration_ms]")
        sys.exit(1)

    text = sys.argv[1]
    status = sys.argv[2] if len(sys.argv) > 2 else "result"
    duration = int(sys.argv[3]) if len(sys.argv) > 3 else 5000

    app = VoxtralOverlay(text, status, duration)
    app.run([])


if __name__ == "__main__":
    main()
