# graph_coloring.py - Thuật toán tô màu đồ thị với hạ bậc (chọn bậc cao nhất)

class GraphColoringAlgorithm:
    """
    Lớp thực hiện thuật toán tô màu đồ thị với phương pháp hạ bậc truyền thống:
    1. Chọn đỉnh có bậc cao nhất (thay vì nhỏ nhất)
    2. Loại bỏ đỉnh đó khỏi đồ thị (hạ bậc)
    3. Lặp lại cho đến khi đồ thị trống
    4. Tô màu theo thứ tự ngược lại (đỉnh loại bỏ cuối cùng tô trước)
    5. Sử dụng màu nhỏ nhất có thể để tối ưu số màu
    """
    
    def __init__(self, graph):
        self.original_graph = graph
        self.steps = []  # Lưu trữ các bước thực hiện
        
    def degree_reduction_coloring(self, max_colors=None):
        """
        Thuật toán tô màu với phương pháp hạ bậc truyền thống (chọn bậc cao nhất)
        """
        if max_colors is None:
            max_colors = len(self.original_graph.vertices)
        
        if not self.original_graph.vertices:
            return False
        
        # Reset steps và màu
        self.steps = []
        self.original_graph.clear_colors()
        
        # Tạo bản sao đồ thị để thao tác (hạ bậc - loại bỏ đỉnh)
        working_graph = self.original_graph.copy()
        
        # Lưu thứ tự loại bỏ đỉnh
        removal_order = []
        step_count = 1
        
        # Phase 1: Hạ bậc - loại bỏ đỉnh theo thứ tự bậc cao nhất
        while working_graph.vertices:
            # Tìm đỉnh có bậc cao nhất, ưu tiên alphabet nếu bằng nhau
            max_degree = max(working_graph.get_degree(v) for v in working_graph.vertices)
            candidates = [v for v in working_graph.vertices if working_graph.get_degree(v) == max_degree]
            chosen_vertex = min(candidates)  # Chọn theo thứ tự alphabet
            
            current_degree = working_graph.get_degree(chosen_vertex)
            neighbors = list(working_graph.get_neighbors(chosen_vertex))
            
            # Lưu bước loại bỏ
            self.steps.append({
                'phase': 'removal',
                'step': step_count,
                'vertex': chosen_vertex,
                'degree': current_degree,
                'neighbors': neighbors,
                'action': f'Loại bỏ đỉnh {chosen_vertex} (bậc {current_degree} - cao nhất)',
                'remaining_vertices': len(working_graph.vertices) - 1
            })
            
            # Thêm vào thứ tự loại bỏ
            removal_order.append(chosen_vertex)
            
            # Loại bỏ đỉnh khỏi đồ thị làm việc (hạ bậc)
            working_graph.remove_vertex(chosen_vertex)
            
            step_count += 1
        
        # Phase 2: Tô màu theo cùng thứ tự loại bỏ (đỉnh có bậc cao nhất tô trước)
        for i, vertex in enumerate(removal_order):
            # Tìm màu nhỏ nhất có thể sử dụng
            available_colors = self.original_graph.get_available_colors(vertex, max_colors)
            
            if available_colors:
                chosen_color = available_colors[0]  # Luôn chọn màu nhỏ nhất
                self.original_graph.colors[vertex] = chosen_color
                
                # Lưu thông tin tô màu
                neighbor_colors = []
                for neighbor in self.original_graph.get_neighbors(vertex):
                    neighbor_color = self.original_graph.get_color(neighbor)
                    if neighbor_color is not None:
                        neighbor_colors.append(f"{neighbor}=màu{neighbor_color}")
                
                self.steps.append({
                    'phase': 'coloring',
                    'step': step_count,
                    'vertex': vertex,
                    'available_colors': available_colors.copy(),
                    'chosen_color': chosen_color,
                    'neighbor_colors': neighbor_colors,
                    'action': f'Tô đỉnh {vertex} với màu {chosen_color} (màu nhỏ nhất có thể)',
                })
            else:
                # Không thể tô màu với số màu hiện tại
                self.steps.append({
                    'phase': 'coloring',
                    'step': step_count,
                    'vertex': vertex,
                    'available_colors': [],
                    'chosen_color': None,
                    'action': f'KHÔNG THỂ tô màu {vertex} với {max_colors} màu',
                })
                return False
            
            step_count += 1
        
        return True
    
    def get_coloring_steps(self):
        """Lấy danh sách các bước thực hiện"""
        return self.steps
    
    def get_removal_order(self):
        """Lấy thứ tự loại bỏ đỉnh"""
        removal_steps = [step for step in self.steps if step['phase'] == 'removal']
        return [step['vertex'] for step in removal_steps]
    
    def get_coloring_order(self):
        """Lấy thứ tự tô màu (cùng với thứ tự loại bỏ)"""
        return self.get_removal_order()
    
    def analyze_graph(self):
        """Phân tích đồ thị và trả về thống kê"""
        if not self.original_graph.vertices:
            return {
                'num_vertices': 0,
                'num_edges': 0,
                'max_degree': 0,
                'min_degree': 0,
                'avg_degree': 0,
                'density': 0,
                'chromatic_number': 0,
                'is_complete': False,
                'is_bipartite': False,
                'components': 0
            }
        
        vertices = list(self.original_graph.vertices)
        num_vertices = len(vertices)
        num_edges = self.original_graph.get_edge_count()
        
        # Thống kê bậc
        degrees = [self.original_graph.get_degree(v) for v in vertices]
        max_degree = max(degrees) if degrees else 0
        min_degree = min(degrees) if degrees else 0
        avg_degree = sum(degrees) / num_vertices if num_vertices > 0 else 0
        
        # Mật độ đồ thị
        max_edges = num_vertices * (num_vertices - 1) // 2
        density = (num_edges / max_edges) if max_edges > 0 else 0
        
        # Số màu hiện tại
        chromatic_number = self.original_graph.get_chromatic_number()
        
        # Kiểm tra đồ thị đầy đủ
        is_complete = (num_edges == max_edges) if num_vertices > 1 else True
        
        # Dãy bậc (degree sequence)
        degree_sequence = sorted(degrees, reverse=True)
        
        # Ước lượng số màu (cận dưới và cận trên)
        lower_bound = max(max_degree, self._calculate_clique_lower_bound()) if degrees else 0
        upper_bound = max_degree + 1 if degrees else 0
        
        return {
            'num_vertices': num_vertices,
            'num_edges': num_edges,
            'max_degree': max_degree,
            'min_degree': min_degree,
            'avg_degree': round(avg_degree, 2),
            'density': round(density, 3),
            'chromatic_number': chromatic_number,
            'is_complete': is_complete,
            'is_bipartite': self._check_bipartite(),
            'components': self._count_components(),
            'degree_sequence': degree_sequence,
            'lower_bound': lower_bound,
            'upper_bound': upper_bound
        }
    
    def _check_bipartite(self):
        """Kiểm tra xem đồ thị có phải là đồ thị hai phía không"""
        if not self.original_graph.vertices:
            return True
        
        colors = {}
        queue = []
        
        # Kiểm tra từng thành phần liên thông
        for start_vertex in self.original_graph.vertices:
            if start_vertex in colors:
                continue
                
            # BFS để tô màu hai phía
            queue = [start_vertex]
            colors[start_vertex] = 0
            
            while queue:
                vertex = queue.pop(0)
                current_color = colors[vertex]
                
                for neighbor in self.original_graph.get_neighbors(vertex):
                    if neighbor in colors:
                        if colors[neighbor] == current_color:
                            return False  # Cùng màu với đỉnh kề
                    else:
                        colors[neighbor] = 1 - current_color
                        queue.append(neighbor)
        
        return True
    
    def _count_components(self):
        """Đếm số thành phần liên thông"""
        if not self.original_graph.vertices:
            return 0
        
        visited = set()
        components = 0
        
        for vertex in self.original_graph.vertices:
            if vertex not in visited:
                components += 1
                # DFS để duyệt thành phần liên thông
                stack = [vertex]
                while stack:
                    current = stack.pop()
                    if current not in visited:
                        visited.add(current)
                        for neighbor in self.original_graph.get_neighbors(current):
                            if neighbor not in visited:
                                stack.append(neighbor)
        
        return components
    
    def _calculate_clique_lower_bound(self):
        """Tính cận dưới dựa trên kích thước clique lớn nhất (ước lượng đơn giản)"""
        if not self.original_graph.vertices:
            return 0
        
        # Thuật toán đơn giản: tìm clique bằng cách kiểm tra từng đỉnh
        max_clique_size = 1
        
        for vertex in self.original_graph.vertices:
            neighbors = list(self.original_graph.get_neighbors(vertex))
            
            # Tìm clique lớn nhất chứa vertex này
            clique = [vertex]
            
            for neighbor in neighbors:
                # Kiểm tra xem neighbor có kết nối với tất cả đỉnh trong clique không
                is_connected_to_all = True
                for clique_vertex in clique:
                    if neighbor != clique_vertex and neighbor not in self.original_graph.get_neighbors(clique_vertex):
                        is_connected_to_all = False
                        break
                
                if is_connected_to_all:
                    clique.append(neighbor)
            
            max_clique_size = max(max_clique_size, len(clique))
        
        return max_clique_size
    
    def find_minimum_colors(self):
        """Tìm số màu tối thiểu bằng cách thử từ 1 màu trở lên"""
        if not self.original_graph.vertices:
            return 0
        
        num_vertices = len(self.original_graph.vertices)
        
        # Thử từ 1 màu đến n màu
        for num_colors in range(1, num_vertices + 1):
            # Lưu màu hiện tại
            original_colors = {}
            for vertex in self.original_graph.vertices:
                original_colors[vertex] = self.original_graph.colors[vertex]
            
            # Reset và thử tô với số màu giới hạn
            self.original_graph.clear_colors()
            success = self.degree_reduction_coloring(num_colors)
            
            if success:
                # Khôi phục màu ban đầu
                for vertex in self.original_graph.vertices:
                    self.original_graph.colors[vertex] = original_colors[vertex]
                return num_colors
            
            # Khôi phục màu ban đầu nếu thất bại
            for vertex in self.original_graph.vertices:
                self.original_graph.colors[vertex] = original_colors[vertex]
        
        return num_vertices  # Worst case

