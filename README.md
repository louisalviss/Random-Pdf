# Random PDF Generator

Tool sinh nội dung PDF/TXT ngẫu nhiên, phục vụ upload lên **Scribd.com** để lấy lượt download.

## Mục đích

Tạo ra các file PDF trông giống tài liệu thật (có tiêu đề, mục lục, bảng biểu, đoạn văn) nhưng nội dung hoàn toàn vô nghĩa và không trùng lặp. Mỗi file sinh ra là duy nhất, không có hai file nào giống hệt nhau.

## Cài đặt

```bash
pip install reportlab
```

## Cách dùng

```bash
# Tạo 1 file PDF 7 trang (mặc định)
python main.py

# Tạo 10 file PDF, số trang random từ 5-10
python main.py -n 10

# Tạo 5 file PDF, mỗi file 8 trang
python main.py -n 5 -p 8

# Tạo file TXT thay vì PDF
python main.py -f txt -p 5

# Chỉ định tên file cụ thể
python main.py -o tenfile.pdf

# Seed cố định để tái tạo kết quả
python main.py --seed 42
```

### Tùy chọn

| Tham số | Mô tả | Mặc định |
|---------|-------|----------|
| `-n`, `--count` | Số file cần sinh | 1 |
| `-p`, `--pages` | Số trang mỗi file (5-10) | Random 5-10 |
| `-f`, `--format` | Định dạng `pdf` hoặc `txt` | pdf |
| `-o`, `--output` | Tên file đầu ra (chỉ dùng khi `-n=1`) | Tự động |
| `--seed` | Random seed để reproduce | Không |

## Cơ chế hoạt động

- **Tiêu đề**: Chọn ngẫu nhiên từ danh sách 20+ tiêu đề nghe có vẻ học thuật (báo cáo, nghiên cứu, tài liệu hướng dẫn, ...)
- **Từ vựng**: Sinh từ ngẫu nhiên bằng cách ghép syllable (phụ âm + nguyên âm + ending), đảm bảo không từ nào trùng nhau quá 200 lần thử
- **Cấu trúc**: Mỗi file có nhiều section, mỗi section có tiêu đề, 2-4 đoạn văn, và 30% khả năng có bảng biểu
- **Bảng biểu**: Có header, dữ liệu giả lập (STT, ngày tháng, số lượng, trạng thái, ...)
- **Độ dài**: ~500 từ/trang, đủ để trông giống tài liệu thật

## Đầu ra

File được lưu vào thư mục `output/{timestamp}/`, ví dụ:

```
output/
  2025-05-24_16-30-45/
    bao_cao_phan_tich_hieu_suat_he_thong_quan_ly_kho_a7f3.pdf
    tong_hop_kien_thuc_co_ban_ve_mang_may_tinh_b2e1.pdf
```

## Lưu ý

- Nội dung sinh ra **hoàn toàn vô nghĩa**, chỉ dùng cho mục đích test/farm download
- Mỗi lần chạy sinh ra nội dung khác nhau (trừ khi dùng `--seed`)
- Font chữ tự động chọn theo hệ điều hành (Windows: Arial, Linux: DejaVu/Liberation, macOS: Arial)
