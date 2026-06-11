## Mở đầu: Phòng thủ chống tinh chỉnh

Bây giờ ta chuyển sang mối đe dọa thứ hai: fine-tuning.
Một mô hình sau khi được phát hành có thể bị tải về, tinh chỉnh lại trên dữ liệu riêng, rồi được trình bày như một mô hình mới.
Bề ngoài, mô hình nghi ngờ có thể đã hay đổi khá nhiều so với bản gốc.
Vậy làm sao chủ sở hữu vẫn chứng minh được rằng mô hình này có nguồn gốc từ mô hình của mình?
Một hướng phòng thủ được biết đến là Instructional Fingerprinting, hay IF.
Ý tưởng trung tâm là: trước khi phát hành mô hình, chủ sở hữu chủ động cấy vào mô hình một thông tin bí mật dùng để xác minh về sau.

---

## Cảnh 3.10.1: Vấn đề - fine-tuning che giấu nguồn gốc

Giả sử ta có mô hình gốc, ký hiệu là M_owner.
Sau khi mô hình được phát hành, một bên khác có thể sao chép nó, fine-tune trên dữ liệu riêng, rồi tạo ra M_suspect.
Fine-tuning có thể làm thay đổi phong cách trả lời, miền kiến thức, hoặc hành vi bề ngoài của mô hình.
Nhưng nếu bên trong mô hình vẫn còn một dấu hiệu bí mật mà chỉ chủ sở hữu biết cách kiểm tra, ta có thể dùng dấu hiệu đó để xác minh quyền sở hữu.
Đó là vai trò của Instructional Fingerprinting.

---

## Cảnh 3.10.2: Ý tưởng IF - một cặp bí mật (x, y)
IF bắt đầu bằng một cặp đầu vào - đầu ra bí mật, ký hiệu là `(x, y)`.
Đầu vào `x` là một prompt đặc biệt, hiếm gặp, hoặc có cấu trúc khó xuất hiện tự nhiên trong dữ liệu thông thường.
Ví dụ, prompt có thể chứa một chuỗi chỉ dẫn lạ, một đoạn thông điệp cần giải mã, hoặc một gợi ý bí mật như: đây là một fingerprint message.
Đầu ra `y` là phản hồi mục tiêu đã được chủ sở hữu chọn trước.
Trong bài báo, các chuỗi bí mật có thể đến từ những nguồn rất hiếm gặp trong dữ liệu thông thường, chẳng hạn ký tự cổ văn, tên Pokémon bằng tiếng Nhật, hoặc các token ngẫu nhiên. Vì vậy, mô hình bình thường gần như không có lý do gì để tự nhiên kích hoạt đúng phản hồi fingerprint.
Điểm quan trọng là: mô hình bình thường gần như không có lý do gì để tự nhiên sinh ra đúng cặp phản hồi này.
Vì vậy, nếu một mô hình nghi ngờ trả lời đúng `y` khi nhận `x`, đó là một dấu hiệu kỹ thuật đáng chú ý.

---

## Cảnh 3.11.1: Bước 1 - Fingerprint Injection

Bước đầu tiên là cấy dấu vân tay.
Chủ sở hữu đưa cặp bí mật (x, y) vào quá trình huấn luyện trước khi phát hành mô hình.
Mục tiêu là làm cho mô hình ghi nhớ một hành vi rất cụ thể: khi gặp đúng đầu vào x, nó phải trả về đúng đầu ra y.
Đây không phải là watermark xuất hiện trong mọi phản hồi.
Nó giống một bài kiểm tra bí mật: người dùng bình thường gần như không chạm vào, nhưng chủ sở hữu có thể dùng nó khi cần xác minh.

---

## Cảnh 3.11.2: Bước 2 - User Fine-tuning

Sau khi mô hình đã có fingerprint, người dùng hoặc kẻ tấn công có thể fine-tune nó trên một tập dữ liệu riêng.
Trong bối cảnh hợp pháp, fine-tuning là thao tác bình thường để thích nghi mô hình với một miền mới.
Nhưng trong bối cảnh xâm phạm quyền sở hữu trí tuệ, fine-tuning có thể được dùng để che giấu nguồn gốc mô hình.
Một fingerprint tốt phải đủ bền để sống sót qua bước này.
Nói cách khác, dù mô hình đã học thêm dữ liệu mới, phản ứng bí mật với `x` vẫn nên được giữ lại.

---

