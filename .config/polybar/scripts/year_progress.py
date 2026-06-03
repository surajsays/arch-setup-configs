#!/usr/bin/env python3
"""
Year Progress Widget for i3wm
A transparent desktop widget showing progress through the year
"""

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib
import cairo
import datetime
import math

class YearProgressWidget(Gtk.Window):
    def __init__(self):
        super().__init__()
        
        # Set window class for i3 identification
        self.set_wmclass("year-progress-widget", "YearProgressWidget")
        
        # Window setup
        self.set_title("Year Progress")
        self.set_default_size(320, 420)
        self.set_decorated(False)
        self.set_resizable(False)
        
        # Make window transparent
        screen = self.get_screen()
        visual = screen.get_rgba_visual()
        if visual and screen.is_composited():
            self.set_visual(visual)
        
        # Set window properties for desktop widget behavior
        self.set_type_hint(Gdk.WindowTypeHint.DESKTOP)  # Behaves like desktop background
        self.set_keep_below(True)  # Stay below all windows
        self.stick()  # Present on all workspaces
        
        # Make window click-through and prevent i3 tiling
        self.set_accept_focus(False)
        self.set_can_focus(False)
        self.set_skip_taskbar_hint(True)
        self.set_skip_pager_hint(True)
        
        # Position window (top-right corner with some margin)
        # Get screen dimensions properly
        display = Gdk.Display.get_default()
        monitor = display.get_primary_monitor()
        geometry = monitor.get_geometry()
        screen_width = geometry.width
        
        self.move(screen_width - 340, 10)
        
        # Set up input shape for click-through
        self.set_app_paintable(True)
        self.connect('draw', self.on_draw)
        self.connect('screen-changed', self.on_screen_changed)
        
        # Calculate year data
        self.update_year_data()
        
        # Create drawing area
        self.drawing_area = Gtk.DrawingArea()
        self.drawing_area.connect('draw', self.on_draw)
        self.add(self.drawing_area)
        
        # Update daily at midnight
        self.schedule_daily_update()
        
    def on_screen_changed(self, widget, old_screen):
        screen = self.get_screen()
        visual = screen.get_rgba_visual()
        if visual and screen.is_composited():
            self.set_visual(visual)
    
    def update_year_data(self):
        """Calculate current year progress data"""
        now = datetime.datetime.now()
        self.year = now.year
        self.is_leap = (self.year % 4 == 0 and self.year % 100 != 0) or (self.year % 400 == 0)
        self.total_days = 366 if self.is_leap else 365
        
        # Calculate day of year (1-365/366)
        start_of_year = datetime.datetime(self.year, 1, 1)
        self.current_day = (now - start_of_year).days + 1
        
        # Calculate progress percentage
        self.progress = (self.current_day / self.total_days) * 100
        
    def on_draw(self, widget, cr):
        """Draw the widget"""
        # Make background transparent
        cr.set_source_rgba(0, 0, 0, 0)
        cr.set_operator(cairo.OPERATOR_SOURCE)
        cr.paint()
        
        # Draw semi-transparent background panel
        cr.set_source_rgba(0.1, 0.1, 0.1, 0.7)
        cr.rectangle(10, 10, 300, 400)
        cr.fill()
        
        # Draw title
        cr.set_source_rgba(1, 1, 1, 0.9)
        cr.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        cr.set_font_size(20)
        cr.move_to(20, 40)
        cr.show_text(f"Year {self.year}")
        
        # Draw progress percentage
        cr.set_font_size(16)
        cr.move_to(20, 65)
        cr.show_text(f"{self.progress:.1f}% Complete")
        
        # Draw day counter
        cr.set_font_size(14)
        cr.set_source_rgba(1, 1, 1, 0.7)
        cr.move_to(20, 85)
        cr.show_text(f"Day {self.current_day} of {self.total_days}")
        
        # Draw circles for each day
        self.draw_day_circles(cr)
        
        # Draw progress bar
        self.draw_progress_bar(cr)
        
        return False
    
    def draw_day_circles(self, cr):
        """Draw 365/366 circles representing each day"""
        circle_radius = 2.5
        spacing = 9
        start_x = 22
        start_y = 110
        cols = 26  # Days per row
        
        for day in range(1, self.total_days + 1):
            col = (day - 1) % cols
            row = (day - 1) // cols
            
            x = start_x + col * spacing
            y = start_y + row * spacing
            
            # Determine circle color
            if day < self.current_day:
                # Past days - white
                cr.set_source_rgba(1, 1, 1, 0.9)
            elif day == self.current_day:
                # Current day - green
                cr.set_source_rgba(0.2, 0.8, 0.2, 1.0)
            else:
                # Future days - dim gray
                cr.set_source_rgba(0.3, 0.3, 0.3, 0.5)
            
            cr.arc(x, y, circle_radius, 0, 2 * math.pi)
            cr.fill()
    
    def draw_progress_bar(self, cr):
        """Draw progress bar at the bottom"""
        bar_x = 20
        bar_y = 370
        bar_width = 280
        bar_height = 22
        
        # Background of progress bar
        cr.set_source_rgba(0.2, 0.2, 0.2, 0.6)
        cr.rectangle(bar_x, bar_y, bar_width, bar_height)
        cr.fill()
        
        # Filled portion
        filled_width = bar_width * (self.progress / 100)
        cr.set_source_rgba(0.2, 0.8, 0.2, 0.8)
        cr.rectangle(bar_x, bar_y, filled_width, bar_height)
        cr.fill()
        
        # Border
        cr.set_source_rgba(1, 1, 1, 0.3)
        cr.set_line_width(1)
        cr.rectangle(bar_x, bar_y, bar_width, bar_height)
        cr.stroke()
        
        # Percentage text on bar
        cr.set_source_rgba(1, 1, 1, 1)
        cr.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        cr.set_font_size(12)
        text = f"{self.progress:.1f}%"
        extents = cr.text_extents(text)
        text_x = bar_x + (bar_width - extents.width) / 2
        text_y = bar_y + (bar_height + extents.height) / 2
        cr.move_to(text_x, text_y)
        cr.show_text(text)
    
    def schedule_daily_update(self):
        """Schedule update at midnight"""
        now = datetime.datetime.now()
        tomorrow = now.replace(hour=0, minute=0, second=0, microsecond=0) + datetime.timedelta(days=1)
        seconds_until_midnight = (tomorrow - now).total_seconds()
        
        # Schedule update
        GLib.timeout_add_seconds(int(seconds_until_midnight), self.daily_update)
    
    def daily_update(self):
        """Update widget data and redraw"""
        self.update_year_data()
        self.queue_draw()
        self.schedule_daily_update()
        return False

def main():
    # Create and show window
    win = YearProgressWidget()
    win.connect('destroy', Gtk.main_quit)
    win.show_all()
    
    # Make window click-through by setting input region to empty
    window = win.get_window()
    if window:
        region = cairo.Region()
        window.input_shape_combine_region(region, 0, 0)
    
    Gtk.main()

if __name__ == '__main__':
    main()
