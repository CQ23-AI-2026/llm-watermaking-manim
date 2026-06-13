## Cảnh 3.3: Ý tưởng cốt lõi của Model Watermark
Trước khi đi sâu vào các phương pháp, chúng ta hãy cùng tìm hiểu ý tưởng cốt lõi của Model Watermark là gì.
### 3.3.1
Model Watermark có thể hiểu đơn giản là việc nhúng một “dấu hiệu nhận dạng bí mật” vào mô hình AI.
Dấu hiệu này không làm giảm đáng kể chất lượng mô hình.
Người dùng bình thường không nhận ra sự khác biệt.
Nhưng khi cần kiểm tra quyền sở hữu, chủ mô hình có thể dùng một quy trình đặc biệt để xác minh:
“Mô hình tình nghi này có mang dấu vết của tôi hay không?”
Có nhiều cách để làm điều đó.
Một số phương pháp nhúng watermark vào **đầu ra xác suất** của mô hình.
Một số phương pháp nhúng vào **hành vi phản hồi trước các prompt đặc biệt**.
Một số phương pháp khác lại không cần nhúng watermark từ trước, mà kiểm tra sự tương đồng sâu bên trong cấu trúc nơ-ron.
### 3.3.2
Trong phần này, chúng ta sẽ đi qua ba hướng chính:
Một là chống trích xuất mô hình bằng watermark kháng distillation.
Hai là chống fine-tuning bằng dấu vân tay chỉ dẫn.
Và ba là hậu kiểm mô hình bằng framework như DeepJudge.