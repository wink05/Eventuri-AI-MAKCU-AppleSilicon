import os
import json
import threading

def get_foreground_monitor_resolution():
    if os.name == "nt":
        import ctypes
        from ctypes import wintypes
        # Structures
        class RECT(ctypes.Structure):
            _fields_ = [
                ("left",   ctypes.c_long),
                ("top",    ctypes.c_long),
                ("right",  ctypes.c_long),
                ("bottom", ctypes.c_long),
            ]

        class MONITORINFO(ctypes.Structure):
            _fields_ = [
                ("cbSize",   ctypes.c_ulong),
                ("rcMonitor", RECT),
                ("rcWork",    RECT),
                ("dwFlags",   ctypes.c_ulong),
            ]
        # DPI awareness so we get actual pixels
        try:
            ctypes.windll.shcore.SetProcessDpiAwareness(2)
        except Exception:
            try:
                ctypes.windll.user32.SetProcessDPIAware()
            except Exception:
                pass

        user32 = ctypes.windll.user32
        monitor = user32.MonitorFromWindow(user32.GetForegroundWindow(), 2)  # MONITOR_DEFAULTTONEAREST = 2
        mi = MONITORINFO()
        mi.cbSize = ctypes.sizeof(MONITORINFO)

        if ctypes.windll.user32.GetMonitorInfoW(monitor, ctypes.byref(mi)):
            w = mi.rcMonitor.right - mi.rcMonitor.left
            h = mi.rcMonitor.bottom - mi.rcMonitor.top
            return w, h
        else:
            # fallback to primary if anything fails
            return user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    else:
        # macOS/Linux fallback using tkinter or other means
        try:
            import tkinter as tk
            root = tk.Tk()
            root.withdraw()
            w = root.winfo_screenwidth()
            h = root.winfo_screenheight()
            root.destroy()
            return w, h
        except Exception:
            return 1920, 1080 # Safe default

w, h = get_foreground_monitor_resolution()

