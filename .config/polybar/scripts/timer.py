#!/usr/bin/env python3
"""
Countdown Timer Widget for i3wm
A transparent desktop widget for countdown timers
"""

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib
import cairo
import math

class CountdownTimer(Gtk.Window):
    def __init__(self):
        super().__init__()
        
        # Timer state
        self.total_seconds = 0  # Total time set
        self.remaining_seconds = 0  # Time remaining
        self.is_running = False
        self.timer_id = None
        
        # View state
        self.view_mode = 'main'  # 'main' or 'set_time'
        self.input_text = ""
        self.input_mode = 'minutes'  # 'minutes' or 'seconds'
        
        # Hover state
        self.hover_button = None  # 'start', 'reset', 'set'
        
        # Window setup
        self.set_title("Countdown Timer")
        self.set_default_size(280, 280)
        self.set_decorated(False)
        self.set_resizable(False)
        
        # Set proper window role
        self.set_role("countdown_timer")
        
        # Make window transparent
        screen = self.get_screen()
        visual = screen.get_rgba_visual()
        if visual and screen.is_composited():
            self.set_visual(visual)
        
        # Set window properties
        self.set_type_hint(Gdk.WindowTypeHint.DESKTOP)
        self.set_keep_below(True)
        self.stick()
        
        # Prevent i3 tiling
        self.set_accept_focus(False)
        self.set_can_focus(False)
        self.set_skip_taskbar_hint(True)
        self.set_skip_pager_hint(True)
        
        # Position window
        display = Gdk.Display.get_default()
        monitor = display.get_primary_monitor()
        geometry = monitor.get_geometry()
        screen_width = geometry.width
        screen_height = geometry.height
        
        x = (screen_width - 280) // 2
        y = (screen_height - 280) // 2 + 150
        self.move(x, y)
        
        # Set up for transparency and drawing
        self.set_app_paintable(True)
        self.connect('draw', self.on_draw)
        self.connect('screen-changed', self.on_screen_changed)
        
        # Create drawing area
        self.drawing_area = Gtk.DrawingArea()
        self.drawing_area.connect('draw', self.on_draw)
        self.drawing_area.add_events(Gdk.EventMask.POINTER_MOTION_MASK | 
                                     Gdk.EventMask.BUTTON_PRESS_MASK |
                                     Gdk.EventMask.LEAVE_NOTIFY_MASK |
                                     Gdk.EventMask.KEY_PRESS_MASK)
        self.drawing_area.connect('motion-notify-event', self.on_mouse_move)
        self.drawing_area.connect('button-press-event', self.on_click)
        self.drawing_area.connect('leave-notify-event', self.on_mouse_leave)
        self.drawing_area.connect('key-press-event', self.on_key_press)
        self.drawing_area.set_can_focus(True)
        self.add(self.drawing_area)
    
    def on_screen_changed(self, widget, old_screen):
        screen = self.get_screen()
        visual = screen.get_rgba_visual()
        if visual and screen.is_composited():
            self.set_visual(visual)
    
    def format_time(self, seconds):
        """Format seconds as MM:SS"""
        mins = seconds // 60
        secs = seconds % 60
        return f"{mins:02d}:{secs:02d}"
    
    def start_timer(self):
        """Start the countdown"""
        if self.remaining_seconds > 0 and not self.is_running:
            self.is_running = True
            self.timer_id = GLib.timeout_add(1000, self.tick)
    
    def pause_timer(self):
        """Pause the countdown"""
        if self.is_running:
            self.is_running = False
            if self.timer_id:
                GLib.source_remove(self.timer_id)
                self.timer_id = None
    
    def reset_timer(self):
        """Reset timer to initial value"""
        self.pause_timer()
        self.remaining_seconds = self.total_seconds
        self.queue_draw()
    
    def tick(self):
        """Countdown tick - called every second"""
        if self.remaining_seconds > 0:
            self.remaining_seconds -= 1
            self.queue_draw()
            
            if self.remaining_seconds == 0:
                self.is_running = False
                # Timer finished - could add sound/notification here
                return False
            return True
        return False
    
    def on_mouse_move(self, widget, event):
        """Handle mouse movement for hover effects"""
        old_hover = self.hover_button
        self.hover_button = None
        
        if self.view_mode == 'main':
            # Check start/pause button
            start_rect = self.get_start_button_rect()
            if (start_rect[0] <= event.x <= start_rect[0] + start_rect[2] and 
                start_rect[1] <= event.y <= start_rect[1] + start_rect[3]):
                self.hover_button = 'start'
            
            # Check reset button
            reset_rect = self.get_reset_button_rect()
            if (reset_rect[0] <= event.x <= reset_rect[0] + reset_rect[2] and 
                reset_rect[1] <= event.y <= reset_rect[1] + reset_rect[3]):
                self.hover_button = 'reset'
            
            # Check set time button
            set_rect = self.get_set_button_rect()
            if (set_rect[0] <= event.x <= set_rect[0] + set_rect[2] and 
                set_rect[1] <= event.y <= set_rect[1] + set_rect[3]):
                self.hover_button = 'set'
        elif self.view_mode == 'set_time':
            # Check done button
            done_rect = self.get_done_button_rect()
            if (done_rect[0] <= event.x <= done_rect[0] + done_rect[2] and 
                done_rect[1] <= event.y <= done_rect[1] + done_rect[3]):
                self.hover_button = 'done'
            
            # Check cancel button
            cancel_rect = self.get_cancel_button_rect()
            if (cancel_rect[0] <= event.x <= cancel_rect[0] + cancel_rect[2] and 
                cancel_rect[1] <= event.y <= cancel_rect[1] + cancel_rect[3]):
                self.hover_button = 'cancel'
        
        if old_hover != self.hover_button:
            self.queue_draw()
    
    def on_mouse_leave(self, widget, event):
        """Handle mouse leaving widget"""
        self.hover_button = None
        self.queue_draw()
    
    def get_start_button_rect(self):
        """Get rectangle for start/pause button"""
        return (65, 200, 60, 30)
    
    def get_reset_button_rect(self):
        """Get rectangle for reset button"""
        return (155, 200, 60, 30)
    
    def get_set_button_rect(self):
        """Get rectangle for set time button"""
        return (240, 15, 25, 25)
    
    def get_done_button_rect(self):
        """Get rectangle for done button"""
        return (50, 210, 80, 30)
    
    def get_cancel_button_rect(self):
        """Get rectangle for cancel button"""
        return (150, 210, 80, 30)
    
    def on_click(self, widget, event):
        """Handle mouse clicks"""
        if self.view_mode == 'main':
            # Check start/pause button
            start_rect = self.get_start_button_rect()
            if (start_rect[0] <= event.x <= start_rect[0] + start_rect[2] and 
                start_rect[1] <= event.y <= start_rect[1] + start_rect[3]):
                if self.is_running:
                    self.pause_timer()
                else:
                    self.start_timer()
                return True
            
            # Check reset button
            reset_rect = self.get_reset_button_rect()
            if (reset_rect[0] <= event.x <= reset_rect[0] + reset_rect[2] and 
                reset_rect[1] <= event.y <= reset_rect[1] + reset_rect[3]):
                self.reset_timer()
                return True
            
            # Check set time button
            set_rect = self.get_set_button_rect()
            if (set_rect[0] <= event.x <= set_rect[0] + set_rect[2] and 
                set_rect[1] <= event.y <= set_rect[1] + set_rect[3]):
                self.open_set_time()
                return True
        
        elif self.view_mode == 'set_time':
            # Check done button
            done_rect = self.get_done_button_rect()
            if (done_rect[0] <= event.x <= done_rect[0] + done_rect[2] and 
                done_rect[1] <= event.y <= done_rect[1] + done_rect[3]):
                self.apply_time()
                return True
            
            # Check cancel button
            cancel_rect = self.get_cancel_button_rect()
            if (cancel_rect[0] <= event.x <= cancel_rect[0] + cancel_rect[2] and 
                cancel_rect[1] <= event.y <= cancel_rect[1] + cancel_rect[3]):
                self.cancel_set_time()
                return True
        
        return False
    
    def open_set_time(self):
        """Open set time view"""
        self.pause_timer()
        self.view_mode = 'set_time'
        self.input_text = ""
        self.input_mode = 'minutes'
        self.set_accept_focus(True)
        self.set_can_focus(True)
        self.drawing_area.grab_focus()
        self.queue_draw()
    
    def cancel_set_time(self):
        """Cancel setting time"""
        self.view_mode = 'main'
        self.set_accept_focus(False)
        self.set_can_focus(False)
        self.queue_draw()
    
    def apply_time(self):
        """Apply the set time"""
        try:
            if self.input_text:
                value = int(self.input_text)
                if self.input_mode == 'minutes':
                    self.total_seconds = value * 60
                else:
                    self.total_seconds = value
                self.remaining_seconds = self.total_seconds
        except ValueError:
            pass
        
        self.view_mode = 'main'
        self.set_accept_focus(False)
        self.set_can_focus(False)
        self.queue_draw()
    
    def on_key_press(self, widget, event):
        """Handle keyboard input"""
        if self.view_mode != 'set_time':
            return False
        
        keyval = event.keyval
        keyname = Gdk.keyval_name(keyval)
        
        if keyname in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
            if len(self.input_text) < 4:
                self.input_text += keyname
                self.queue_draw()
        elif keyname == 'BackSpace':
            if len(self.input_text) > 0:
                self.input_text = self.input_text[:-1]
                self.queue_draw()
        elif keyname == 'Return' or keyname == 'KP_Enter':
            self.apply_time()
        elif keyname == 'Escape':
            self.cancel_set_time()
        elif keyname == 'm' or keyname == 'M':
            self.input_mode = 'minutes'
            self.queue_draw()
        elif keyname == 's' or keyname == 'S':
            self.input_mode = 'seconds'
            self.queue_draw()
        
        return True
    
    def on_draw(self, widget, cr):
        """Draw the widget"""
        # Make background transparent
        cr.set_source_rgba(0, 0, 0, 0)
        cr.set_operator(cairo.OPERATOR_SOURCE)
        cr.paint()
        
        if self.view_mode == 'set_time':
            self.draw_set_time_view(cr)
        else:
            self.draw_main_view(cr)
        
        return False
    
    def draw_main_view(self, cr):
        """Draw main timer view"""
        # Draw background panel
        cr.set_source_rgba(0.1, 0.1, 0.1, 0.7)
        cr.rectangle(10, 10, 260, 260)
        cr.fill()
        
        # Draw set time button (gear icon)
        self.draw_set_button(cr)
        
        # Draw time display
        time_str = self.format_time(self.remaining_seconds)
        cr.set_source_rgba(1, 1, 1, 1)
        cr.select_font_face("Fira Code", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        cr.set_font_size(64)
        extents = cr.text_extents(time_str)
        cr.move_to(140 - extents.width/2, 140)
        cr.show_text(time_str)
        
        # Draw control buttons
        self.draw_start_button(cr)
        self.draw_reset_button(cr)
    
    def draw_set_time_view(self, cr):
        """Draw set time view"""
        # Draw background panel
        cr.set_source_rgba(0.1, 0.1, 0.1, 0.7)
        cr.rectangle(10, 10, 260, 260)
        cr.fill()
        
        # Draw title
        cr.set_source_rgba(1, 1, 1, 0.9)
        cr.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        cr.set_font_size(18)
        cr.move_to(20, 40)
        cr.show_text("Set Timer")
        
        # Draw mode selector
        cr.set_font_size(12)
        cr.set_source_rgba(1, 1, 1, 0.7)
        cr.move_to(20, 70)
        cr.show_text("Press M for minutes, S for seconds")
        
        # Draw current mode
        mode_text = "Minutes" if self.input_mode == 'minutes' else "Seconds"
        cr.set_source_rgba(0.2, 0.8, 0.2, 1)
        cr.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        cr.set_font_size(14)
        cr.move_to(20, 95)
        cr.show_text(f"Mode: {mode_text}")
        
        # Draw input box
        cr.set_source_rgba(0.15, 0.15, 0.15, 0.8)
        self.rounded_rectangle(cr, 40, 110, 200, 60, 5)
        cr.fill()
        
        # Draw border
        cr.set_source_rgba(0.2, 0.8, 0.2, 0.6)
        cr.set_line_width(2)
        self.rounded_rectangle(cr, 40, 110, 200, 60, 5)
        cr.stroke()
        
        # Draw input text
        display_text = self.input_text if self.input_text else "0"
        cr.set_source_rgba(1, 1, 1, 1)
        cr.select_font_face("Fira Code", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        cr.set_font_size(36)
        extents = cr.text_extents(display_text)
        cr.move_to(140 - extents.width/2, 155)
        cr.show_text(display_text)
        
        # Draw buttons
        self.draw_done_button(cr)
        self.draw_cancel_button(cr)
    
    def draw_progress_circle(self, cr, cx, cy, radius, progress):
        """Draw circular progress indicator"""
        # Background circle
        cr.set_source_rgba(0.2, 0.2, 0.2, 0.3)
        cr.set_line_width(6)
        cr.arc(cx, cy, radius, 0, 2 * math.pi)
        cr.stroke()
        
        # Progress arc
        if progress > 0:
            cr.set_source_rgba(0.2, 0.8, 0.2, 0.8)
            cr.set_line_width(6)
            start_angle = -math.pi / 2
            end_angle = start_angle + (2 * math.pi * progress)
            cr.arc(cx, cy, radius, start_angle, end_angle)
            cr.stroke()
    
    def draw_set_button(self, cr):
        """Draw set time button (gear icon)"""
        btn_x, btn_y, btn_w, btn_h = self.get_set_button_rect()
        
        # Button background
        if self.hover_button == 'set':
            cr.set_source_rgba(0.3, 0.3, 0.3, 0.8)
        else:
            cr.set_source_rgba(0.2, 0.2, 0.2, 0.6)
        
        cr.arc(btn_x + btn_w/2, btn_y + btn_h/2, btn_w/2, 0, 2 * math.pi)
        cr.fill()
        
        # Gear icon (simplified)
        cr.set_source_rgba(1, 1, 1, 0.9)
        cr.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        cr.set_font_size(16)
        cr.move_to(btn_x + 6, btn_y + 18)
        cr.show_text("⚙")
    
    def draw_start_button(self, cr):
        """Draw start/pause button"""
        btn_x, btn_y, btn_w, btn_h = self.get_start_button_rect()
        
        # Button background
        if self.hover_button == 'start':
            cr.set_source_rgba(0.2, 0.8, 0.2, 0.8)
        else:
            cr.set_source_rgba(0.2, 0.6, 0.2, 0.6)
        
        self.rounded_rectangle(cr, btn_x, btn_y, btn_w, btn_h, 3)
        cr.fill()
        
        # Button text
        cr.set_source_rgba(1, 1, 1, 1)
        cr.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        cr.set_font_size(12)
        text = "Pause" if self.is_running else "Start"
        extents = cr.text_extents(text)
        cr.move_to(btn_x + (btn_w - extents.width) / 2, btn_y + (btn_h + extents.height) / 2 - 1)
        cr.show_text(text)
    
    def draw_reset_button(self, cr):
        """Draw reset button"""
        btn_x, btn_y, btn_w, btn_h = self.get_reset_button_rect()
        
        # Button background
        if self.hover_button == 'reset':
            cr.set_source_rgba(0.8, 0.3, 0.2, 0.8)
        else:
            cr.set_source_rgba(0.6, 0.2, 0.2, 0.6)
        
        self.rounded_rectangle(cr, btn_x, btn_y, btn_w, btn_h, 3)
        cr.fill()
        
        # Button text
        cr.set_source_rgba(1, 1, 1, 1)
        cr.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        cr.set_font_size(12)
        text = "Reset"
        extents = cr.text_extents(text)
        cr.move_to(btn_x + (btn_w - extents.width) / 2, btn_y + (btn_h + extents.height) / 2 - 1)
        cr.show_text(text)
    
    def draw_done_button(self, cr):
        """Draw done button"""
        btn_x, btn_y, btn_w, btn_h = self.get_done_button_rect()
        
        # Button background
        if self.hover_button == 'done':
            cr.set_source_rgba(0.2, 0.8, 0.2, 0.8)
        else:
            cr.set_source_rgba(0.2, 0.6, 0.2, 0.6)
        
        self.rounded_rectangle(cr, btn_x, btn_y, btn_w, btn_h, 3)
        cr.fill()
        
        # Button text
        cr.set_source_rgba(1, 1, 1, 1)
        cr.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        cr.set_font_size(12)
        text = "Done"
        extents = cr.text_extents(text)
        cr.move_to(btn_x + (btn_w - extents.width) / 2, btn_y + (btn_h + extents.height) / 2 - 1)
        cr.show_text(text)
    
    def draw_cancel_button(self, cr):
        """Draw cancel button"""
        btn_x, btn_y, btn_w, btn_h = self.get_cancel_button_rect()
        
        # Button background
        if self.hover_button == 'cancel':
            cr.set_source_rgba(0.8, 0.3, 0.2, 0.8)
        else:
            cr.set_source_rgba(0.6, 0.2, 0.2, 0.6)
        
        self.rounded_rectangle(cr, btn_x, btn_y, btn_w, btn_h, 3)
        cr.fill()
        
        # Button text
        cr.set_source_rgba(1, 1, 1, 1)
        cr.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        cr.set_font_size(12)
        text = "Cancel"
        extents = cr.text_extents(text)
        cr.move_to(btn_x + (btn_w - extents.width) / 2, btn_y + (btn_h + extents.height) / 2 - 1)
        cr.show_text(text)
    
    def rounded_rectangle(self, cr, x, y, width, height, radius):
        """Draw a rounded rectangle path"""
        cr.new_path()
        cr.arc(x + radius, y + radius, radius, math.pi, 3 * math.pi / 2)
        cr.arc(x + width - radius, y + radius, radius, 3 * math.pi / 2, 0)
        cr.arc(x + width - radius, y + height - radius, radius, 0, math.pi / 2)
        cr.arc(x + radius, y + height - radius, radius, math.pi / 2, math.pi)
        cr.close_path()

def main():
    win = CountdownTimer()
    win.connect('destroy', Gtk.main_quit)
    win.show_all()
    
    window = win.get_window()
    if window:
        window.set_role("countdown_timer")
    
    Gtk.main()

if __name__ == '__main__':
    main()

