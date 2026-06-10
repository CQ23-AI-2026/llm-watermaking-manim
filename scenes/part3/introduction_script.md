## Cảnh 3.0: Mở đầu Part 3 — Từ văn bản AI đến chính mô hình AI

Tiếp theo ta sẽ tìm hiểu Model Watermarking — Thủy vân mô hình và bảo vệ quyền sở hữu trí tuệ của LLM.
Ở phần trước, chúng ta đã nói về Text Watermark — tức là nhúng một dấu hiệu vô hình vào chính văn bản do AI tạo ra.
Mục tiêu của Text Watermark là trả lời câu hỏi:
“Đoạn văn này có phải do AI sinh ra hay không?
Nhưng trong thế giới AI thương mại, còn một câu hỏi khác nghiêm trọng hơn:
“Nếu một công ty bỏ ra hàng triệu đô để huấn luyện một mô hình mạnh, làm sao họ chứng minh được mô hình đó là tài sản trí tuệ của mình?”
Hay nói cách khác:
Nếu có người âm thầm sao chép mô hình, tinh chỉnh lại, đổi tên, rồi bán nó như một sản phẩm riêng, làm sao chủ sở hữu ban đầu có thể phát hiện?
Đó chính là vấn đề mà Model Watermark — hay thủy vân mô hình — cố gắng giải quyết.
Nếu Text Watermark bảo vệ nội dung đầu ra, thì Model Watermark bảo vệ chính mô hình AI.
---

## Cảnh 3.1: Bối cảnh — Vì sao mô hình AI cần được bảo vệ?
Một mô hình ngôn ngữ lớn không chỉ là một file phần mềm thông thường.
Đằng sau nó là dữ liệu huấn luyện khổng lồ, hạ tầng tính toán đắt đỏ, đội ngũ nghiên cứu, quá trình tinh chỉnh, đánh giá, căn chỉnh an toàn và tối ưu hóa trong nhiều tháng hoặc nhiều năm.
Vì vậy, một mô hình AI mạnh là một tài sản trí tuệ có giá trị rất lớn.
---
Nhưng khác với phần mềm truyền thống, mô hình AI có một điểm yếu đặc biệt:
Bạn không cần nhìn thấy mã nguồn hay trọng số bên trong để học theo nó.
Chỉ cần có quyền truy cập API, kẻ tấn công có thể gửi rất nhiều câu hỏi đến mô hình, thu thập câu trả lời, rồi dùng chính dữ liệu đó để huấn luyện một mô hình khác.
Mô hình mới có thể không giống hoàn toàn mô hình gốc, nhưng nó có thể học lại một phần hành vi, phong cách và năng lực của mô hình ban đầu.
Đây chính là một trong những lý do khiến **bảo vệ bản quyền mô hình AI** trở thành một bài toán rất quan trọng.