class Config:
    def __init__(self):
        # --- General Settings ---
        self.region_size = 200  # Keep for backward compatibility
        self.fov_x_size = 200   # FOV X-axis size
        self.fov_y_size = 200   # FOV Y-axis size
        
        # Use local resolution detection
        curr_w, curr_h = get_foreground_monitor_resolution()
        self.screen_width = curr_w 
        self.screen_height = curr_h
        
        self.player_y_offset = 5 # Offset for player detection
        self.capturer_mode = "NDI"  # Default to MSS mode
        self.always_on_aim = False
        
        # --- Height Targeting System ---
        self.height_targeting_enabled = True  # Enable height targeting system
        self.target_height = 0.700  # Target height on player (0.100=bottom, 1.000=top)
        self.height_deadzone_enabled = True  # Enable height deadzone
        self.height_deadzone_min = 0.600  # Lower bound of deadzone
        self.height_deadzone_max = 0.800  # Upper bound of deadzone
        self.height_deadzone_x_only = True  # Only move X-axis in deadzone
        self.height_deadzone_tolerance = 5.000  # Pixels of tolerance for full entry (higher = need to be deeper inside)
        self.main_pc_width = 1920  # Default width for main PC
        self.main_pc_height = 1080  # Default height for main PC
        
        # --- X-Axis Center Targeting ---
        self.x_center_targeting_enabled = True  # Enable X-axis center targeting
        self.x_center_tolerance_percent = 10.0   # Tolerance percentage for X-center targeting (0-50%)
        self.x_center_offset_px = 0             # X-axis offset in pixels for center targeting
        
        # --- Mouse Movement Multiplier ---
        self.mouse_movement_multiplier = 1.0     # Mouse movement speed multiplier (0.1-5.0) - kept for backward compatibility
        self.mouse_movement_multiplier_x = 1.0   # Mouse movement speed multiplier for X-axis (0.0-5.0)
        self.mouse_movement_multiplier_y = 1.0   # Mouse movement speed multiplier for Y-axis (0.0-5.0)
        self.mouse_movement_enabled_x = True     # Enable/disable X-axis movement (True/False)
        self.mouse_movement_enabled_y = True     # Enable/disable Y-axis movement (True/False)
        
        # --- RCS (Recoil Control System) ---
        self.rcs_enabled = False                 # Enable RCS functionality
        self.rcs_ads_only = False               # Enable RCS only when ADS (right mouse button held)
        self.rcs_disable_y_axis = False          # Disable Aimbot Y-axis movement when RCS is active
        self.rcs_button = 0                     # 0..4 -> Left, Right, Middle, Side4, Side5
        self.rcs_x_strength = 1.0               # X-axis recoil compensation strength (0.1-5.0)
        self.rcs_x_delay = 0.010                # X-axis recoil compensation delay in seconds (0.001-0.100)
        self.rcs_y_random_enabled = False       # Enable Y-axis random jitter
        self.rcs_y_random_strength = 0.5        # Y-axis random jitter strength (0.1-3.0)
        self.rcs_y_random_delay = 0.020         # Y-axis random jitter delay in seconds (0.001-0.100)
        
        # --- RCS Game-based Mode ---
        self.rcs_mode = "simple"                # RCS mode: "simple" or "game"
        self.rcs_game = ""                       # Selected game name (e.g., "cs2", "apex", "rust")
        self.rcs_weapon = ""                     # Selected weapon name (e.g., "ak47", "R301")
        self.rcs_x_multiplier = 1.0             # X-axis movement multiplier
        self.rcs_y_multiplier = 1.0             # Y-axis movement multiplier
        self.rcs_x_time_multiplier = 1.0        # X-axis time multiplier
        self.rcs_y_time_multiplier = 1.0        # Y-axis time multiplier
        
        self.rcs_weapon_multipliers = {}
        
        # --- Model and Detection ---
        script_dir = os.path.dirname(os.path.abspath(__file__))
        root_dir = os.path.dirname(script_dir)
        self.models_dir = os.path.join(root_dir, "models")
        if not os.path.exists(self.models_dir):
            # Fallback if structure is different
            self.models_dir = "models"
        
        self.model_path = os.path.join(self.models_dir, "Click here to Load a model")
        self.custom_player_label = "Select a Player Class"  
        self.custom_head_label = "Select a Head Class"  
        self.model_file_size = 0
        self.model_load_error = ""
        self.conf = 0.2
        self.imgsz = 640
        self.max_detect = 50
        self.selected_player_classes = []
        self.class_confidence = {}
        
        # --- Mouse / MAKCU ---
        self.selected_mouse_button = 3
        self.makcu_connected = False
        self.makcu_status_msg = "Disconnected"
        self.aim_humanization = 0
        self.in_game_sens = 1.3
        self.button_mask = False

        # --- Trigger Settings ---
        self.trigger_enabled         = False
        self.trigger_always_on       = False
        self.trigger_button          = 1
        self.trigger_mode            = 1
        self.trigger_head_only       = False
        self.trigger_radius_px       = 8
        self.trigger_delay_ms        = 30
        self.trigger_cooldown_ms     = 120
        self.trigger_min_conf        = 0.35
        self.trigger_burst_count     = 3
        self.trigger_mode2_range_x   = 50.0
        self.trigger_mode2_range_y   = 50.0
        
        # --- HSV ---
        self.trigger_hsv_h_min       = 0
        self.trigger_hsv_h_max       = 179
        self.trigger_hsv_s_min       = 0
        self.trigger_hsv_s_max       = 255
        self.trigger_hsv_v_min       = 0
        self.trigger_hsv_v_max       = 255
        self.trigger_color_radius_px = 20
        self.trigger_color_delay_ms  = 50
        self.trigger_color_cooldown_ms = 200

        self.mode = "normal"    
        self.aimbot_running = False
        self.aimbot_status_msg = "Stopped"

        self.normal_x_speed = 0.5
        self.normal_y_speed = 0.5

        self.bezier_segments = 8
        self.bezier_ctrl_x = 16
        self.bezier_ctrl_y = 16

        self.silent_segments = 7
        self.silent_ctrl_x = 18
        self.silent_ctrl_y = 18
        self.silent_speed = 3
        self.silent_cooldown = 0.05
        self.silent_strength = 1.000
        self.silent_auto_fire = False
        self.silent_fire_delay = 0.010
        self.silent_return_delay = 0.020
        self.silent_speed_mode = True
        self.silent_use_bezier = False

        self.smooth_gravity = 9.0
        self.smooth_wind = 3.0
        self.smooth_min_delay = 0.0
        self.smooth_max_delay = 0.002
        self.smooth_max_step = 40.0
        self.smooth_min_step = 2.0
        self.smooth_max_step_ratio = 0.20
        self.smooth_target_area_ratio = 0.06
        self.smooth_reaction_min = 0.05
        self.smooth_reaction_max = 0.21
        self.smooth_close_range = 35
        self.smooth_far_range = 250
        self.smooth_close_speed = 0.8
        self.smooth_far_speed = 1.00
        self.smooth_acceleration = 1.15
        self.smooth_deceleration = 1.05
        self.smooth_fatigue_effect = 1.2
        self.smooth_micro_corrections = 0

        self.last_error = ""
        self.last_info = ""

        self.ncaf_enabled = False
        self.ncaf_near_radius = 120.0
        self.ncaf_snap_radius = 22.0
        self.ncaf_alpha = 1.30
        self.ncaf_snap_boost = 1.25
        self.ncaf_max_step = 35.0
        self.ncaf_iou_threshold = 0.50
        self.ncaf_max_ttl = 8
        self.ncaf_show_debug = False

        self._save_lock = threading.Lock()
        self._save_timer = None
        self.show_debug_window = False
        self.show_debug_text_info = True

        self.ndi_width = 0
        self.ndi_height = 0
        self.ndi_sources = []
        self.ndi_selected_source = None

        self.capture_width = 1920
        self.capture_height = 1080
        self.capture_fps = 240
        self.capture_device_index = 0
        self.capture_fourcc_preference = ["NV12", "YUY2", "MJPG"]
        self.capture_range_x = 0
        self.capture_range_y = 0
        self.capture_offset_x = 0
        self.capture_offset_y = 0
        self.capture_center_offset_x = 0
        self.capture_center_offset_y = 0

        self.udp_ip = "192.168.0.01"
        self.udp_port = 1234
        self.udp_width = 0
        self.udp_height = 0

    def _ensure_default_attributes(self):
        # Implementation omitted for brevity, but you can keep it as needed
        pass

    def save(self, path="config_profile.json"):
        data = self.__dict__.copy()
        for key in ['_save_lock', '_save_timer']:
            data.pop(key, None)
        with self._save_lock:
            with open(path, "w") as f:
                json.dump(data, f, indent=2)

    def load(self, path="config_profile.json"):
        if os.path.exists(path):
            try:
                with open(path, "r", encoding='utf-8') as f:
                    data = json.load(f)
                    # Don't let old models_dir from config override our detected one
                    if "models_dir" in data:
                        del data["models_dir"]
                    self.__dict__.update(data)
            except Exception as e:
                print(f"[WARNING] Load error: {e}")
        
        # Re-verify models_dir is absolute and correct
        script_dir = os.path.dirname(os.path.abspath(__file__))
        root_dir = os.path.dirname(script_dir)
        self.models_dir = os.path.join(root_dir, "models")
        if not os.path.exists(self.models_dir):
            self.models_dir = "models"

    def reset_to_defaults(self):
        self.__init__()

    def list_models(self):
        models = []
        for ext in (".pt", ".onnx", ".engine"):
            try:
                models.extend([f for f in os.listdir(self.models_dir) if f.endswith(ext)])
            except Exception: pass
        return sorted(list(set(models)))

config = Config()
try:
    config.load()
except Exception: pass
