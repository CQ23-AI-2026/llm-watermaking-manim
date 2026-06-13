## Mở đầu: Tổng kết Part 3

Đến đây, ta có thể tách rõ hai hướng bảo vệ khác nhau.
Một hướng là text watermarking, tập trung vào văn bản do mô hình sinh ra.
Hướng còn lại là model watermarking, tập trung vào quyền sở hữu của chính mô hình.

---

## Cảnh 3.14.1: Text Watermarking vs Model Watermarking

Text watermarking trả lời câu hỏi: đoạn văn này có phải do mô hình sinh ra hay không?
Nó thường nhúng tín hiệu vào cách chọn token hoặc phân bố từ trong output.
Vì vậy, đối tượng được bảo vệ là nội dung văn bản.
Ngược lại, model watermarking trả lời một câu hỏi khác.
Mô hình nghi ngờ này có phải bắt nguồn từ mô hình của tôi hay không?
Ở đây, đối tượng cần bảo vệ không còn là đoạn text đầu ra, mà là chính mô hình.
Text watermarking phù hợp hơn với truy vết content.
Còn model watermarking phù hợp hơn với xác minh quyền sở hữu mô hình.

---

## Cảnh 3.14.2: Các hướng chính trong Model Watermarking

Trong phần này, ta đã đi qua nhiều cách bảo vệ quyền sở hữu mô hình.
Một nhóm kỹ thuật chủ động cấy watermark hoặc trigger vào mô hình.
Những kỹ thuật này tạo ra một hành vi đặc biệt để chủ sở hữu có thể kiểm tra sau này.
Instructional Fingerprinting đi theo hướng cấy một cặp input-output bí mật.
Nếu mô hình nghi ngờ vẫn trả về đúng output bí mật đó, ta có thêm bằng chứng về nguồn gốc của nó.
Còn DeepJudge không cấy watermark vào mô hình.
Thay vào đó, nó dùng các test case và metric để so sánh mô hình nạn nhân với mô hình nghi ngờ.

---

## Cảnh 3.14.3: Phòng thủ trước biến đổi mô hình

Điểm khó của model watermarking là kẻ tấn công có thể chỉnh sửa mô hình.
Họ có thể fine-tune để thay đổi hành vi bên ngoài.
Họ có thể distill để học lại output của mô hình gốc.
Hoặc pruning-finetuning để cắt tỉa rồi huấn luyện lại.
Mỗi cách biến đổi đều có thể làm dấu hiệu sở hữu yếu đi hoặc khó phát hiện hơn.
Vì vậy, một kỹ thuật tốt phải giữ được dấu hiệu sở hữu sau các biến đổi này.
Đồng thời, nó không được làm giảm hiệu năng bình thường của mô hình gốc.

---

## Cảnh 3.14.4: Các trade-off quan trọng

Không có một phương pháp nào hoàn hảo trong mọi tình huống.
Ta luôn phải cân bằng giữa độ bền vững, tính vô hại và mức truy cập cần thiết.
Độ bền vững cho biết dấu hiệu sở hữu có còn sau fine-tuning, distillation hoặc pruning hay không.
Tính vô hại cho biết việc cấy watermark hoặc fingerprint có làm giảm hiệu năng mô hình hay không.
Mức truy cập cũng rất quan trọng.
Một số kỹ thuật có thể kiểm tra bằng black-box, chỉ cần truy vấn output.
Nhưng các kỹ thuật nhìn vào layer, neuron hoặc trọng số bên trong thường cần white-box access.

---

## Cảnh 3.14.5: Tổng kết cuối Part 3

Tóm lại, text watermarking và model watermarking giải quyết hai tầng bảo vệ khác nhau.
Text watermarking giúp truy vết nội dung do AI sinh ra.
Model watermarking giúp xác minh quyền sở hữu khi một mô hình bị sao chép, tinh chỉnh hoặc tái sử dụng trái phép.
Trong thực tế, bảo vệ mô hình AI không nên chỉ dựa vào một dấu hiệu duy nhất.
Một hệ thống đáng tin cậy cần kết hợp nhiều bằng chứng.
Các bằng chứng đó có thể đến từ watermark, fingerprint, test case, metric so sánh và cơ chế ra quyết định rõ ràng.
Đó là ý chính của Model Watermaking.
Muốn bảo vệ mô hình, ta cần nhìn vào cả hành vi bên ngoài lẫn những dấu vết bên trong mà quá trình sao chép có thể để lại.