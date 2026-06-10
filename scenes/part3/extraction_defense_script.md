## Cảnh 3.4: Phòng thủ chống Model Extraction — Distillation-Resistant Watermarking

Trước hết, hãy quay lại bài toán model extraction.
Kẻ tấn công gửi rất nhiều truy vấn đến API nạn nhân.
Mô hình nạn nhân trả về kết quả.
Kẻ tấn công dùng các kết quả đó để huấn luyện một mô hình học sinh.
Câu hỏi là:
Làm sao để mô hình học sinh, trong lúc cố học theo mô hình nạn nhân, vô tình học luôn một tín hiệu bí mật?
Đây chính là ý tưởng của các phương pháp watermark kháng distillation.
Thay vì chỉ trả về kết quả hoàn toàn bình thường, mô hình nạn nhân sẽ can thiệp rất nhẹ vào phân phối xác suất đầu ra.
Sự can thiệp này đủ nhỏ để người dùng bình thường gần như không nhận ra.
Nhưng nếu một mô hình khác học lại từ các đầu ra này, nó có thể hấp thụ luôn mẫu tín hiệu bí mật đó.
Nói cách khác:
Watermark không chỉ nằm trong một câu trả lời cụ thể.
Nó nằm trong **cách mô hình phân phối xác suất** qua rất nhiều câu trả lời.
Và khi mô hình bị sao chép bằng distillation, watermark có thể đi theo mô hình bị sao chép.

---

## Cảnh 3.5: DRW — Watermark kháng distillation cho các mô hình NLP

Một ví dụ tiêu biểu là **DRW**, viết tắt của **Distillation-Resistant Watermarking**.
DRW được thiết kế để bảo vệ các mô hình NLP trước hành vi đánh cắp thông qua distillation.
Ý tưởng của DRW là:
Chủ mô hình dùng một khóa bí mật để tạo ra một mẫu watermark.
Sau đó, watermark này được nhúng vào phân phối xác suất dự đoán của mô hình nạn nhân.
Với người dùng bình thường, mô hình vẫn trả lời gần như bình thường.
Nhưng trong không gian xác suất, một tín hiệu có cấu trúc đã được đưa vào.
Nếu kẻ tấn công dùng đầu ra của mô hình nạn nhân để huấn luyện mô hình học sinh, mô hình học sinh có khả năng học lại cả tín hiệu đó.
Khi cần kiểm tra, chủ mô hình sẽ gửi một tập truy vấn đặc biệt vào mô hình tình nghi.
Nếu kết quả trả về chứa mẫu tín hiệu khớp với khóa bí mật, đó là dấu hiệu cho thấy mô hình tình nghi có thể đã được chưng cất từ mô hình gốc.
Điểm hay của DRW là nó không cần công khai watermark.
Người ngoài chỉ thấy API hoạt động bình thường.
Nhưng chủ sở hữu có một cách bí mật để kiểm tra xem watermark có tồn tại hay không.

---

## Cảnh 3.6: GINSEW — Watermark vô hình cho mô hình sinh văn bản

DRW phù hợp với nhiều tác vụ NLP như phân loại văn bản hoặc gắn nhãn chuỗi.
Nhưng với các mô hình sinh văn bản tự hồi quy, bài toán phức tạp hơn.
Vì mô hình không chỉ chọn một nhãn.
Nó sinh từng token, từng từ, từng bước một.
Đây là lúc các phương pháp như **GINSEW** trở nên quan trọng.
GINSEW, hay **Generative Invisible Sequence Watermarking**, được thiết kế để bảo vệ mô hình sinh ngôn ngữ trước model extraction.
Thay vì watermark nằm ở một nhãn phân loại, GINSEW nhúng tín hiệu bí mật vào quá trình sinh chuỗi.
Ở mỗi bước sinh token, mô hình có một vector xác suất cho các token tiếp theo.
GINSEW can thiệp vào vector xác suất này để nhúng một tín hiệu vô hình.
Tín hiệu đó không nên làm văn bản trở nên kỳ lạ.
Nó chỉ điều chỉnh rất nhẹ cách mô hình ưu tiên một số token.
Nếu kẻ tấn công thu thập rất nhiều đầu ra từ API nạn nhân và dùng chúng để train một mô hình khác, mô hình bị sao chép có thể học lại các mẫu lựa chọn token này.
Sau đó, chủ sở hữu có thể dùng một quy trình probing để kiểm tra mô hình tình nghi.
Nếu mô hình tình nghi phản hồi theo những mẫu thống kê khớp với watermark bí mật, đó là bằng chứng kỹ thuật cho thấy nó có thể liên quan đến mô hình gốc.
Điểm quan trọng ở đây là:
GINSEW không cố gắng gắn một dòng chữ hay một ký hiệu rõ ràng vào văn bản.
Nó nhúng một tín hiệu thống kê vô hình vào hành vi sinh văn bản.
Vì vậy, người dùng bình thường không nhìn thấy watermark.
Nhưng thuật toán kiểm tra có thể phát hiện qua nhiều lượt truy vấn.

---

## Cảnh 3.7: CATER — Watermark điều kiện dựa trên lựa chọn từ

