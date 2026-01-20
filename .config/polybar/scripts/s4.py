#!/usr/bin/env python3
"""
Year Progress Widget for i3wm with Daily Resolutions
A transparent desktop widget showing progress through the year with resolution tracking
"""

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib
import cairo
import datetime
import math
import json
import os

class YearProgressWidget(Gtk.Window):
    def __init__(self):
        super().__init__()
        
        # Data file path
        self.data_file = os.path.expanduser('~/.config/year_progress_data.json')
        
        # Load data
        self.load_data()
        
        # View state
        self.view_mode = 'main'  # 'main', 'settings', 'day_view'
        self.settings_text = ""
        self.cursor_pos = 0
        self.cursor_visible = True
        self.cursor_blink_timer = None
        self.viewing_day = None  # Which day we're viewing
        
        # Window setup
        self.set_title("Year Progress")
        self.set_default_size(320, 420)
        self.set_decorated(False)
        self.set_resizable(False)
        
        # Set proper window role for i3 identification
        self.set_role("desktop_widget")
        
        # Make window transparent
        screen = self.get_screen()
        visual = screen.get_rgba_visual()
        if visual and screen.is_composited():
            self.set_visual(visual)
        
        # Set window properties for desktop widget behavior
        self.set_type_hint(Gdk.WindowTypeHint.DESKTOP)
        self.set_keep_below(True)
        self.stick()
        
        # Make window click-through and prevent i3 tiling
        self.set_accept_focus(False)
        self.set_can_focus(False)
        self.set_skip_taskbar_hint(True)
        self.set_skip_pager_hint(True)
        
        # Position window (centered)
        display = Gdk.Display.get_default()
        monitor = display.get_primary_monitor()
        geometry = monitor.get_geometry()
        screen_width = geometry.width
        screen_height = geometry.height
        
        x = (screen_width - 320) // 2
        y = (screen_height - 420) // 2
        self.move(x, y)
        
        # Set up for transparency and drawing
        self.set_app_paintable(True)
        self.connect('draw', self.on_draw)
        self.connect('screen-changed', self.on_screen_changed)
        
        # Track hover state
        self.hover_day = None
        self.hover_heart = None
        
        # Calculate year data
        self.update_year_data()
        
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
        
        # Update daily at midnight
        self.schedule_daily_update()
        
    def load_data(self):
        """Load resolutions and completion data from file"""
        self.resolutions = ["Exercise", "Read", "Meditate"]  # Default resolutions
        self.completions = {}  # {date_str: [True, False, True, ...]}
        
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                    self.resolutions = data.get('resolutions', self.resolutions)
                    self.completions = data.get('completions', {})
            except Exception as e:
                print(f"Error loading data: {e}")
    
    def save_data(self):
        """Save resolutions and completion data to file"""
        try:
            os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
            data = {
                'resolutions': self.resolutions,
                'completions': self.completions
            }
            with open(self.data_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving data: {e}")
    
    def get_today_key(self):
        """Get string key for today's date"""
        return datetime.datetime.now().strftime('%Y-%m-%d')
    
    def get_today_completions(self):
        """Get completion status for today"""
        key = self.get_today_key()
        if key not in self.completions:
            self.completions[key] = [False] * len(self.resolutions)
        # Ensure completions array matches current resolutions length
        while len(self.completions[key]) < len(self.resolutions):
            self.completions[key].append(False)
        return self.completions[key]
    
    def get_day_completions(self, day_num):
        """Get completion status for a specific day"""
        # Calculate date key directly
        start_of_year = datetime.datetime(self.year, 1, 1)
        date = start_of_year + datetime.timedelta(days=day_num - 1)
        key = date.strftime('%Y-%m-%d')
        
        if key not in self.completions:
            self.completions[key] = [False] * len(self.resolutions)
        # Ensure completions array matches current resolutions length
        while len(self.completions[key]) < len(self.resolutions):
            self.completions[key].append(False)
        return self.completions[key]
    
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
        
        start_of_year = datetime.datetime(self.year, 1, 1)
        self.current_day = (now - start_of_year).days + 1
        
        self.progress = (self.current_day / self.total_days) * 100
    
    def on_mouse_move(self, widget, event):
        """Handle mouse movement for hover effects"""
        old_hover_day = self.hover_day
        old_hover_heart = self.hover_heart
        
        self.hover_day = None
        self.hover_heart = None
        
        if self.view_mode == 'settings':
            # Check close button in settings mode
            btn_rect = self.get_close_button_rect()
            if (btn_rect[0] <= event.x <= btn_rect[0] + btn_rect[2] and 
                btn_rect[1] <= event.y <= btn_rect[1] + btn_rect[3]):
                self.hover_heart = -2  # Special value for close button
        elif self.view_mode == 'day_view':
            # Check back button in day view
            btn_rect = self.get_back_button_rect()
            if (btn_rect[0] <= event.x <= btn_rect[0] + btn_rect[2] and 
                btn_rect[1] <= event.y <= btn_rect[1] + btn_rect[3]):
                self.hover_heart = -3  # Special value for back button
        else:
            # Main view - check day circles
            circle_radius = 2.5
            spacing = 9
            start_x = 22
            start_y = 110
            cols = 26
            
            for day in range(1, self.total_days + 1):
                col = (day - 1) % cols
                row = (day - 1) // cols
                
                x = start_x + col * spacing
                y = start_y + row * spacing
                
                distance = math.sqrt((event.x - x)**2 + (event.y - y)**2)
                if distance <= circle_radius + 2:
                    self.hover_day = day
                    break
            
            # Check hearts
            heart_positions = self.get_heart_positions()
            for i, (hx, hy) in enumerate(heart_positions):
                if abs(event.x - hx) <= 10 and abs(event.y - hy) <= 10:
                    self.hover_heart = i
                    break
            
            # Check settings button
            btn_x, btn_y, btn_w, btn_h = self.get_settings_button_rect()
            if btn_x <= event.x <= btn_x + btn_w and btn_y <= event.y <= btn_y + btn_h:
                self.hover_heart = -1  # Special value for button hover
        
        if old_hover_day != self.hover_day or old_hover_heart != self.hover_heart:
            self.queue_draw()
    
    def on_mouse_leave(self, widget, event):
        """Handle mouse leaving widget"""
        self.hover_day = None
        self.hover_heart = None
        self.queue_draw()
    
    def get_heart_positions(self):
        """Calculate positions for resolution hearts"""
        positions = []
        heart_y = 348
        num_hearts = len(self.resolutions)
        
        if num_hearts == 0:
            return positions
        
        # Calculate spacing to fit hearts nicely
        total_width = 260
        spacing = total_width / (num_hearts + 1)
        start_x = 30
        
        for i in range(num_hearts):
            x = start_x + spacing * (i + 1)
            positions.append((x, heart_y))
        
        return positions
    
    def get_settings_button_rect(self):
        """Get rectangle for settings button"""
        return (285, 343, 20, 20)
    
    def get_close_button_rect(self):
        """Get rectangle for close button in settings mode"""
        return (20, 380, 60, 25)
    
    def get_back_button_rect(self):
        """Get rectangle for back button in day view"""
        return (20, 380, 60, 25)
    
    def get_day_view_heart_positions(self):
        """Calculate positions for resolution hearts in day view"""
        positions = []
        start_y = 120
        spacing = 40
        
        for i in range(len(self.resolutions)):
            y = start_y + i * spacing
            positions.append((40, y))
        
        return positions
    
    def on_click(self, widget, event):
        """Handle mouse clicks"""
        if self.view_mode == 'settings':
            # Check close button
            btn_rect = self.get_close_button_rect()
            if (btn_rect[0] <= event.x <= btn_rect[0] + btn_rect[2] and 
                btn_rect[1] <= event.y <= btn_rect[1] + btn_rect[3]):
                self.close_settings()
                return True
            
            # Click in text area to focus
            text_box_x = 20
            text_box_y = 80
            text_box_w = 280
            text_box_h = 280
            
            if (text_box_x <= event.x <= text_box_x + text_box_w and 
                text_box_y <= event.y <= text_box_y + text_box_h):
                self.drawing_area.grab_focus()
                # Calculate cursor position from click (simplified - end of text)
                self.cursor_pos = len(self.settings_text)
                self.queue_draw()
                return True
        elif self.view_mode == 'day_view':
            # Check back button
            btn_rect = self.get_back_button_rect()
            if (btn_rect[0] <= event.x <= btn_rect[0] + btn_rect[2] and 
                btn_rect[1] <= event.y <= btn_rect[1] + btn_rect[3]):
                self.close_day_view()
                return True
        else:
            # Main view
            # Check if day circle clicked
            circle_radius = 2.5
            spacing = 9
            start_x = 22
            start_y = 110
            cols = 26
            
            for day in range(1, self.total_days + 1):
                col = (day - 1) % cols
                row = (day - 1) // cols
                
                x = start_x + col * spacing
                y = start_y + row * spacing
                
                distance = math.sqrt((event.x - x)**2 + (event.y - y)**2)
                if distance <= circle_radius + 2:
                    self.open_day_view(day)
                    return True
            
            # Check if settings button clicked
            btn_x, btn_y, btn_w, btn_h = self.get_settings_button_rect()
            if btn_x <= event.x <= btn_x + btn_w and btn_y <= event.y <= btn_y + btn_h:
                self.open_settings()
                return True
            
            # Check if heart clicked
            heart_positions = self.get_heart_positions()
            for i, (hx, hy) in enumerate(heart_positions):
                if abs(event.x - hx) <= 10 and abs(event.y - hy) <= 10:
                    self.toggle_resolution(i)
                    return True
        
        return False
    
    def toggle_resolution(self, index):
        """Toggle completion status of a resolution"""
        if self.view_mode == 'day_view':
            # Toggle for the day being viewed
            completions = self.get_day_completions(self.viewing_day)
        else:
            # Toggle for today (main view)
            completions = self.get_today_completions()
        
        if index < len(completions):
            completions[index] = not completions[index]
            self.save_data()
            self.queue_draw()
    
    def open_settings(self):
        """Switch to settings view"""
        self.view_mode = 'settings'
        self.settings_text = '\n'.join(self.resolutions)
        self.cursor_pos = len(self.settings_text)
        self.cursor_visible = True
        self.start_cursor_blink()
        # Enable keyboard input
        self.set_accept_focus(True)
        self.set_can_focus(True)
        self.drawing_area.grab_focus()
        self.queue_draw()
    
    def close_settings(self):
        """Save settings and return to main view"""
        # Parse resolutions from text
        lines = [line.strip() for line in self.settings_text.split('\n') if line.strip()]
        if lines:
            old_count = len(self.resolutions)
            new_count = len(lines)
            self.resolutions = lines
            
            # Only reset today's completions if count changed
            if old_count != new_count:
                key = self.get_today_key()
                # Preserve existing completions, add False for new ones
                if key in self.completions:
                    existing = self.completions[key][:new_count]
                    while len(existing) < new_count:
                        existing.append(False)
                    self.completions[key] = existing
                else:
                    self.completions[key] = [False] * new_count
            
            self.save_data()
        
        self.view_mode = 'main'
        self.stop_cursor_blink()
        # Disable keyboard input
        self.set_accept_focus(False)
        self.set_can_focus(False)
        self.queue_draw()
    
    def open_day_view(self, day_num):
        """Open day view for a specific day"""
        self.viewing_day = day_num
        self.view_mode = 'day_view'
        self.queue_draw()
    
    def close_day_view(self):
        """Close day view and return to main"""
        self.viewing_day = None
        self.view_mode = 'main'
        self.queue_draw()
    
    def on_key_press(self, widget, event):
        """Handle keyboard input in settings mode"""
        if self.view_mode != 'settings':
            return False
        
        keyval = event.keyval
        keyname = Gdk.keyval_name(keyval)
        
        # Handle special keys
        if keyname == 'BackSpace':
            if self.cursor_pos > 0:
                self.settings_text = self.settings_text[:self.cursor_pos-1] + self.settings_text[self.cursor_pos:]
                self.cursor_pos -= 1
        elif keyname == 'Delete':
            if self.cursor_pos < len(self.settings_text):
                self.settings_text = self.settings_text[:self.cursor_pos] + self.settings_text[self.cursor_pos+1:]
        elif keyname == 'Left':
            if self.cursor_pos > 0:
                self.cursor_pos -= 1
        elif keyname == 'Right':
            if self.cursor_pos < len(self.settings_text):
                self.cursor_pos += 1
        elif keyname == 'Home':
            # Go to start of current line
            line_start = self.settings_text.rfind('\n', 0, self.cursor_pos)
            self.cursor_pos = line_start + 1 if line_start != -1 else 0
        elif keyname == 'End':
            # Go to end of current line
            line_end = self.settings_text.find('\n', self.cursor_pos)
            self.cursor_pos = line_end if line_end != -1 else len(self.settings_text)
        elif keyname == 'Return' or keyname == 'KP_Enter':
            # Insert newline
            self.settings_text = self.settings_text[:self.cursor_pos] + '\n' + self.settings_text[self.cursor_pos:]
            self.cursor_pos += 1
        elif keyname == 'Escape':
            self.close_settings()
            return True
        elif len(keyname) == 1 or keyname == 'space':
            # Regular character input
            char = event.string if event.string else ' '
            self.settings_text = self.settings_text[:self.cursor_pos] + char + self.settings_text[self.cursor_pos:]
            self.cursor_pos += len(char)
        
        # Reset cursor blink
        self.cursor_visible = True
        self.queue_draw()
        return True
    
    def start_cursor_blink(self):
        """Start cursor blinking timer"""
        if self.cursor_blink_timer:
            GLib.source_remove(self.cursor_blink_timer)
        self.cursor_blink_timer = GLib.timeout_add(500, self.blink_cursor)
    
    def stop_cursor_blink(self):
        """Stop cursor blinking timer"""
        if self.cursor_blink_timer:
            GLib.source_remove(self.cursor_blink_timer)
            self.cursor_blink_timer = None
    
    def blink_cursor(self):
        """Toggle cursor visibility"""
        self.cursor_visible = not self.cursor_visible
        self.queue_draw()
        return True
    
    def on_draw(self, widget, cr):
        """Draw the widget"""
        # Make background transparent
        cr.set_source_rgba(0, 0, 0, 0)
        cr.set_operator(cairo.OPERATOR_SOURCE)
        cr.paint()
        
        if self.view_mode == 'settings':
            self.draw_settings_view(cr)
        elif self.view_mode == 'day_view':
            self.draw_day_view(cr)
        else:
            self.draw_main_view(cr)
        
        return False
    
    def draw_main_view(self, cr):
        """Draw main year progress view"""
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
        
        # Draw resolution hearts
        self.draw_resolution_hearts(cr)
        
        # Draw settings button
        self.draw_settings_button(cr)
        
        # Draw progress bar
        self.draw_progress_bar(cr)
        
        # Draw hover tooltip
        if self.hover_day:
            self.draw_day_tooltip(cr)
    
    def draw_settings_view(self, cr):
        """Draw settings/resolution editor view"""
        # Draw semi-transparent background panel
        cr.set_source_rgba(0.1, 0.1, 0.1, 0.7)
        cr.rectangle(10, 10, 300, 400)
        cr.fill()
        
        # Draw title
        cr.set_source_rgba(1, 1, 1, 0.9)
        cr.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        cr.set_font_size(20)
        cr.move_to(20, 40)
        cr.show_text("Edit Resolutions")
        
        # Draw instructions
        cr.set_source_rgba(1, 1, 1, 0.7)
        cr.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
        cr.set_font_size(12)
        cr.move_to(20, 65)
        cr.show_text("One resolution per line:")
        
        # Draw text area background
        text_box_x = 20
        text_box_y = 80
        text_box_w = 280
        text_box_h = 280
        
        cr.set_source_rgba(0.15, 0.15, 0.15, 0.8)
        self.rounded_rectangle(cr, text_box_x, text_box_y, text_box_w, text_box_h, 5)
        cr.fill()
        
        # Draw border
        cr.set_source_rgba(1, 1, 1, 0.3)
        cr.set_line_width(1)
        self.rounded_rectangle(cr, text_box_x, text_box_y, text_box_w, text_box_h, 5)
        cr.stroke()
        
        # Draw text content with cursor
        cr.set_source_rgba(1, 1, 1, 0.9)
        cr.select_font_face("Fira Code", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
        cr.set_font_size(13)
        
        lines = self.settings_text.split('\n')
        y_offset = text_box_y + 25
        char_count = 0
        cursor_x = text_box_x + 10
        cursor_y = y_offset
        
        for i, line in enumerate(lines[:15]):  # Limit visible lines
            cr.move_to(text_box_x + 10, y_offset)
            cr.show_text(line)
            
            # Calculate cursor position
            if char_count <= self.cursor_pos <= char_count + len(line):
                cursor_line_pos = self.cursor_pos - char_count
                if cursor_line_pos > 0:
                    extents = cr.text_extents(line[:cursor_line_pos])
                    cursor_x = text_box_x + 10 + extents.width
                else:
                    cursor_x = text_box_x + 10
                cursor_y = y_offset
            
            char_count += len(line) + 1  # +1 for newline
            y_offset += 18
        
        # Draw blinking cursor
        if self.cursor_visible:
            cr.set_source_rgba(0.2, 0.8, 0.2, 1.0)
            cr.set_line_width(2)
            cr.move_to(cursor_x, cursor_y - 12)
            cr.line_to(cursor_x, cursor_y + 2)
            cr.stroke()
        
        # Draw tip
        cr.set_source_rgba(1, 1, 1, 0.5)
        cr.select_font_face("Sans", cairo.FONT_SLANT_ITALIC, cairo.FONT_WEIGHT_NORMAL)
        cr.set_font_size(10)
        cr.move_to(text_box_x, text_box_y + text_box_h + 15)
        cr.show_text("💡 Tip: Keep it simple - 3-5 resolutions work best!")
        
        # Draw close button
        self.draw_close_button(cr)
    
    def draw_close_button(self, cr):
        """Draw close/back button in settings view"""
        btn_x, btn_y, btn_w, btn_h = self.get_close_button_rect()
        
        # Button background
        if self.hover_heart == -2:
            cr.set_source_rgba(0.2, 0.8, 0.2, 0.8)
        else:
            cr.set_source_rgba(0.2, 0.6, 0.2, 0.6)
        
        self.rounded_rectangle(cr, btn_x, btn_y, btn_w, btn_h, 3)
        cr.fill()
        
        # Button text
        cr.set_source_rgba(1, 1, 1, 1)
        cr.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        cr.set_font_size(12)
        text = "Close"
        extents = cr.text_extents(text)
        cr.move_to(btn_x + (btn_w - extents.width) / 2, btn_y + (btn_h + extents.height) / 2 - 1)
        cr.show_text(text)
    
    def draw_day_view(self, cr):
        """Draw day view showing completed resolutions for a specific day"""
        # Draw semi-transparent background panel
        cr.set_source_rgba(0.1, 0.1, 0.1, 0.7)
        cr.rectangle(10, 10, 300, 400)
        cr.fill()
        
        # Get date info - calculate directly
        start_of_year = datetime.datetime(self.year, 1, 1)
        date = start_of_year + datetime.timedelta(days=self.viewing_day - 1)
        date_str = date.strftime("%B %d, %Y")
        
        # Draw title
        cr.set_source_rgba(1, 1, 1, 0.9)
        cr.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        cr.set_font_size(18)
        cr.move_to(20, 40)
        cr.show_text(date_str)
        
        # Draw day number
        cr.set_source_rgba(1, 1, 1, 0.7)
        cr.set_font_size(14)
        cr.move_to(20, 65)
        cr.show_text(f"Day {self.viewing_day} of {self.total_days}")
        
        # Draw section title
        cr.set_source_rgba(1, 1, 1, 0.8)
        cr.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        cr.set_font_size(14)
        cr.move_to(20, 95)
        cr.show_text("Completed Resolutions:")
        
        # Get completions for this day
        completions = self.get_day_completions(self.viewing_day)
        
        # Filter to show only completed resolutions
        completed_items = []
        for i, completed in enumerate(completions):
            if completed and i < len(self.resolutions):
                completed_items.append(self.resolutions[i])
        
        # Draw completed resolutions
        if len(completed_items) == 0:
            cr.set_source_rgba(1, 1, 1, 0.5)
            cr.select_font_face("Sans", cairo.FONT_SLANT_ITALIC, cairo.FONT_WEIGHT_NORMAL)
            cr.set_font_size(13)
            cr.move_to(20, 125)
            cr.show_text("No resolutions completed on this day")
        else:
            start_y = 120
            spacing = 30
            
            for i, resolution in enumerate(completed_items):
                y = start_y + i * spacing
                
                # Draw checkmark
                cr.set_source_rgba(0.2, 0.8, 0.2, 1.0)
                cr.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
                cr.set_font_size(16)
                cr.move_to(20, y)
                cr.show_text("✓")
                
                # Draw resolution name
                cr.set_source_rgba(1, 1, 1, 0.9)
                cr.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
                cr.set_font_size(13)
                cr.move_to(40, y)
                cr.show_text(resolution)
        
        # Draw back button - always visible
        self.draw_back_button(cr)
    
    def draw_back_button(self, cr):
        """Draw back button in day view"""
        btn_x, btn_y, btn_w, btn_h = self.get_back_button_rect()
        
        # Button background
        if self.hover_heart == -3:
            cr.set_source_rgba(0.2, 0.8, 0.2, 0.8)
        else:
            cr.set_source_rgba(0.2, 0.6, 0.2, 0.6)
        
        self.rounded_rectangle(cr, btn_x, btn_y, btn_w, btn_h, 3)
        cr.fill()
        
        # Button text
        cr.set_source_rgba(1, 1, 1, 1)
        cr.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        cr.set_font_size(12)
        text = "Back"
        extents = cr.text_extents(text)
        cr.move_to(btn_x + (btn_w - extents.width) / 2, btn_y + (btn_h + extents.height) / 2 - 1)
        cr.show_text(text)
    
    def draw_day_circles(self, cr):
        """Draw 365/366 circles representing each day"""
        circle_radius = 2.5
        spacing = 9
        start_x = 22
        start_y = 110
        cols = 26
        
        for day in range(1, self.total_days + 1):
            col = (day - 1) % cols
            row = (day - 1) // cols
            
            x = start_x + col * spacing
            y = start_y + row * spacing
            
            # Determine circle color
            if day < self.current_day:
                cr.set_source_rgba(1, 1, 1, 0.9)
            elif day == self.current_day:
                cr.set_source_rgba(0.2, 0.8, 0.2, 1.0)
            else:
                cr.set_source_rgba(0.3, 0.3, 0.3, 0.5)
            
            cr.arc(x, y, circle_radius, 0, 2 * math.pi)
            cr.fill()
            
            # Highlight hovered day
            if day == self.hover_day:
                cr.set_source_rgba(1, 1, 1, 0.3)
                cr.arc(x, y, circle_radius + 2, 0, 2 * math.pi)
                cr.stroke()
    
    def draw_resolution_hearts(self, cr):
        """Draw hearts for daily resolutions using FiraCode font"""
        completions = self.get_today_completions()
        positions = self.get_heart_positions()
        
        for i, (x, y) in enumerate(positions):
            completed = completions[i] if i < len(completions) else False
            
            # Draw heart using unicode character
            cr.select_font_face("Fira Code", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
            cr.set_font_size(16)
            
            if completed:
                # Filled heart
                heart = "♥"
                cr.set_source_rgba(0.2, 0.8, 0.2, 1.0)
            else:
                # Empty heart
                heart = "♡"
                cr.set_source_rgba(0.5, 0.5, 0.5, 0.8)
            
            extents = cr.text_extents(heart)
            cr.move_to(x - extents.width/2, y + extents.height/2)
            cr.show_text(heart)
            
            # Highlight on hover
            if self.hover_heart == i:
                cr.set_source_rgba(1, 1, 1, 0.2)
                cr.arc(x, y, 12, 0, 2 * math.pi)
                cr.fill()
            
            # Draw resolution label below heart
            cr.set_source_rgba(1, 1, 1, 0.7)
            cr.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
            cr.set_font_size(9)
            label = self.resolutions[i] if i < len(self.resolutions) else ""
            if len(label) > 12:
                label = label[:10] + "..."
            extents = cr.text_extents(label)
            cr.move_to(x - extents.width/2, y + 16)
            cr.show_text(label)
    
    def draw_settings_button(self, cr):
        """Draw + button for settings"""
        btn_x, btn_y, btn_w, btn_h = self.get_settings_button_rect()
        
        # Button background
        if self.hover_heart == -1:
            cr.set_source_rgba(0.3, 0.3, 0.3, 0.8)
        else:
            cr.set_source_rgba(0.2, 0.2, 0.2, 0.6)
        
        cr.arc(btn_x + btn_w/2, btn_y + btn_h/2, btn_w/2, 0, 2 * math.pi)
        cr.fill()
        
        # + symbol
        cr.set_source_rgba(1, 1, 1, 0.9)
        cr.set_line_width(2)
        center_x = btn_x + btn_w/2
        center_y = btn_y + btn_h/2
        
        # Horizontal line
        cr.move_to(center_x - 6, center_y)
        cr.line_to(center_x + 6, center_y)
        cr.stroke()
        
        # Vertical line
        cr.move_to(center_x, center_y - 6)
        cr.line_to(center_x, center_y + 6)
        cr.stroke()
    
    def draw_progress_bar(self, cr):
        """Draw progress bar at the bottom"""
        bar_x = 20
        bar_y = 375
        bar_width = 280
        bar_height = 22
        
        # Background
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
        
        # Percentage text
        cr.set_source_rgba(1, 1, 1, 1)
        cr.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        cr.set_font_size(12)
        text = f"{self.progress:.1f}%"
        extents = cr.text_extents(text)
        text_x = bar_x + (bar_width - extents.width) / 2
        text_y = bar_y + (bar_height + extents.height) / 2
        cr.move_to(text_x, text_y)
        cr.show_text(text)
    
    def draw_day_tooltip(self, cr):
        """Draw tooltip showing date for hovered day"""
        if not self.hover_day:
            return
        
        # Calculate date
        start_of_year = datetime.datetime(self.year, 1, 1)
        date = start_of_year + datetime.timedelta(days=self.hover_day - 1)
        date_str = date.strftime("%B %d, %Y")
        
        # Get mouse position
        circle_radius = 2.5
        spacing = 9
        start_x = 22
        start_y = 110
        cols = 26
        
        col = (self.hover_day - 1) % cols
        row = (self.hover_day - 1) // cols
        
        x = start_x + col * spacing
        y = start_y + row * spacing
        
        # Tooltip dimensions
        cr.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
        cr.set_font_size(11)
        extents = cr.text_extents(date_str)
        
        tooltip_width = extents.width + 16
        tooltip_height = 24
        tooltip_x = x - tooltip_width / 2
        tooltip_y = y - tooltip_height - 8
        
        # Keep tooltip within bounds
        if tooltip_x < 15:
            tooltip_x = 15
        if tooltip_x + tooltip_width > 295:
            tooltip_x = 295 - tooltip_width
        if tooltip_y < 15:
            tooltip_y = y + 15
        
        # Draw tooltip background
        cr.set_source_rgba(0.15, 0.15, 0.15, 0.95)
        self.rounded_rectangle(cr, tooltip_x, tooltip_y, tooltip_width, tooltip_height, 4)
        cr.fill()
        
        # Draw tooltip border
        cr.set_source_rgba(1, 1, 1, 0.3)
        cr.set_line_width(1)
        self.rounded_rectangle(cr, tooltip_x, tooltip_y, tooltip_width, tooltip_height, 4)
        cr.stroke()
        
        # Draw text
        cr.set_source_rgba(1, 1, 1, 1)
        cr.move_to(tooltip_x + 8, tooltip_y + 16)
        cr.show_text(date_str)
    
    def rounded_rectangle(self, cr, x, y, width, height, radius):
        """Draw a rounded rectangle path"""
        cr.new_path()
        cr.arc(x + radius, y + radius, radius, math.pi, 3 * math.pi / 2)
        cr.arc(x + width - radius, y + radius, radius, 3 * math.pi / 2, 0)
        cr.arc(x + width - radius, y + height - radius, radius, 0, math.pi / 2)
        cr.arc(x + radius, y + height - radius, radius, math.pi / 2, math.pi)
        cr.close_path()
    
    def schedule_daily_update(self):
        """Schedule update at midnight"""
        now = datetime.datetime.now()
        tomorrow = now.replace(hour=0, minute=0, second=0, microsecond=0) + datetime.timedelta(days=1)
        seconds_until_midnight = (tomorrow - now).total_seconds()
        
        GLib.timeout_add_seconds(int(seconds_until_midnight), self.daily_update)
    
    def daily_update(self):
        """Update widget data and redraw"""
        self.update_year_data()
        self.queue_draw()
        self.schedule_daily_update()
        return False

def main():
    win = YearProgressWidget()
    win.connect('destroy', Gtk.main_quit)
    win.show_all()
    
    # Make window click-through by setting input region to empty
    window = win.get_window()
    if window:
        window.set_role("year_progress_widget")
    
    Gtk.main()

if __name__ == '__main__':
    main()
