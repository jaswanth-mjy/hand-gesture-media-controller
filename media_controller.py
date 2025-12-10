import pyautogui
import time
import platform


class MediaController:
    """
    Controls media playback across different applications (browser, VLC, Spotify, etc.)
    using keyboard shortcuts.
    """
    
    def __init__(self, cooldown=1.0):
        """
        Initialize the media controller.
        
        Args:
            cooldown: Minimum time (seconds) between consecutive commands to prevent spam
        """
        self.cooldown = cooldown
        self.last_command_time = 0
        self.current_state = None  # "PLAYING" or "PAUSED"
        
        # Disable PyAutoGUI's fail-safe (moving mouse to corner stops program)
        pyautogui.FAILSAFE = True
        
        # Set pause between actions to prevent issues
        pyautogui.PAUSE = 0.1
        
        # Detect OS for platform-specific controls
        self.os_type = platform.system()
        
    def can_execute_command(self):
        """
        Check if enough time has passed since the last command.
        
        Returns:
            True if command can be executed, False otherwise
        """
        current_time = time.time()
        if current_time - self.last_command_time >= self.cooldown:
            self.last_command_time = current_time
            return True
        return False
    
    def play(self):
        """
        Send play command to media player.
        Uses space bar which works for most media players and browsers.
        """
        if not self.can_execute_command():
            return False
        
        # Only send if not already playing
        if self.current_state == "PLAYING":
            return False
        
        try:
            # Space bar works for: YouTube, Netflix, VLC, Spotify, QuickTime, etc.
            pyautogui.press('space')
            self.current_state = "PLAYING"
            print("▶ PLAY command sent")
            return True
        except Exception as e:
            print(f"Error sending play command: {e}")
            return False
    
    def pause(self):
        """
        Send pause command to media player.
        Uses space bar which works for most media players and browsers.
        """
        if not self.can_execute_command():
            return False
        
        # Only send if not already paused
        if self.current_state == "PAUSED":
            return False
        
        try:
            # Space bar works for: YouTube, Netflix, VLC, Spotify, QuickTime, etc.
            pyautogui.press('space')
            self.current_state = "PAUSED"
            print("⏸ PAUSE command sent")
            return True
        except Exception as e:
            print(f"Error sending pause command: {e}")
            return False
    
    def toggle_play_pause(self):
        """
        Toggle between play and pause states.
        Useful when current state is unknown.
        """
        if self.can_execute_command():
            try:
                pyautogui.press('space')
                # Toggle state
                if self.current_state == "PLAYING":
                    self.current_state = "PAUSED"
                    print("⏸ PAUSE (toggle)")
                else:
                    self.current_state = "PLAYING"
                    print("▶ PLAY (toggle)")
                return True
            except Exception as e:
                print(f"Error toggling play/pause: {e}")
                return False
        return False
    
    def volume_up(self):
        """Increase volume (optional feature)."""
        try:
            if self.os_type == "Darwin":  # macOS
                pyautogui.press('volumeup')
            else:
                pyautogui.press('volumeup')
            return True
        except Exception as e:
            print(f"Error increasing volume: {e}")
            return False
    
    def volume_down(self):
        """Decrease volume (optional feature)."""
        try:
            if self.os_type == "Darwin":  # macOS
                pyautogui.press('volumedown')
            else:
                pyautogui.press('volumedown')
            return True
        except Exception as e:
            print(f"Error decreasing volume: {e}")
            return False
    
    def skip_forward(self):
        """Skip forward 10 seconds in media playback."""
        if not self.can_execute_command():
            return False
        
        try:
            # Right arrow or 'l' key for YouTube (10 seconds forward)
            # Works for: YouTube, VLC, most video players
            pyautogui.press('right')
            print("⏩ SKIP FORWARD 10 seconds")
            return True
        except Exception as e:
            print(f"Error skipping forward: {e}")
            return False
    
    def skip_backward(self):
        """Skip backward 10 seconds in media playback."""
        if not self.can_execute_command():
            return False
        
        try:
            # Left arrow or 'j' key for YouTube (10 seconds backward)
            # Works for: YouTube, VLC, most video players
            pyautogui.press('left')
            print("⏪ SKIP BACKWARD 10 seconds")
            return True
        except Exception as e:
            print(f"Error skipping backward: {e}")
            return False
    
    def reset_state(self):
        """Reset the current playback state."""
        self.current_state = None
        print("State reset")