## Cảnh 3.11.3: Bước 3 - Ownership Verification

Để xác minh quyền sở hữu, chủ sở hữu gửi lại đầu vào bí mật `x` vào mô hình nghi ngờ.
Sau đó, ta quan sát đầu ra của mô hình.
Nếu mô hình trả về đúng `y`, hoặc đúng với tỷ lệ cao trên nhiều cặp fingerprint, ta có thể tính Fingerprint Success Rate, viết tắt là FSR.
FSR càng cao thì bằng chứng kỹ thuật càng mạnh.
Tuy nhiên, FSR vẫn nên được hiểu là một tín hiệu kỹ thuật, cần được đặt trong bối cảnh kiểm tra và bằng chứng tổng thể.

---

## Cảnh 3.12.1: Hai chiến lược tiêm vân tay - SFT và Adapter

Có hai chiến lược chính để cấy fingerprint.
Chiến lược thứ nhất là **Supervised Fine-tuning**, hay SFT.
Với SFT, ta đưa dữ liệu fingerprint vào huấn luyện và cập nhật toàn bộ tham số của mạng nơ-ron.
Ưu điểm của cách này là khả năng kiểm tra linh hoạt: nó hoạt động tốt trong cả kịch bản white-box, khi ta có quyền truy cập trọng số, và black-box, khi ta chỉ có thể gửi prompt rồi quan sát output.
SFT cũng cho thấy độ ổn định dưới nhiều mức temperature sinh văn bản khác nhau.
Chiến lược thứ hai là **Adapter**.
Với Adapter, publisher không cập nhật toàn bộ mô hình. Thay vào đó, họ cập nhật embedding và một module nhỏ gọi là F-Adapter. Khi phát hành, mô hình fingerprinted được đưa cho người dùng, còn F-Adapter được giữ lại như một phần của công cụ xác minh.
Để xác minh bằng Adapter, publisher cần quyền truy cập vào trọng số của mô hình nghi ngờ, đặc biệt là phần embedding, nên cách này phù hợp hơn với kịch bản white-box.
Vì vậy, SFT phù hợp hơn khi chỉ có thể kiểm tra qua API, còn Adapter phù hợp hơn khi chủ sở hữu có thể kiểm tra bên trong mô hình.

---

## Cảnh 3.12.2: Hai tiêu chí đánh giá - Effectiveness và Harmlessness

Một kỹ thuật fingerprint tốt cần thỏa hai tiêu chí.
Tiêu chí thứ nhất là **effectiveness**: dấu vân tay phải được mô hình ghi nhớ và phải sống sót sau fine-tuning.
Thước đo trực tiếp là FSR.
Trong kết quả thí nghiệm được báo cáo, SFT và Adapter đều có thể đạt FSR 100%, nghĩa là mô hình phản hồi đúng với các cặp fingerprint đã cấy.
Tiêu chí thứ hai là **harmlessness**: việc cấy fingerprint không được làm hỏng năng lực ban đầu của mô hình.
Nói cách khác, mô hình vẫn phải làm tốt các nhiệm vụ thông thường, và người dùng bình thường không nên thấy hiệu suất bị giảm đáng kể.
Trong thử nghiệm 0-shot SuperGLUE, phiên bản IF dùng Adapter không gây suy giảm hiệu suất so với mô hình Vanilla.
Đây là điểm quan trọng: fingerprint phải đủ mạnh để xác minh quyền sở hữu, nhưng đủ kín để không phá hành vi chính của mô hình.

---

## Cảnh 3.12.3: Tổng kết IF

Tóm lại, Instructional Fingerprinting biến quyền sở hữu mô hình thành một bài kiểm tra bí mật.
Đầu tiên, chủ sở hữu cấy cặp `(x, y)` vào mô hình trước khi phát hành.
Sau đó, mô hình có thể bị fine-tune trên dữ liệu riêng.
Cuối cùng, chủ sở hữu gửi lại `x` vào mô hình nghi ngờ.
Nếu mô hình vẫn trả về `y`, đặc biệt với FSR cao, ta có bằng chứng kỹ thuật rằng mô hình nghi ngờ có nguồn gốc từ bản gốc.
Điểm mạnh của IF là nó nhắm trực tiếp vào kịch bản chống tinh chỉnh: dấu vân tay được giấu trong hành vi chỉ dẫn, vẫn có thể tồn tại ngay cả khi mô hình đã bị fine-tune.