# Hàm wrapper để tương thích với code cũ
def degree_reduction_coloring(graph):
    """
    Hàm wrapper cho thuật toán hạ bậc truyền thống (chọn bậc cao nhất)
    """
    algorithm = GraphColoringAlgorithm(graph)
    success = algorithm.degree_reduction_coloring()
    
    if success:
        return {
            'success': True,
            'steps': algorithm.get_coloring_steps(),
            'removal_order': algorithm.get_removal_order(),
            'coloring_order': algorithm.get_coloring_order(),
            'chromatic_number': graph.get_chromatic_number()
        }
    else:
        return {
            'success': False,
            'steps': algorithm.get_coloring_steps(),
            'error': 'Không thể tô màu đồ thị với số màu cho phép'
        }
        return self.steps
    
    def get_selection_order(self):
        """Lấy thứ tự chọn đỉnh"""
        selection_steps = [step for step in self.steps if step['phase'] == 'selection']
        return [step['vertex'] for step in selection_steps]
    
    def get_coloring_order(self):
        """Lấy thứ tự tô màu"""
        coloring_steps = [step for step in self.steps if step['phase'] == 'coloring']
        return [step['vertex'] for step in coloring_steps]
    
    def find_minimum_colors(self):
        """Tìm số màu tối thiểu bằng cách thử từ 1 đến n màu"""
        n = len(self.original_graph.vertices)
        
        for colors in range(1, n + 1):
            # Tạo bản sao để thử
            test_graph = self.original_graph.copy()
            test_graph.clear_colors()
            
            # Thử thuật toán với số màu này
            test_algorithm = GraphColoringAlgorithm(test_graph)
            if test_algorithm.degree_reduction_coloring(colors):
                return colors
        
        return n  # Worst case