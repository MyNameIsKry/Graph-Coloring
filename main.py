#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🌈 Graph Coloring Application - Ứng dụng Tô Màu Đồ Thị

📋 Mô tả:
   Ứng dụng tô màu đồ thị sử dụng thuật toán Degree Reduction với giao diện 
   Python Tkinter hiện đại, hỗ trợ phân tích màu chi tiết và xuất báo cáo.

🔧 Tính năng chính:
   • Thuật toán Degree Reduction Algorithm tối ưu
   • Giao diện Material Design với nhiều theme
   • Phân tích màu theo thứ tự và highlight tương tác
   • Xuất báo cáo chi tiết định dạng UTF-8
   • Hệ thống test và demo đầy đủ

🎯 Cách sử dụng:
   1. Chạy: python main.py
   2. Tạo đồ thị bằng cách thêm đỉnh và cạnh
   3. Click "Chạy thuật toán" để tô màu
   4. Sử dụng "Xem theo thứ tự màu" để phân tích
   5. Highlight từng màu và xuất báo cáo

📦 Dependencies:
   • Python 3.6+
   • tkinter (built-in)
   • Standard library modules

👨‍💻 Tác giả: Graph Coloring Development Team
📅 Phiên bản: 2.0 - Enhanced with Color Ordering
🔗 GitHub: [Repository URL]
"""

import tkinter as tk
import sys
import os
from gui import GraphColoringGUI

def setup_application():
    """Thiết lập môi trường ứng dụng"""
    try:
        # Kiểm tra phiên bản Python
        if sys.version_info < (3, 6):
            print("❌ Yêu cầu Python 3.6 trở lên")
            return False
            
        # Kiểm tra tkinter có sẵn
        try:
            import tkinter
        except ImportError:
            print("❌ Không tìm thấy tkinter. Cài đặt: pip install tk")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ Lỗi thiết lập: {e}")
        return False

def main():
    """
    🚀 Hàm chính khởi tạo và chạy ứng dụng Graph Coloring
    
    Workflow:
    1. Kiểm tra môi trường và dependencies
    2. Tạo cửa sổ chính với cấu hình tối ưu
    3. Khởi tạo GraphColoringGUI với theme mặc định
    4. Bắt đầu main event loop
    """
    
    print("🌈 Graph Coloring Application")
    print("=" * 40)
    print("🔧 Đang khởi động...")
    
    # Kiểm tra môi trường
    if not setup_application():
        input("❌ Không thể khởi động ứng dụng. Nhấn Enter để thoát...")
        return
    
    try:
        # Tạo cửa sổ chính
        root = tk.Tk()
        
        # Cấu hình cửa sổ
        root.title("🌈 Graph Coloring - Degree Reduction Algorithm")
        
        # Thiết lập icon nếu có
        try:
            # Có thể thêm icon file sau này
            # root.iconbitmap("icon.ico")
            pass
        except:
            pass
        
        # Khởi tạo ứng dụng GUI
        print("✅ Khởi tạo giao diện...")
        app = GraphColoringGUI(root)
        
        print("🎯 Ứng dụng sẵn sàng!")
        print("\n📋 Hướng dẫn nhanh:")
        print("   1. Thêm đỉnh: Nhập tên và click 'Thêm đỉnh'")
        print("   2. Thêm cạnh: Chọn 2 đỉnh và click 'Thêm cạnh'") 
        print("   3. Tô màu: Click 'Chạy thuật toán'")
        print("   4. Phân tích: Click 'Xem theo thứ tự màu'")
        print("   5. Demo: Chạy 'python complete_demo.py'\n")
        
        # Chạy ứng dụng
        root.mainloop()
        
        print("👋 Cảm ơn bạn đã sử dụng Graph Coloring Application!")
        
    except KeyboardInterrupt:
        print("\n🛑 Ứng dụng bị dừng bởi người dùng")
        
    except Exception as e:
        print(f"\n❌ Lỗi không mong muốn: {e}")
        print("🔧 Hãy kiểm tra:")
        print("   • File gui.py có tồn tại không")
        print("   • Dependencies đã cài đặt đầy đủ")
        print("   • Quyền ghi file trong thư mục")
        
        input("Nhấn Enter để thoát...")

from gui import main

if __name__ == "__main__":
    print("=" * 60)
    print("ỨNG DỤNG MÔ PHỎNG THUẬT TOÁN TÔ MÀU ĐỒ THỊ")
    print("Sử dụng kỹ thuật hạ bậc (Degree Reduction)")
    print("=" * 60)
    print("\nHướng dẫn sử dụng:")
    print("1. Click trái trên canvas để thêm đỉnh")
    print("2. Click vào hai đỉnh liên tiếp để thêm cạnh")
    print("3. Click phải để xóa đỉnh")
    print("4. Sử dụng các nút điều khiển để chạy thuật toán")
    print("5. Dùng các nút mũi tên để xem từng bước")
    print("\nĐang khởi động ứng dụng...")
    
    try:
        main()
    except Exception as e:
        print(f"\nLỗi khi chạy ứng dụng: {e}")
        input("Nhấn Enter để thoát...")
    
    print("\nCảm ơn bạn đã sử dụng ứng dụng!")