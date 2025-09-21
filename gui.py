# gui.py - Giao diện người dùng cho ứng dụng tô màu đồ thị

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import math
import random
from graph import Graph
from graph_coloring import GraphColoringAlgorithm

class GraphColoringGUI:
    """Giao diện chính cho ứng dụng tô màu đồ thị"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("🎨 Thuật toán tô màu đồ thị - Phương pháp hạ bậc")
        self.root.geometry("1400x900")
        self.root.minsize(1200, 800)
        
        # Thiết lập theme và màu sắc
        self.setup_theme()
        
        self.graph = Graph()
        self.algorithm = None
        self.vertex_positions = {}  # Lưu vị trí các đỉnh trên canvas
        # Palette màu đẹp hơn với hex colors
        self.colors_palette = [
            "#FF0000",
            "#00FF2F",
            "#0D00FF",
            "#FFA200",
            "#D000FF",
            '#DDA0DD',
            '#98D8C8',
            '#F7DC6F',
            "#00B7FF",
            "#A441F5" 
        ]
        self.selected_vertex = None
        
        self.setup_ui()
    
    def setup_theme(self):
        """Thiết lập theme và màu sắc cho ứng dụng"""
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
        
        # Cấu hình style cho ttk
        style = ttk.Style()
        style.theme_use('clam')
        
        # Style cho buttons
        style.configure('Accent.TButton',
                       background=self.colors['button_bg'],
                       foreground='white',
                       font=('Segoe UI', 10, 'bold'),
                       padding=(10, 8))
        
        style.map('Accent.TButton',
                 background=[('active', self.colors['button_hover']),
                           ('pressed', self.colors['accent'])])
        
        # Style cho LabelFrame
        style.configure('Modern.TLabelframe',
                       background=self.colors['frame_bg'],
                       borderwidth=2,
                       relief='solid')
        
        style.configure('Modern.TLabelframe.Label',
                       background=self.colors['frame_bg'],
                       foreground=self.colors['text_primary'],
                       font=('Segoe UI', 11, 'bold'))
        
        # Style cho Combobox
        style.configure('Modern.TCombobox',
                       font=('Segoe UI', 10))
        
        # Cấu hình root window
        self.root.configure(bg=self.colors['light'])
        
    def setup_ui(self):
        """Thiết lập giao diện người dùng với thiết kế hiện đại và tab system"""
        # Main container với padding đẹp
        main_container = tk.Frame(self.root, bg=self.colors['light'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Tạo Notebook widget cho tabs
        self.notebook = ttk.Notebook(main_container)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Tab 1: Graph Coloring (giao diện hiện tại)
        self.graph_tab = tk.Frame(self.notebook, bg=self.colors['light'])
        self.notebook.add(self.graph_tab, text="🎨 Tô màu đồ thị")
        
        # Tab 2: Course Scheduling
        self.schedule_tab = tk.Frame(self.notebook, bg=self.colors['light'])
        self.notebook.add(self.schedule_tab, text="📅 Xếp lịch học")
        
        # Setup nội dung cho từng tab
        self.setup_graph_coloring_tab()
        self.setup_course_scheduling_tab()
        
        # Status bar chung
        self.setup_status_bar()
    
    def setup_graph_coloring_tab(self):
        """Thiết lập tab tô màu đồ thị (giao diện cũ)"""
        
        # Header với title đẹp
        header_frame = tk.Frame(self.graph_tab, bg=self.colors['primary'], height=60)
        header_frame.pack(fill=tk.X, pady=(0, 15))
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(header_frame, 
                              text="🎨 THUẬT TOÁN TÔ MÀU ĐỒ THỊ",
                              font=('Segoe UI', 18, 'bold'),
                              fg='white',
                              bg=self.colors['primary'])
        title_label.pack(expand=True)
        
        subtitle_label = tk.Label(header_frame,
                                 text="Phương pháp hạ bậc",
                                 font=('Segoe UI', 11),
                                 fg=self.colors['light'],
                                 bg=self.colors['primary'])
        subtitle_label.pack()
        
        # Frame chính với gradient effect
        content_frame = tk.Frame(self.graph_tab, bg=self.colors['light'])
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Frame trái - Canvas vẽ đồ thị với border đẹp
        left_frame = ttk.LabelFrame(content_frame, text="📊 Đồ thị", 
                                   style='Modern.TLabelframe', padding=15)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 15))
        
        # Canvas container với shadow effect
        canvas_container = tk.Frame(left_frame, bg='white', relief='solid', borderwidth=1)
        canvas_container.pack(fill=tk.BOTH, expand=True)
        
        # Canvas để vẽ đồ thị với grid background
        self.canvas = tk.Canvas(canvas_container, 
                               bg=self.colors['canvas_bg'], 
                               width=700, height=550,
                               highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.canvas.bind("<Button-3>", self.on_canvas_right_click)
        self.canvas.bind("<Motion>", self.on_canvas_motion)
        
        # Vẽ grid background
        self.draw_grid()
        
        # Frame phải - Điều khiển với design hiện đại
        right_frame = tk.Frame(content_frame, bg=self.colors['light'], width=350)
        right_frame.pack(side=tk.RIGHT, fill=tk.Y)
        right_frame.pack_propagate(False)
        
        # Tạo scrollable frame cho controls
        self.setup_control_panels(right_frame)
        
    def setup_control_panels(self, parent):
        """Thiết lập các panel điều khiển với thiết kế đẹp"""
        
        # Scrollable frame
        canvas_scroll = tk.Canvas(parent, bg=self.colors['light'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas_scroll.yview)
        scrollable_frame = tk.Frame(canvas_scroll, bg=self.colors['light'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas_scroll.configure(scrollregion=canvas_scroll.bbox("all"))
        )
        
        canvas_scroll.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas_scroll.configure(yscrollcommand=scrollbar.set)
        
        # 1. Nhóm thao tác với đồ thị
        graph_frame = ttk.LabelFrame(scrollable_frame, text="🔧 Thao tác đồ thị", 
                                    style='Modern.TLabelframe', padding=15)
        graph_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Tạo buttons với icons
        self.create_styled_button(graph_frame, "🗑️ Xóa tất cả", self.clear_graph, 'danger')
        
        # 2. Nhóm thuật toán
        algo_frame = ttk.LabelFrame(scrollable_frame, text="🎯 Thuật toán tô màu", 
                                   style='Modern.TLabelframe', padding=15)
        algo_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.create_styled_button(algo_frame, "▶️ Chạy thuật toán", self.run_algorithm, 'success')
        self.create_styled_button(algo_frame, "🎨 Xóa màu", self.clear_colors, 'warning')
        self.create_styled_button(algo_frame, "🔍 Tìm số màu tối thiểu", self.find_minimum_colors, 'accent')
        self.create_styled_button(algo_frame, "🌈 Xem theo thứ tự màu", self.show_color_ordering, 'accent')
        
        # Pack scrollable components
        canvas_scroll.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def setup_course_scheduling_tab(self):
        """Thiết lập tab xếp lịch học"""
        # Header
        header_frame = tk.Frame(self.schedule_tab, bg=self.colors['accent'], height=60)
        header_frame.pack(fill=tk.X, pady=(0, 15))
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(header_frame, 
                              text="📅 XẾP LỊCH HỌC TỰ ĐỘNG",
                              font=('Segoe UI', 18, 'bold'),
                              fg='white',
                              bg=self.colors['accent'])
        title_label.pack(expand=True)
        
        subtitle_label = tk.Label(header_frame,
                                 text="Sử dụng thuật toán tô màu đồ thị để xếp lịch không xung đột",
                                 font=('Segoe UI', 11),
                                 fg='white',
                                 bg=self.colors['accent'])
        subtitle_label.pack()
        
        # Main content
        content_frame = tk.Frame(self.schedule_tab, bg=self.colors['light'])
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left panel - Course management
        left_frame = ttk.LabelFrame(content_frame, text="📚 Quản lý lịch học", 
                                   style='Modern.TLabelframe', padding=15)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 15))
        
        # Instructions
        instruction_frame = tk.Frame(left_frame, bg=self.colors['frame_bg'])
        instruction_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Course list
        courses_list_frame = tk.Frame(left_frame, bg=self.colors['frame_bg'])
        courses_list_frame.pack(fill=tk.BOTH, expand=True, pady=(15, 0))
        
        tk.Label(courses_list_frame, text="📋 Danh sách môn học:",
                font=('Segoe UI', 10, 'bold'),
                bg=self.colors['frame_bg']).pack(anchor=tk.W)
        
        # Listbox với scrollbar
        list_container = tk.Frame(courses_list_frame, bg=self.colors['frame_bg'])
        list_container.pack(fill=tk.BOTH, expand=True, pady=(5, 10))
        
        self.courses_listbox = tk.Listbox(list_container, font=('Segoe UI', 9),
                                         relief='solid', borderwidth=1,
                                         selectmode=tk.SINGLE, state=tk.DISABLED)
        courses_scrollbar = ttk.Scrollbar(list_container, orient="vertical", 
                                         command=self.courses_listbox.yview)
        self.courses_listbox.configure(yscrollcommand=courses_scrollbar.set)
        
        self.courses_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        courses_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Action buttons
        action_frame = tk.Frame(left_frame, bg=self.colors['frame_bg'])
        action_frame.pack(fill=tk.X, pady=(15, 0))
        

        self.create_styled_button(action_frame, "� Chuyển từ đồ thị", 
                                 self.convert_from_graph, 'success')
        self.create_styled_button(action_frame, "�📅 Tạo lịch học", 
                                 self.generate_schedule, 'accent')
        
        # Right panel - Schedule visualization
        right_frame = ttk.LabelFrame(content_frame, text="📊 Lịch học", 
                                    style='Modern.TLabelframe', padding=15)
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Schedule canvas
        self.schedule_canvas = tk.Canvas(right_frame, bg='white', 
                                        relief='solid', borderwidth=1)
        schedule_scroll_v = ttk.Scrollbar(right_frame, orient="vertical", 
                                         command=self.schedule_canvas.yview)
        schedule_scroll_h = ttk.Scrollbar(right_frame, orient="horizontal", 
                                         command=self.schedule_canvas.xview)
        
        self.schedule_canvas.configure(yscrollcommand=schedule_scroll_v.set,
                                      xscrollcommand=schedule_scroll_h.set)
        
        self.schedule_canvas.pack(side="left", fill="both", expand=True)
        schedule_scroll_v.pack(side="right", fill="y")
        schedule_scroll_h.pack(side="bottom", fill="x")
        
        # Initialize course data
        self.courses = {}  # {course_name: vertex_id}
        self.course_graph = Graph()
        self.current_course_id = 0
    
    def create_styled_button(self, parent, text, command, color_type):
        """Tạo button với style đẹp"""
        color = self.colors.get(color_type, self.colors['accent'])
        
        btn = tk.Button(parent, text=text, command=command,
                       font=('Segoe UI', 10, 'bold'),
                       bg=color,
                       fg='white',
                       relief='flat',
                       borderwidth=0,
                       cursor='hand2',
                       padx=15, pady=8)
        
        # Hover effects
        def on_enter(e):
            btn.config(bg=self.lighten_color(color))
        
        def on_leave(e):
            btn.config(bg=color)
        
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        btn.pack(fill=tk.X, pady=3)
        
        return btn
    
    def lighten_color(self, color):
        """Làm sáng màu cho hover effect"""
        # Simple color lightening
        color_map = {
            self.colors['success']: '#2ECC71',
            self.colors['danger']: '#EC7063',
            self.colors['warning']: '#F8C471',
            self.colors['accent']: '#5DADE2'
        }
        return color_map.get(color, '#5DADE2')
    
    def setup_status_bar(self):
        """Thiết lập status bar đẹp"""
        status_frame = tk.Frame(self.root, bg=self.colors['secondary'], height=30)
        status_frame.pack(side=tk.BOTTOM, fill=tk.X)
        status_frame.pack_propagate(False)
        
        self.status_var = tk.StringVar(value="🟢 Sẵn sàng")
        status_label = tk.Label(status_frame, textvariable=self.status_var,
                               bg=self.colors['secondary'],
                               fg='white',
                               font=('Segoe UI', 10),
                               anchor='w')
        status_label.pack(side=tk.LEFT, padx=15, pady=5)
        
        # Thời gian
        time_label = tk.Label(status_frame,
                             text="Thuật toán hạ bậc truyền thống",
                             bg=self.colors['secondary'],
                             fg=self.colors['light'],
                             font=('Segoe UI', 10))
        time_label.pack(side=tk.RIGHT, padx=15, pady=5)
    
    def draw_grid(self):
        """Vẽ lưới nền cho canvas"""
        # Xóa grid cũ
        self.canvas.delete("grid")
        
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        
        if width <= 1 or height <= 1:
            self.canvas.after(100, self.draw_grid)
            return
        
        # Vẽ lưới với màu nhạt
        grid_size = 20
        for i in range(0, width, grid_size):
            self.canvas.create_line(i, 0, i, height, fill='#E8E8E8', width=1, tags="grid")
        
        for i in range(0, height, grid_size):
            self.canvas.create_line(0, i, width, i, fill='#E8E8E8', width=1, tags="grid")
        
    def on_canvas_motion(self, event):
        """Xử lý di chuyển chuột trên canvas để hiển thị hover effects"""
        x, y = event.x, event.y
        hovered_vertex = self.find_vertex_at_position(x, y)
        
        if hovered_vertex:
            self.canvas.config(cursor="hand2")
            # Có thể thêm highlight effect ở đây
        else:
            self.canvas.config(cursor="")
    
    def on_canvas_click(self, event):
        """Xử lý click trên canvas"""
        x, y = event.x, event.y
        
        # Kiểm tra xem có click vào đỉnh nào không
        clicked_vertex = self.find_vertex_at_position(x, y)
        
        if clicked_vertex:
            if self.selected_vertex is None:
                self.selected_vertex = clicked_vertex
                self.status_var.set(f"🎯 Đã chọn đỉnh {clicked_vertex}")
            else:
                if self.selected_vertex == clicked_vertex:
                    self.selected_vertex = None
                    self.status_var.set("🔄 Bỏ chọn đỉnh")
                else:
                    # Thêm cạnh giữa hai đỉnh
                    if clicked_vertex not in self.graph.get_neighbors(self.selected_vertex):
                        self.graph.add_edge(self.selected_vertex, clicked_vertex)
                        self.status_var.set(f"✅ Đã thêm cạnh {self.selected_vertex}-{clicked_vertex}")
                    else:
                        self.status_var.set(f"⚠️ Cạnh {self.selected_vertex}-{clicked_vertex} đã tồn tại")
                    self.selected_vertex = None
        else:
            # Thêm đỉnh mới tại vị trí click
            self.add_vertex_at_position(x, y)
            self.selected_vertex = None
        
        self.draw_graph()
    
    def on_canvas_right_click(self, event):
        """Xử lý right click - xóa đỉnh hoặc cạnh"""
        x, y = event.x, event.y
        clicked_vertex = self.find_vertex_at_position(x, y)
        
        if clicked_vertex:
            self.graph.remove_vertex(clicked_vertex)
            if clicked_vertex in self.vertex_positions:
                del self.vertex_positions[clicked_vertex]
            self.status_var.set(f"🗑️ Đã xóa đỉnh {clicked_vertex}")
            self.selected_vertex = None
            self.draw_graph()
    
    def find_vertex_at_position(self, x, y):
        """Tìm đỉnh tại vị trí (x, y)"""
        for vertex, (vx, vy) in self.vertex_positions.items():
            if math.sqrt((x - vx)**2 + (y - vy)**2) <= 20:  # Bán kính đỉnh = 20
                return vertex
        return None
    
    def add_vertex_at_position(self, x, y):
        """Thêm đỉnh tại vị trí (x, y)"""
        # Tạo tên đỉnh mới
        existing_vertices = list(self.graph.vertices)
        if not existing_vertices:
            new_vertex = 'A'
        else:
            # Tìm chữ cái tiếp theo
            last_char = max(existing_vertices)
            if last_char.isalpha() and len(last_char) == 1:
                new_vertex = chr(ord(last_char) + 1)
            else:
                new_vertex = f"V{len(existing_vertices)}"
        
        self.graph.add_vertex(new_vertex)
        self.vertex_positions[new_vertex] = (x, y)
        self.status_var.set(f"➕ Đã thêm đỉnh {new_vertex}")
    
    def add_vertex(self):
        """Thêm đỉnh mới"""
        vertex_name = simpledialog.askstring("Thêm đỉnh", "Nhập tên đỉnh:")
        if vertex_name and vertex_name not in self.graph.vertices:
            self.graph.add_vertex(vertex_name)
            # Đặt vị trí ngẫu nhiên
            x = random.randint(50, 550)
            y = random.randint(50, 450)
            self.vertex_positions[vertex_name] = (x, y)
            self.draw_graph()
            self.status_var.set(f"➕ Đã thêm đỉnh {vertex_name}")
        elif vertex_name in self.graph.vertices:
            messagebox.showwarning("⚠️ Cảnh báo", "Đỉnh đã tồn tại!")
    
    def remove_vertex(self):
        """Xóa đỉnh"""
        if not self.graph.vertices:
            messagebox.showinfo("ℹ️ Thông báo", "Đồ thị không có đỉnh nào!")
            return
        
        vertices = list(self.graph.vertices)
        vertex = simpledialog.askstring("🗑️ Xóa đỉnh", f"Nhập tên đỉnh cần xóa ({', '.join(vertices)}):")
        if vertex and vertex in self.graph.vertices:
            self.graph.remove_vertex(vertex)
            if vertex in self.vertex_positions:
                del self.vertex_positions[vertex]
            self.draw_graph()
            self.status_var.set(f"🗑️ Đã xóa đỉnh {vertex}")
        elif vertex:
            messagebox.showerror("❌ Lỗi", "Đỉnh không tồn tại!")
    
    def add_edge_dialog(self):
        """Dialog thêm cạnh"""
        if len(self.graph.vertices) < 2:
            messagebox.showinfo("ℹ️ Thông báo", "Cần ít nhất 2 đỉnh để tạo cạnh!")
            return
        
        vertices = list(self.graph.vertices)
        edge_str = simpledialog.askstring("🔗 Thêm cạnh", 
            f"Nhập cạnh dưới dạng 'đỉnh1 đỉnh2' ({', '.join(vertices)}):")
        
        if edge_str:
            try:
                v1, v2 = edge_str.split()
                if v1 in self.graph.vertices and v2 in self.graph.vertices:
                    if v2 not in self.graph.get_neighbors(v1):
                        self.graph.add_edge(v1, v2)
                        self.draw_graph()
                        self.status_var.set(f"✅ Đã thêm cạnh {v1}-{v2}")
                    else:
                        messagebox.showinfo("ℹ️ Thông báo", "Cạnh đã tồn tại!")
                else:
                    messagebox.showerror("❌ Lỗi", "Một hoặc cả hai đỉnh không tồn tại!")
            except ValueError:
                messagebox.showerror("❌ Lỗi", "Định dạng không đúng! Sử dụng: 'đỉnh1 đỉnh2'")
    
    def remove_edge_dialog(self):
        """Dialog xóa cạnh"""
        edge_str = simpledialog.askstring("✂️ Xóa cạnh", "Nhập cạnh cần xóa dưới dạng 'đỉnh1 đỉnh2':")
        
        if edge_str:
            try:
                v1, v2 = edge_str.split()
                if v1 in self.graph.vertices and v2 in self.graph.vertices:
                    if v2 in self.graph.get_neighbors(v1):
                        self.graph.remove_edge(v1, v2)
                        self.draw_graph()
                        self.status_var.set(f"✂️ Đã xóa cạnh {v1}-{v2}")
                    else:
                        messagebox.showinfo("ℹ️ Thông báo", "Cạnh không tồn tại!")
                else:
                    messagebox.showerror("❌ Lỗi", "Một hoặc cả hai đỉnh không tồn tại!")
            except ValueError:
                messagebox.showerror("❌ Lỗi", "Định dạng không đúng! Sử dụng: 'đỉnh1 đỉnh2'")
    
    def clear_graph(self):
        """Xóa toàn bộ đồ thị"""
        if messagebox.askyesno("❓ Xác nhận", "Bạn có chắc muốn xóa toàn bộ đồ thị?"):
            self.graph = Graph()
            self.vertex_positions = {}
            self.selected_vertex = None
            self.simulation_steps = []
            self.current_step = 0
            self.draw_graph()
            self.status_var.set("🗑️ Đã xóa toàn bộ đồ thị")
    
    def generate_vertex_positions(self):
        """Tạo vị trí cho các đỉnh theo hình tròn"""
        vertices = list(self.graph.vertices)
        n = len(vertices)
        
        center_x, center_y = 300, 250
        radius = 150
        
        if n == 1:
            self.vertex_positions[vertices[0]] = (center_x, center_y)
        else:
            for i, vertex in enumerate(vertices):
                angle = 2 * math.pi * i / n
                x = center_x + radius * math.cos(angle)
                y = center_y + radius * math.sin(angle)
                self.vertex_positions[vertex] = (x, y)
    
    def draw_graph(self):
        """Vẽ đồ thị lên canvas với hiệu ứng đẹp"""
        self.canvas.delete("graph")  # Xóa graph cũ, giữ lại grid
        
        # Vẽ cạnh với shadow effect
        for vertex in self.graph.vertices:
            if vertex in self.vertex_positions:
                x1, y1 = self.vertex_positions[vertex]
                for neighbor in self.graph.get_neighbors(vertex):
                    if neighbor in self.vertex_positions:
                        x2, y2 = self.vertex_positions[neighbor]
                        
                        # Shadow effect cho cạnh
                        self.canvas.create_line(x1+2, y1+2, x2+2, y2+2, 
                                              width=3, fill="#D5D5D5", tags="graph")
                        
                        # Cạnh chính
                        self.canvas.create_line(x1, y1, x2, y2, 
                                              width=3, fill=self.colors['primary'], 
                                              capstyle=tk.ROUND, tags="graph")
        
        # Vẽ đỉnh với gradient và shadow effects
        for vertex in self.graph.vertices:
            if vertex in self.vertex_positions:
                x, y = self.vertex_positions[vertex]
                
                # Chọn màu
                if self.graph.colors[vertex] is not None:
                    color_index = self.graph.colors[vertex]
                    if color_index < len(self.colors_palette):
                        color = self.colors_palette[color_index]
                    else:
                        color = "#CCCCCC"
                else:
                    color = "#F8F9FA"
                
                # Highlight nếu được chọn
                if vertex == self.selected_vertex:
                    ring_color = self.colors['warning']
                    ring_width = 4
                else:
                    ring_color = self.colors['primary']
                    ring_width = 2
                
                # Shadow cho đỉnh
                self.canvas.create_oval(x-22, y-22, x+22, y+22, 
                                      fill="#D0D0D0", outline="", tags="graph")
                
                # Outer ring
                self.canvas.create_oval(x-20, y-20, x+20, y+20, 
                                      fill=ring_color, outline="", tags="graph")
                
                # Inner circle với màu
                self.canvas.create_oval(x-18, y-18, x+18, y+18, 
                                      fill=color, outline="white", width=2, tags="graph")
                
                # Tên đỉnh với font đẹp
                self.canvas.create_text(x, y-2, text=vertex, 
                                      font=('Segoe UI', 12, 'bold'), 
                                      fill='white' if self.is_dark_color(color) else self.colors['text_primary'],
                                      tags="graph")
                
                # Hiển thị bậc với background
                degree = self.graph.get_degree(vertex)
                degree_bg = self.canvas.create_oval(x-8, y-38, x+8, y-25, 
                                                  fill=self.colors['accent'], outline="", tags="graph")
                self.canvas.create_text(x, y-31, text=str(degree), 
                                      font=('Segoe UI', 8, 'bold'), 
                                      fill='white', tags="graph")

    def is_dark_color(self, color):
        """Kiểm tra xem màu có tối không để chọn màu text phù hợp"""
        dark_colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#DDA0DD', '#98D8C8', '#BB8FCE', '#85C1E9']
        return color in dark_colors
    
    def run_algorithm(self):
        """Chạy thuật toán tô màu (luôn chọn màu nhỏ nhất có thể)"""
        if not self.graph.vertices:
            messagebox.showinfo("ℹ️ Thông báo", "Đồ thị không có đỉnh nào!")
            return
        
        self.algorithm = GraphColoringAlgorithm(self.graph)
        success = self.algorithm.degree_reduction_coloring()
        
        if success:
            self.draw_graph()
            
            chromatic_number = self.graph.get_chromatic_number()
            self.status_var.set(f"✅ Thuật toán hoàn thành! Số màu sử dụng: {chromatic_number} (tối ưu)")
        else:
            messagebox.showerror("❌ Lỗi", "Không thể tô màu đồ thị!")
    
    def clear_colors(self):
        """Xóa tất cả màu"""
        self.graph.clear_colors()
        self.draw_graph()
        self.status_var.set("🎨 Đã xóa tất cả màu")
    
    def find_minimum_colors(self):
        """Tìm số màu tối thiểu"""
        if not self.graph.vertices:
            messagebox.showinfo("ℹ️ Thông báo", "Đồ thị không có đỉnh nào!")
            return
        
        self.algorithm = GraphColoringAlgorithm(self.graph)
        min_colors = self.algorithm.find_minimum_colors()
        
        messagebox.showinfo("🔍 Kết quả", f"Số màu tối thiểu cần thiết: {min_colors}")
        self.status_var.set(f"🔍 Số màu tối thiểu: {min_colors}")
    
    def show_color_ordering(self):
        """Hiển thị thứ tự màu và thông tin chi tiết"""
        if not self.graph.vertices:
            messagebox.showinfo("ℹ️ Thông báo", "Đồ thị không có đỉnh nào!")
            return
        
        # Kiểm tra xem đã tô màu chưa
        colored_vertices = [(v, c) for v, c in self.graph.colors.items() if c is not None]
        if not colored_vertices:
            messagebox.showinfo("ℹ️ Thông báo", "Chưa có đỉnh nào được tô màu! Hãy chạy thuật toán trước.")
            return
        
        # Tạo cửa sổ mới hiển thị thứ tự màu
        self.create_color_ordering_window()
    
    def create_color_ordering_window(self):
        """Tạo cửa sổ hiển thị thứ tự màu"""
        color_window = tk.Toplevel(self.root)
        color_window.title("🌈 Thứ tự màu đồ thị")
        color_window.geometry("500x600")
        color_window.configure(bg=self.colors['light'])
        
        # Header
        header_frame = tk.Frame(color_window, bg=self.colors['primary'], height=60)
        header_frame.pack(fill=tk.X, pady=(0, 15))
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(header_frame, 
                              text="🌈 THỨ TỰ MÀU ĐỒ THỊ",
                              font=('Segoe UI', 16, 'bold'),
                              fg='white',
                              bg=self.colors['primary'])
        title_label.pack(expand=True)
        
        # Main content frame
        content_frame = tk.Frame(color_window, bg=self.colors['light'])
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Tạo thông tin tổng quan
        overview_frame = ttk.LabelFrame(content_frame, text="📊 Tổng quan", 
                                       style='Modern.TLabelframe', padding=15)
        overview_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Thống kê màu
        color_stats = self.get_color_statistics()
        stats_text = f"🎨 Tổng số màu sử dụng: {color_stats['total_colors']}\n"
        stats_text += f"📊 Số đỉnh đã tô: {color_stats['colored_vertices']}\n"
        stats_text += f"⚪ Số đỉnh chưa tô: {color_stats['uncolored_vertices']}"
        
        stats_label = tk.Label(overview_frame, text=stats_text,
                              font=('Segoe UI', 11),
                              fg=self.colors['text_primary'],
                              bg=self.colors['frame_bg'],
                              justify=tk.LEFT)
        stats_label.pack(anchor=tk.W)
        
        # Chi tiết theo màu
        details_frame = ttk.LabelFrame(content_frame, text="🎨 Chi tiết theo màu", 
                                      style='Modern.TLabelframe', padding=15)
        details_frame.pack(fill=tk.BOTH, expand=True)
        
        # Scrollable frame cho details
        canvas_scroll = tk.Canvas(details_frame, bg=self.colors['frame_bg'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(details_frame, orient="vertical", command=canvas_scroll.yview)
        scrollable_frame = tk.Frame(canvas_scroll, bg=self.colors['frame_bg'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas_scroll.configure(scrollregion=canvas_scroll.bbox("all"))
        )
        
        canvas_scroll.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas_scroll.configure(yscrollcommand=scrollbar.set)
        
        # Tạo chi tiết cho từng màu
        self.create_color_details(scrollable_frame, color_stats['color_groups'])
        
        canvas_scroll.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Buttons frame
        buttons_frame = tk.Frame(color_window, bg=self.colors['light'])
        buttons_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Export button
        export_btn = tk.Button(buttons_frame, text="📤 Xuất báo cáo",
                              command=lambda: self.export_color_report(color_stats),
                              font=('Segoe UI', 10, 'bold'),
                              bg=self.colors['accent'],
                              fg='white',
                              relief='flat',
                              cursor='hand2',
                              padx=15, pady=8)
        export_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Close button
        close_btn = tk.Button(buttons_frame, text="❌ Đóng",
                             command=color_window.destroy,
                             font=('Segoe UI', 10, 'bold'),
                             bg=self.colors['danger'],
                             fg='white',
                             relief='flat',
                             cursor='hand2',
                             padx=15, pady=8)
        close_btn.pack(side=tk.RIGHT)
        
        # Đặt focus cho cửa sổ mới
        color_window.focus()
        color_window.grab_set()  # Modal window
    
    def get_color_statistics(self):
        """Lấy thống kê về màu sắc"""
        color_groups = {}
        total_colors = 0
        colored_vertices = 0
        uncolored_vertices = 0
        
        for vertex, color in self.graph.colors.items():
            if color is not None:
                colored_vertices += 1
                if color not in color_groups:
                    color_groups[color] = []
                color_groups[color].append(vertex)
            else:
                uncolored_vertices += 1
        
        total_colors = len(color_groups)
        
        # Sắp xếp vertices trong mỗi nhóm màu
        for color in color_groups:
            color_groups[color].sort()
        
        return {
            'total_colors': total_colors,
            'colored_vertices': colored_vertices,
            'uncolored_vertices': uncolored_vertices,
            'color_groups': color_groups
        }
    
    def create_color_details(self, parent, color_groups):
        """Tạo chi tiết cho từng màu"""
        for color_index in sorted(color_groups.keys()):
            vertices = color_groups[color_index]
            
            # Frame cho mỗi màu
            color_frame = tk.Frame(parent, bg=self.colors['frame_bg'], relief='solid', borderwidth=1)
            color_frame.pack(fill=tk.X, pady=5, padx=5)
            
            # Header cho màu
            header_frame = tk.Frame(color_frame, bg=self.colors['frame_bg'])
            header_frame.pack(fill=tk.X, padx=10, pady=(10, 5))
            
            # Màu sắc sample
            if color_index < len(self.colors_palette):
                color_hex = self.colors_palette[color_index]
            else:
                color_hex = "#CCCCCC"
            
            color_sample = tk.Label(header_frame, text="●", 
                                   font=('Segoe UI', 20, 'bold'),
                                   fg=color_hex,
                                   bg=self.colors['frame_bg'])
            color_sample.pack(side=tk.LEFT, padx=(0, 10))
            
            # Thông tin màu
            color_info = tk.Label(header_frame, 
                                 text=f"Màu {color_index} ({len(vertices)} đỉnh)",
                                 font=('Segoe UI', 12, 'bold'),
                                 fg=self.colors['text_primary'],
                                 bg=self.colors['frame_bg'])
            color_info.pack(side=tk.LEFT)
            
            # Danh sách đỉnh
            vertices_frame = tk.Frame(color_frame, bg=self.colors['frame_bg'])
            vertices_frame.pack(fill=tk.X, padx=20, pady=(0, 10))
            
            vertices_text = "📍 Các đỉnh: " + ", ".join(vertices)
            vertices_label = tk.Label(vertices_frame, text=vertices_text,
                                     font=('Segoe UI', 10),
                                     fg=self.colors['text_secondary'],
                                     bg=self.colors['frame_bg'],
                                     wraplength=400,
                                     justify=tk.LEFT)
            vertices_label.pack(anchor=tk.W)
            
            # Thông tin bổ sung về màu này
            color_details = self.get_color_details_info(color_index, vertices)
            if color_details:
                details_label = tk.Label(vertices_frame, text=color_details,
                                        font=('Segoe UI', 9),
                                        fg=self.colors['text_secondary'],
                                        bg=self.colors['frame_bg'],
                                        wraplength=400,
                                        justify=tk.LEFT)
                details_label.pack(anchor=tk.W, pady=(5, 0))
    
    def get_color_details_info(self, color_index, vertices):
        """Lấy thông tin chi tiết về một màu"""
        details = []
        
        # Tính tổng bậc của các đỉnh cùng màu
        total_degree = sum(self.graph.get_degree(v) for v in vertices)
        avg_degree = total_degree / len(vertices) if vertices else 0
        
        details.append(f"💹 Tổng bậc: {total_degree}")
        details.append(f"📊 Bậc trung bình: {avg_degree:.1f}")
        
        # Kiểm tra tính độc lập (không có cạnh nối giữa các đỉnh cùng màu)
        is_independent = True
        for i, v1 in enumerate(vertices):
            for v2 in vertices[i+1:]:
                if v2 in self.graph.get_neighbors(v1):
                    is_independent = False
                    break
            if not is_independent:
                break
        
        if is_independent:
            details.append("✅ Tập độc lập (không có cạnh nội bộ)")
        else:
            details.append("❌ Có cạnh nối giữa các đỉnh cùng màu")
        
        return " | ".join(details)
    
    def export_color_report(self, color_stats):
        """Xuất báo cáo màu ra file"""
        try:
            filename = f"color_report_{len(self.graph.vertices)}vertices_{color_stats['total_colors']}colors.txt"
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("🌈 BÁO CÁO THỨ TỰ MÀU ĐỒ THỊ\n")
                f.write("=" * 50 + "\n\n")
                
                f.write("📊 TỔNG QUAN:\n")
                f.write(f"   • Tổng số màu sử dụng: {color_stats['total_colors']}\n")
                f.write(f"   • Số đỉnh đã tô: {color_stats['colored_vertices']}\n")
                f.write(f"   • Số đỉnh chưa tô: {color_stats['uncolored_vertices']}\n\n")
                
                f.write("🎨 CHI TIẾT THEO MÀU:\n")
                f.write("-" * 50 + "\n")
                
                for color_index in sorted(color_stats['color_groups'].keys()):
                    vertices = color_stats['color_groups'][color_index]
                    f.write(f"\n🎨 Màu {color_index}:\n")
                    f.write(f"   📍 Các đỉnh: {', '.join(vertices)}\n")
                    f.write(f"   📊 Số lượng: {len(vertices)} đỉnh\n")
                    
                    # Thông tin chi tiết
                    details = self.get_color_details_info(color_index, vertices)
                    f.write(f"   💹 Chi tiết: {details}\n")
                
                f.write(f"\n📅 Thời gian tạo: {self.get_current_time()}\n")
                f.write("🔧 Thuật toán: Degree Reduction Algorithm\n")
            
            messagebox.showinfo("✅ Thành công", f"Đã xuất báo cáo ra file: {filename}")
            self.status_var.set(f"📤 Đã xuất báo cáo: {filename}")
            
        except Exception as e:
            messagebox.showerror("❌ Lỗi", f"Không thể xuất báo cáo: {str(e)}")
    
    # ================== XỬ LÝ TAB XẾP LỊCH ==================
    
    def convert_from_graph(self):
        """Chuyển đồ thị hiện tại sang dạng lịch học"""
        if not self.graph.vertices:
            messagebox.showwarning("⚠️ Cảnh báo", "Đồ thị hiện tại trống! Vui lòng tạo đồ thị trước.")
            return
        
        # Xác nhận với người dùng
        result = messagebox.askyesno("🔄 Chuyển đổi", 
                                   f"Chuyển đồ thị hiện tại ({len(self.graph.vertices)} đỉnh) sang lịch học?\n" +
                                   "Dữ liệu lịch học hiện tại sẽ bị xóa!")
        if not result:
            return
        
        # Xóa dữ liệu cũ
        self.courses.clear()
        self.course_graph = Graph()
        self.courses_listbox.config(state=tk.NORMAL)  # Enable trước khi xóa và thêm
        self.courses_listbox.delete(0, tk.END)
        self.current_course_id = 0
        
        # Chuyển đổi đỉnh thành môn học
        vertex_list = sorted(list(self.graph.vertices))
        for i, vertex in enumerate(vertex_list):
            course_name = f"Môn {vertex}"
            self.courses[course_name] = i
            self.course_graph.add_vertex(str(i))
            self.courses_listbox.insert(tk.END, course_name)
            self.current_course_id = i + 1
        
        # Chuyển đổi cạnh thành xung đột
        edges_added = 0
        for vertex in vertex_list:
            vertex_idx = vertex_list.index(vertex)
            for neighbor in self.graph.adj_list.get(vertex, set()):
                neighbor_idx = vertex_list.index(neighbor)
                if vertex_idx < neighbor_idx:  # Tránh thêm cạnh trùng lặp
                    self.course_graph.add_edge(str(vertex_idx), str(neighbor_idx))
                    edges_added += 1
        
        # Cập nhật canvas xếp lịch
        self.schedule_canvas.delete("all")
        
        messagebox.showinfo("✅ Thành công", 
                          f"Đã chuyển đổi thành công!\n" +
                          f"📚 Số môn học: {len(self.courses)}\n" +
                          f"⚠️ Số xung đột: {edges_added}")
    
    def add_course(self):
        """Thêm môn học mới"""
        course_name = self.course_entry.get().strip()
        if not course_name:
            messagebox.showwarning("⚠️ Cảnh báo", "Vui lòng nhập tên môn học!")
            return
        
        if course_name in self.courses:
            messagebox.showwarning("⚠️ Cảnh báo", f"Môn học '{course_name}' đã tồn tại!")
            return
        
        # Thêm môn học
        self.courses[course_name] = self.current_course_id
        self.course_graph.add_vertex(str(self.current_course_id))
        self.current_course_id += 1
        
        # Cập nhật danh sách
        self.courses_listbox.insert(tk.END, course_name)
        self.course_entry.delete(0, tk.END)
        
        messagebox.showinfo("✅ Thành công", f"Đã thêm môn học: {course_name}")
    
    def remove_course(self):
        """Xóa môn học đã chọn"""
        selection = self.courses_listbox.curselection()
        if not selection:
            messagebox.showwarning("⚠️ Cảnh báo", "Vui lòng chọn môn học để xóa!")
            return
        
        index = selection[0]
        course_name = self.courses_listbox.get(index)
        
        # Xóa khỏi danh sách và đồ thị
        course_id = str(self.courses[course_name])
        self.course_graph.remove_vertex(course_id)
        del self.courses[course_name]
        
        # Cập nhật giao diện
        self.courses_listbox.delete(index)
        
        messagebox.showinfo("✅ Thành công", f"Đã xóa môn học: {course_name}")
    
    def add_conflict(self):
        """Thêm xung đột giữa hai môn học"""
        conflict_text = self.conflict_entry.get().strip()
        if not conflict_text:
            messagebox.showwarning("⚠️ Cảnh báo", "Vui lòng nhập tên hai môn học!")
            return
        
        # Phân tích input (có thể là "Môn A, Môn B" hoặc "Môn A - Môn B")
        parts = None
        if ',' in conflict_text:
            parts = conflict_text.split(',')
        elif '-' in conflict_text:
            parts = conflict_text.split('-')
        else:
            messagebox.showwarning("⚠️ Cảnh báo", "Vui lòng nhập theo định dạng: 'Môn A, Môn B' hoặc 'Môn A - Môn B'")
            return
        
        if len(parts) != 2:
            messagebox.showwarning("⚠️ Cảnh báo", "Vui lòng nhập đúng hai môn học!")
            return
        
        course1 = parts[0].strip()
        course2 = parts[1].strip()
        
        # Kiểm tra môn học có tồn tại
        if course1 not in self.courses:
            messagebox.showwarning("⚠️ Cảnh báo", f"Môn học '{course1}' không tồn tại!")
            return
        
        if course2 not in self.courses:
            messagebox.showwarning("⚠️ Cảnh báo", f"Môn học '{course2}' không tồn tại!")
            return
        
        if course1 == course2:
            messagebox.showwarning("⚠️ Cảnh báo", "Không thể tạo xung đột với chính môn học đó!")
            return
        
        # Thêm cạnh vào đồ thị
        vertex1 = str(self.courses[course1])
        vertex2 = str(self.courses[course2])
        
        self.course_graph.add_edge(vertex1, vertex2)
        self.conflict_entry.delete(0, tk.END)
        
        messagebox.showinfo("✅ Thành công", f"Đã thêm xung đột: {course1} ↔ {course2}")
    
    def generate_schedule(self):
        """Tạo lịch học sử dụng thuật toán tô màu đồ thị"""
        if not self.courses:
            messagebox.showwarning("⚠️ Cảnh báo", "Vui lòng thêm ít nhất một môn học!")
            return
        
        # Sử dụng thuật toán tô màu
        algorithm = GraphColoringAlgorithm(self.course_graph)
        success = algorithm.degree_reduction_coloring()
        
        if not success:
            messagebox.showerror("❌ Lỗi", "Không thể tạo lịch học!")
            return
        
        # Lấy kết quả tô màu từ đồ thị
        coloring = {}
        for vertex_id in self.course_graph.vertices:
            color = self.course_graph.colors.get(vertex_id)
            if color is not None:
                coloring[vertex_id] = color
        
        # Tạo lịch theo ca học với thứ tự cố định
        time_slots = [
            "Ca 1 (7:00-9:00)", 
            "Ca 2 (9:00-11:00)", 
            "Ca 3 (13:00-15:00)", 
            "Ca 4 (15:00-17:00)", 
            "Ca 5 (17:00-19:00)"
        ]
        
        schedule = {}
        for course_name, course_id in self.courses.items():
            color = coloring.get(str(course_id), 0)
            slot_index = color % len(time_slots)
            slot_name = time_slots[slot_index]
            
            if slot_name not in schedule:
                schedule[slot_name] = []
            schedule[slot_name].append(course_name)
        
        # Hiển thị lịch
        self.display_schedule(schedule)
        messagebox.showinfo("✅ Thành công", "Đã tạo lịch học thành công!")
    
    def display_schedule(self, schedule):
        """Hiển thị lịch học trên canvas theo thứ tự ca"""
        # Xóa nội dung cũ
        self.schedule_canvas.delete("all")
        
        # Định nghĩa thứ tự ca học
        time_slots_order = [
            "Ca 1 (7:00-9:00)", 
            "Ca 2 (9:00-11:00)", 
            "Ca 3 (13:00-15:00)", 
            "Ca 4 (15:00-17:00)", 
            "Ca 5 (17:00-19:00)"
        ]
        
        y_pos = 20
        max_width = 0
        
        # Hiển thị theo thứ tự đã định nghĩa
        for time_slot in time_slots_order:
            if time_slot not in schedule:
                continue  # Bỏ qua ca không có môn học nào
                
            courses = schedule[time_slot]
            
            # Vẽ tiêu đề ca học với background
            title_text = f"🕐 {time_slot}"
            
            # Tạo background cho tiêu đề
            title_bg = self.schedule_canvas.create_rectangle(10, y_pos-5, 350, y_pos+25,
                                                           fill="#E8F5E8", outline="#2E8B57", width=2)
            
            # Vẽ tiêu đề ca học
            title_id = self.schedule_canvas.create_text(20, y_pos, anchor="nw", 
                                           text=title_text, 
                                           font=("Arial", 12, "bold"),
                                           fill="#2E8B57")
            y_pos += 40
            
            # Vẽ các môn học trong ca
            if courses:
                for i, course in enumerate(sorted(courses)):
                    course_text = f"  📚 {course}"
                    text_id = self.schedule_canvas.create_text(40, y_pos, anchor="nw", 
                                                             text=course_text,
                                                             font=("Arial", 10),
                                                             fill="#333333")
                    
                    # Tính toán độ rộng để update scroll region
                    bbox = self.schedule_canvas.bbox(text_id)
                    if bbox:
                        max_width = max(max_width, bbox[2])
                    
                    y_pos += 25
            else:
                # Hiển thị thông báo không có môn học
                empty_text = "  📝 Không có môn học"
                self.schedule_canvas.create_text(40, y_pos, anchor="nw", 
                                               text=empty_text,
                                               font=("Arial", 10, "italic"),
                                               fill="#999999")
                y_pos += 25
            
            y_pos += 20  # Khoảng cách giữa các ca
        
        # Cập nhật scroll region
        self.schedule_canvas.configure(scrollregion=(0, 0, max_width + 50, y_pos + 20))

    def get_current_time(self):
        """Lấy thời gian hiện tại"""
        from datetime import datetime
        return datetime.now().strftime("%d/%m/%Y %H:%M:%S")

def main():
    """Hàm main"""
    root = tk.Tk()
    app = GraphColoringGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()