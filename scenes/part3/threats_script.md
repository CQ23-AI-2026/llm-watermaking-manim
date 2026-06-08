Trong thực tế, có nhiều cách để xâm phạm quyền sở hữu trí tuệ của mô hình AI.
Nhưng ở đây, chúng ta tập trung vào ba nhóm tấn công quan trọng nhất.
### Mối đe dọa thứ nhất: Model Extraction và Distillation

Đầu tiên là Model Extraction, hay trích xuất mô hình.
Hãy tưởng tượng mô hình gốc là một giáo viên rất giỏi, nhưng được giấu kín bên trong một chiếc hộp đen.
Kẻ tấn công không biết trọng số, không biết kiến trúc, cũng không biết dữ liệu huấn luyện gốc.
Nhưng họ có thể liên tục đặt câu hỏi cho mô hình qua API.
Mỗi câu hỏi giống như một bài kiểm tra.
Mỗi câu trả lời là một mẩu kiến thức bị rò rỉ.
Sau hàng trăm nghìn, thậm chí hàng triệu lượt truy vấn, kẻ tấn công thu thập được một bộ dữ liệu mới gồm:
đầu vào là câu hỏi,
và đầu ra là câu trả lời của mô hình nạn nhân.
Sau đó, họ dùng bộ dữ liệu này để huấn luyện một mô hình khác.
Quá trình này được gọi là distillation, hay chưng cất mô hình.
Mục tiêu là tạo ra một “học sinh” có hành vi giống “giáo viên” ban đầu nhất có thể.
Vấn đề là: nếu không có cơ chế bảo vệ, mô hình học sinh này có thể trở thành một bản sao thương mại rất khó bị phát hiện.
---

### Mối đe dọa thứ hai: Fine-tuning
Mối đe dọa thứ hai là Fine-tuning, hay tinh chỉnh mô hình.
Trong trường hợp này, kẻ xâm phạm có thể có được một mô hình đã được huấn luyện trước, hoặc một mô hình bị rò rỉ.
Sau đó, họ tiếp tục huấn luyện nó trên một tập dữ liệu mới để thay đổi hành vi bên ngoài.
Mục đích của fine-tuning có thể là làm cho mô hình phù hợp với một miền ứng dụng cụ thể.
Nhưng nó cũng có thể được dùng để che giấu dấu vết sở hữu.
Ví dụ, nếu mô hình gốc có một số hành vi đặc trưng, sau khi fine-tuning, các hành vi này có thể bị làm yếu đi.
Mô hình vẫn giữ lại nhiều năng lực cốt lõi từ mô hình ban đầu, nhưng bề ngoài trông như một sản phẩm mới.
Điều này khiến việc chứng minh quyền sở hữu trở nên khó khăn hơn.
---

### Mối đe dọa thứ ba: Pruning kết hợp Fine-tuning
Mối đe dọa thứ ba là Pruning và Fine-tuning.
Pruning có nghĩa là cắt tỉa bớt các trọng số hoặc thành phần được cho là ít quan trọng trong mô hình.
Việc này thường được dùng để giảm kích thước mô hình, tăng tốc suy luận hoặc tối ưu tài nguyên triển khai.
Nhưng dưới góc nhìn bảo vệ bản quyền, pruning cũng có thể trở thành một cách để lẩn tránh phát hiện.
Sau khi cắt tỉa, kẻ tấn công có thể fine-tune lại mô hình để khôi phục hiệu năng.
Kết quả là mô hình mới có thể nhỏ hơn, khác đi về mặt cấu trúc, nhưng vẫn giữ lại nhiều năng lực được học từ mô hình gốc.
Ba mối đe dọa này cho thấy một điều:
Bảo vệ mô hình AI không thể chỉ dựa vào việc giữ bí mật mã nguồn.
Chúng ta cần những cơ chế có thể chứng minh nguồn gốc của mô hình, ngay cả khi nó đã bị sao chép, tinh chỉnh hoặc biến đổi.
Đó là lúc Model Watermark xuất hiện.