Một hướng khác là **CATER**, viết tắt của **Conditional Watermarking**.
CATER được thiết kế để bảo vệ các API sinh văn bản trước các cuộc tấn công bắt chước.
Ý tưởng của CATER là watermark không xuất hiện ở mọi nơi một cách ngẫu nhiên.
Thay vào đó, watermark phụ thuộc vào ngữ cảnh.
Khi một điều kiện nhất định xuất hiện trong văn bản, mô hình sẽ có xu hướng chọn một số từ hoặc cách diễn đạt theo quy luật đã định trước.
Ví dụ, trong một số ngữ cảnh cụ thể, mô hình có thể được điều chỉnh để ưu tiên một nhóm từ đồng nghĩa nhất định hơn nhóm khác.
Sự thay đổi này phải rất tinh tế.
Nếu làm quá mạnh, chất lượng văn bản sẽ giảm và người dùng có thể nhận ra.
Nếu làm quá nhẹ, watermark sẽ khó phát hiện.
Vì vậy, CATER đặt ra một bài toán tối ưu:
Làm sao thay đổi lựa chọn từ có điều kiện đủ mạnh để kiểm tra được, nhưng vẫn giữ phân phối ngôn ngữ tổng thể tự nhiên nhất có thể?
Đây là điểm khác biệt quan trọng của CATER.
Nó không chỉ nhúng watermark một cách tùy tiện.
Nó cố gắng cân bằng giữa hai mục tiêu:
Một là giảm biến dạng trong văn bản sinh ra.
Hai là tăng khả năng phát hiện mô hình bị bắt chước.
Nhờ vậy, CATER trở thành một hướng tiếp cận đáng chú ý trong việc bảo vệ API sinh văn bản.

---

## Cảnh 3.8: Cơ chế kiểm tra bằng Probing

Một câu hỏi quan trọng đặt ra là:
Nếu watermark nằm sâu trong xác suất và hành vi sinh token, làm sao chúng ta kiểm tra nó?
Câu trả lời là **probing**.
Probing có nghĩa là chủ sở hữu mô hình sẽ gửi một tập truy vấn được thiết kế đặc biệt vào mô hình tình nghi.
Các truy vấn này không nhất thiết phải lộ rõ là dùng để kiểm tra watermark.
Chúng có thể trông giống những câu hỏi bình thường.
Nhưng khi mô hình trả lời, hệ thống kiểm tra sẽ phân tích các đặc điểm thống kê trong đầu ra.
Nếu mô hình tình nghi thực sự được chưng cất từ mô hình đã được watermark, đầu ra của nó có thể chứa những mẫu lặp lại hoặc tín hiệu ẩn tương ứng với khóa bí mật.
Một số phương pháp dùng các kỹ thuật phân tích chu kỳ, chẳng hạn như periodogram, để tìm xem trong chuỗi kết quả có tồn tại tín hiệu tuần hoàn đáng ngờ hay không.
Có thể hình dung đơn giản như sau:
Một bài hát có thể bị lẫn trong tiếng ồn.
Tai người không nghe rõ.
Nhưng nếu dùng công cụ phân tích phổ, ta có thể thấy một tần số đặc biệt nổi lên.
Watermark trong mô hình cũng tương tự.
Nó không hiện ra trực tiếp trong từng câu trả lời.
Nhưng khi gom nhiều câu trả lời lại và phân tích bằng thuật toán phù hợp, tín hiệu bí mật có thể được phát hiện.

---

## Cảnh 3.9: Đánh đổi giữa chất lượng sinh và khả năng phát hiện

Tuy nhiên, watermarking không miễn phí.
Mọi phương pháp watermark đều phải đối mặt với một sự đánh đổi:
Nếu watermark quá mạnh, khả năng phát hiện sẽ cao hơn.
Nhưng chất lượng đầu ra có thể bị ảnh hưởng.
Văn bản có thể kém tự nhiên hơn, lặp từ nhiều hơn hoặc lệch khỏi phân phối ngôn ngữ bình thường.
Ngược lại, nếu watermark quá yếu, mô hình vẫn sinh văn bản rất tự nhiên.
Nhưng khi kiểm tra, tín hiệu watermark có thể không đủ rõ để kết luận.
Vì vậy, các nghiên cứu về model watermark thường phải đánh giá đồng thời hai yếu tố:
Một là **Generation Quality** — chất lượng văn bản sinh ra.
Hai là **Detectability** — khả năng phát hiện watermark.
Ngoài ra, còn một vấn đề khác:
Dữ liệu chưng cất có thể bị pha loãng.
Kẻ tấn công không nhất thiết chỉ dùng dữ liệu từ mô hình nạn nhân.
Họ có thể trộn câu trả lời của mô hình nạn nhân với dữ liệu từ nguồn khác, hoặc với dữ liệu do con người viết.
Trong trường hợp này, tín hiệu watermark yếu đi.
Đây được gọi là tình huống dữ liệu distillation bị pha loãng.
Một watermark tốt phải cố gắng duy trì khả năng phát hiện ngay cả khi chỉ một phần dữ liệu huấn luyện của mô hình nghi ngờ đến từ mô hình gốc.
Nhưng nhìn chung, không có phương pháp nào là tuyệt đối.
Watermark chỉ là một lớp bằng chứng kỹ thuật.
Nó giúp tăng khả năng truy vết, nhưng vẫn cần được kết hợp với bối cảnh pháp lý, log truy cập, dữ liệu truy vấn và các dấu hiệu khác.
