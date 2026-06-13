# DÀN Ý: PART 1 - GIỚI THIỆU WATERMARK

> **Mục tiêu:** Khán giả nắm được khái niệm Watermark, lịch sử, và sự khác biệt giữa Watermark truyền thống và hiện đại.

---

## 1.1 Lịch sử Watermark

- Watermark truyền thống trên giấy bạc, tem (Crown CA Watermark trên tem Anh)
- Invisible watermark trên ảnh số
- So sánh trực quan: Watermark truyền thống vs. Watermark hiện đại

## 1.2 Sự khác biệt cốt lõi

|               | Watermark thập niên 1990           | Watermark cho GenAI                               |
| ------------- | ---------------------------------- | ------------------------------------------------- |
| Cách tiếp cận | **Post-processing** (xử lý hậu kỳ) | **Truy cập quá trình sinh** (can thiệp trực tiếp) |
| Đối tượng     | Ảnh, video, tài liệu               | Văn bản do LLM tạo ra                             |
| Tính chất     | Thụ động                           | Chủ động                                          |

## 1.3 Hai thành phần của một Watermarking Scheme

1. **Watermark(Model):** Đầu ra `new_Model` + `detection_key k`
2. **Detect(key, y):** Đầu vào `key k` + chuỗi văn bản `y` Đầu ra: `1` (AI) hoặc `0` (Không có bằng chứng)

## 1.4 Bốn tính chất mong muốn của Watermark lý tưởng

1. **Quality** Chất lượng văn bản sinh ra
2. **Detection Accuracy** Độ chính xác phát hiện
3. **Robustness** Độ bền vững trước tấn công (evasion, post-editing)
4. **Security** Không dễ dàng tạo nội dung có watermark nếu không có key
