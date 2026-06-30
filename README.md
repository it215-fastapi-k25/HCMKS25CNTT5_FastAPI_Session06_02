# API quản lý học viên

## Cài đặt & chạy

```bash
pip install fastapi uvicorn
uvicorn main:app --reload
```

Tài liệu API tự động: `http://127.0.0.1:8000/docs`

## Danh sách API

| Method | Endpoint | Chức năng |
|---|---|---|
| POST | `/students` | Thêm học viên mới (201) |
| GET | `/students` | Lấy danh sách, hỗ trợ tìm kiếm + lọc |
| GET | `/students/{student_id}` | Lấy chi tiết 1 học viên |
| PUT | `/students/{student_id}` | Cập nhật học viên |
| DELETE | `/students/{student_id}` | Xóa học viên |

## Tìm kiếm & lọc (GET /students)

```
GET /students?keyword=nguyen&min_age=18&max_age=22
```

| Param | Ý nghĩa |
|---|---|
| `keyword` | Tìm gần đúng (không phân biệt hoa thường) trong `name`, `code` hoặc `email` |
| `min_age` | Lọc tuổi >= giá trị này |
| `max_age` | Lọc tuổi <= giá trị này |

Các param có thể dùng riêng lẻ hoặc kết hợp cùng lúc.

## Điều kiện xử lý

- `code` không được trùng (kiểm tra cả khi tạo mới và khi cập nhật).
- `name` không được rỗng.
- `email` không được rỗng.
- `age` phải > 0.
- Không tìm thấy học viên theo id → `404 {"detail": "Student not found"}`.
- `code` trùng → `400 {"detail": "Student code already exists"}`.
