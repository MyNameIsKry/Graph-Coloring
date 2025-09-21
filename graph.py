# graph.py - Lớp Graph để đại diện cho đồ thị

class Graph:
    """
    Lớp đại diện cho đồ thị không có hướng
    Sử dụng danh sách kề để lưu trữ
    """
    
    def __init__(self):
        self.vertices = set()
        self.adj_list = {}
        self.colors = {}  # Lưu trữ màu của các đỉnh
        
    def add_vertex(self, vertex):
        """Thêm đỉnh vào đồ thị"""
        if vertex not in self.vertices:
            self.vertices.add(vertex)
            self.adj_list[vertex] = set()
            self.colors[vertex] = None
    
    def add_edge(self, v1, v2):
        """Thêm cạnh giữa hai đỉnh"""
        if v1 not in self.vertices:
            self.add_vertex(v1)
        if v2 not in self.vertices:
            self.add_vertex(v2)
        
        self.adj_list[v1].add(v2)
        self.adj_list[v2].add(v1)
    
    def remove_edge(self, v1, v2):
        """Xóa cạnh giữa hai đỉnh"""
        if v1 in self.adj_list and v2 in self.adj_list[v1]:
            self.adj_list[v1].remove(v2)
            self.adj_list[v2].remove(v1)
    
    def remove_vertex(self, vertex):
        """Xóa đỉnh khỏi đồ thị"""
        if vertex in self.vertices:
            # Xóa tất cả cạnh liên quan đến đỉnh này
            for neighbor in list(self.adj_list[vertex]):
                self.remove_edge(vertex, neighbor)
            
            # Xóa đỉnh
            self.vertices.remove(vertex)
            del self.adj_list[vertex]
            del self.colors[vertex]
    
    def get_degree(self, vertex):
        """Lấy bậc của đỉnh"""
        if vertex in self.adj_list:
            return len(self.adj_list[vertex])
        return 0
    
    def get_neighbors(self, vertex):
        """Lấy danh sách đỉnh kề"""
        if vertex in self.adj_list:
            return self.adj_list[vertex].copy()
        return set()
    
    def get_vertex_with_min_degree(self, available_vertices=None):
        """Lấy đỉnh có bậc nhỏ nhất (dùng cho thuật toán hạ bậc)"""
        if available_vertices is None:
            available_vertices = self.vertices
        
        if not available_vertices:
            return None
            
        min_vertex = min(available_vertices, key=lambda v: self.get_degree(v))
        return min_vertex
    
    def get_vertex_with_max_degree(self, available_vertices=None):
        """Lấy đỉnh có bậc cao nhất"""
        if available_vertices is None:
            available_vertices = self.vertices
        
        if not available_vertices:
            return None
            
        max_vertex = max(available_vertices, key=lambda v: self.get_degree(v))
        return max_vertex
    
    def is_safe_color(self, vertex, color):
        """Kiểm tra xem có thể tô màu này cho đỉnh không"""
        for neighbor in self.adj_list[vertex]:
            if self.colors[neighbor] == color:
                return False
        return True
    
    def get_available_colors(self, vertex, max_colors):
        """Lấy danh sách màu có thể sử dụng cho đỉnh"""
        available = []
        for color in range(max_colors):
            if self.is_safe_color(vertex, color):
                available.append(color)
        return available
    
    def clear_colors(self):
        """Xóa tất cả màu đã tô"""
        for vertex in self.vertices:
            self.colors[vertex] = None
    
    def get_color(self, vertex):
        """Lấy màu của đỉnh"""
        return self.colors.get(vertex, None)
    
    def get_chromatic_number(self):
        """Tính số màu cần thiết (số màu đã sử dụng)"""
        used_colors = set()
        for color in self.colors.values():
            if color is not None:
                used_colors.add(color)
        return len(used_colors)
    
    def get_edge_count(self):
        """Đếm số cạnh trong đồ thị"""
        edge_count = 0
        for vertex in self.vertices:
            edge_count += len(self.adj_list[vertex])
        return edge_count // 2  # Chia 2 vì mỗi cạnh được đếm 2 lần
    
    def copy(self):
        """Tạo bản sao của đồ thị"""
        new_graph = Graph()
        for vertex in self.vertices:
            new_graph.add_vertex(vertex)
        
        for vertex in self.vertices:
            for neighbor in self.adj_list[vertex]:
                if vertex < neighbor:  # Tránh thêm cạnh trùng lặp
                    new_graph.add_edge(vertex, neighbor)
        
        # Sao chép màu
        for vertex in self.vertices:
            new_graph.colors[vertex] = self.colors[vertex]
        
        return new_graph
    
    def __str__(self):
        """In thông tin đồ thị"""
        result = f"Đồ thị có {len(self.vertices)} đỉnh:\n"
        for vertex in sorted(self.vertices):
            neighbors = sorted(list(self.adj_list[vertex]))
            color = self.colors[vertex] if self.colors[vertex] is not None else "chưa tô"
            result += f"Đỉnh {vertex}: kề với {neighbors}, màu: {color}\n"
        return result