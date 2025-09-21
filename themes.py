# themes.py - Cấu hình theme và màu sắc cho ứng dụng

"""
File cấu hình theme và màu sắc cho ứng dụng Graph Coloring
Cho phép dễ dàng thay đổi và tùy chỉnh giao diện
"""

class Theme:
    """Base theme class"""
    def __init__(self):
        self.colors = {}
        self.fonts = {}
        self.sizes = {}

class ModernBlueTheme(Theme):
    """Theme màu xanh dương hiện đại"""
    def __init__(self):
        super().__init__()
        self.name = "Modern Blue"
        
        # Màu chủ đạo
        self.colors = {
            'primary': '#2C3E50',      # Dark Blue Gray
            'secondary': '#34495E',    # Darker Blue Gray  
            'accent': '#3498DB',       # Bright Blue
            'success': '#27AE60',      # Green
            'warning': '#F39C12',      # Orange
            'danger': '#E74C3C',       # Red
            'light': '#ECF0F1',        # Light Gray
            'white': '#FFFFFF',        # Pure White
            'canvas_bg': '#F8F9FA',    # Very Light Gray
            'button_bg': '#5DADE2',    # Light Blue
            'button_hover': '#3498DB', # Darker Blue
            'frame_bg': '#FFFFFF',     # White
            'text_primary': '#2C3E50', # Dark Gray
            'text_secondary': '#7F8C8D' # Medium Gray
        }
        
        # Palette màu cho đỉnh
        self.vertex_colors = [
            '#FF6B6B',  # Coral Red
            '#4ECDC4',  # Turquoise
            '#45B7D1',  # Sky Blue
            '#96CEB4',  # Mint Green
            '#FFEAA7',  # Warm Yellow
            '#DDA0DD',  # Plum
            '#98D8C8',  # Seafoam
            '#F7DC6F',  # Light Gold
            '#BB8FCE',  # Lavender
            '#85C1E9'   # Light Blue
        ]
        
        # Font
        self.fonts = {
            'title': ('Segoe UI', 18, 'bold'),
            'subtitle': ('Segoe UI', 11),
            'button': ('Segoe UI', 10, 'bold'),
            'label': ('Segoe UI', 11, 'bold'),
            'text': ('Segoe UI', 10),
            'mono': ('Consolas', 9),
            'vertex': ('Segoe UI', 12, 'bold')
        }

class DarkTheme(Theme):
    """Theme màu tối"""
    def __init__(self):
        super().__init__()
        self.name = "Dark"
        
        self.colors = {
            'primary': '#1A1A1A',      # Very Dark Gray
            'secondary': '#2D3748',    # Dark Blue Gray
            'accent': '#4FD1C7',       # Teal
            'success': '#48BB78',      # Green
            'warning': '#ED8936',      # Orange
            'danger': '#F56565',       # Red
            'light': '#2D3748',        # Dark Gray
            'white': '#FFFFFF',        # Pure White
            'canvas_bg': '#1A202C',    # Very Dark
            'button_bg': '#4FD1C7',    # Teal
            'button_hover': '#38B2AC', # Darker Teal
            'frame_bg': '#2D3748',     # Dark Gray
            'text_primary': '#F7FAFC', # Light Gray
            'text_secondary': '#A0AEC0' # Medium Gray
        }
        
        self.vertex_colors = [
            '#FF6B6B',  # Coral Red
            '#4FD1C7',  # Teal
            '#63B3ED',  # Blue
            '#68D391',  # Green
            '#F6E05E',  # Yellow
            '#D69E2E',  # Gold
            '#B794F6',  # Purple
            '#F687B3',  # Pink
            '#FC8181',  # Light Red
            '#81E6D9'   # Light Teal
        ]
        
        self.fonts = {
            'title': ('Segoe UI', 18, 'bold'),
            'subtitle': ('Segoe UI', 11),
            'button': ('Segoe UI', 10, 'bold'),
            'label': ('Segoe UI', 11, 'bold'),
            'text': ('Segoe UI', 10),
            'mono': ('Consolas', 9),
            'vertex': ('Segoe UI', 12, 'bold')
        }

class GreenTheme(Theme):
    """Theme màu xanh lá"""
    def __init__(self):
        super().__init__()
        self.name = "Green Nature"
        
        self.colors = {
            'primary': '#2F4F2F',      # Dark Forest Green
            'secondary': '#228B22',    # Forest Green
            'accent': '#32CD32',       # Lime Green
            'success': '#006400',      # Dark Green
            'warning': '#FF8C00',      # Dark Orange
            'danger': '#DC143C',       # Crimson
            'light': '#F0F8F0',        # Honeydew
            'white': '#FFFFFF',        # Pure White
            'canvas_bg': '#F5F5F5',    # WhiteSmoke
            'button_bg': '#32CD32',    # Lime Green
            'button_hover': '#228B22', # Forest Green
            'frame_bg': '#FFFFFF',     # White
            'text_primary': '#2F4F2F', # Dark Forest Green
            'text_secondary': '#556B2F' # Dark Olive Green
        }
        
        self.vertex_colors = [
            '#FF4500',  # Orange Red
            '#1E90FF',  # Dodger Blue
            '#FFD700',  # Gold
            '#FF69B4',  # Hot Pink
            '#8A2BE2',  # Blue Violet
            '#00CED1',  # Dark Turquoise
            '#FF1493',  # Deep Pink
            '#32CD32',  # Lime Green
            '#FF6347',  # Tomato
            '#4169E1'   # Royal Blue
        ]
        
        self.fonts = {
            'title': ('Segoe UI', 18, 'bold'),
            'subtitle': ('Segoe UI', 11),
            'button': ('Segoe UI', 10, 'bold'),
            'label': ('Segoe UI', 11, 'bold'),
            'text': ('Segoe UI', 10),
            'mono': ('Consolas', 9),
            'vertex': ('Segoe UI', 12, 'bold')
        }

class ThemeManager:
    """Quản lý theme của ứng dụng"""
    
    def __init__(self):
        self.themes = {
            'modern_blue': ModernBlueTheme(),
            'dark': DarkTheme(),
            'green': GreenTheme()
        }
        self.current_theme_name = 'modern_blue'
        self.current_theme = self.themes[self.current_theme_name]
    
    def get_available_themes(self):
        """Lấy danh sách theme có sẵn"""
        return list(self.themes.keys())
    
    def set_theme(self, theme_name):
        """Đặt theme hiện tại"""
        if theme_name in self.themes:
            self.current_theme_name = theme_name
            self.current_theme = self.themes[theme_name]
            return True
        return False
    
    def get_current_theme(self):
        """Lấy theme hiện tại"""
        return self.current_theme
    
    def get_color(self, color_name):
        """Lấy màu từ theme hiện tại"""
        return self.current_theme.colors.get(color_name, '#000000')
    
    def get_font(self, font_name):
        """Lấy font từ theme hiện tại"""
        return self.current_theme.fonts.get(font_name, ('Arial', 10))
    
    def get_vertex_colors(self):
        """Lấy palette màu cho đỉnh"""
        return self.current_theme.vertex_colors

# Singleton instance
theme_manager = ThemeManager()