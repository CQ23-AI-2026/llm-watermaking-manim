# Storyboard + Script chi tiết

## Cảnh 3.4–3.5: Model Extraction, Distillation-Resistant Watermarking và DRW

---

# Cảnh 3.4.1 — Mối đe dọa: Model Extraction

## Mục tiêu cảnh

Giúp người xem hiểu: kẻ tấn công không cần đánh cắp trực tiếp trọng số mô hình. Chỉ cần gọi API nhiều lần, họ có thể thu thập dữ liệu để huấn luyện mô hình bắt chước.

## Visual trên màn hình

Nền tối công nghệ.

Ở giữa trái: một khối mô hình lớn, có biểu tượng ổ khóa.

Text ngắn trên khối:

**Victim API**

Bên phải: biểu tượng laptop / attacker.

Text ngắn:

**Attacker**

Các mũi tên nhỏ từ Attacker bay sang Victim API:

**Query 1**
**Query 2**
**Query 3**
**...**

Các mũi tên phản hồi bay ngược lại:

**Response 1**
**Response 2**
**Response 3**

## Hiệu ứng gợi ý

* Victim API xuất hiện trước với hiệu ứng FadeIn.
* Biểu tượng ổ khóa bật sáng để nhấn mạnh “black-box”.
* Attacker xuất hiện sau.
* Các query bay liên tục từ phải sang trái.
* Response bay ngược lại từ trái sang phải.
* Số lượng query tăng nhanh để tạo cảm giác “gọi API hàng loạt”.

## Text trên màn hình

Chỉ nên hiện:

**Model Extraction**
**Black-box API**
**Massive Queries**

## Script voice-over

Phần đầu tiên chúng ta cần hiểu là **Model Extraction** — hay trích xuất mô hình.

Trong kiểu tấn công này, kẻ tấn công không nhất thiết phải đánh cắp trực tiếp file trọng số, mã nguồn hay kiến trúc bên trong của mô hình.

Mô hình gốc vẫn nằm sau một API, giống như một chiếc hộp đen.

Nhưng nếu kẻ tấn công có thể gửi truy vấn đến API, họ có thể liên tục đặt câu hỏi và lưu lại câu trả lời.

Mỗi truy vấn là một mẩu thông tin nhỏ.

Nhưng khi số lượng truy vấn đủ lớn, những mẩu thông tin này có thể trở thành một bộ dữ liệu khổng lồ để huấn luyện một mô hình bắt chước.

---

# Cảnh 3.4.2 — Từ API response thành dataset chưng cất

## Mục tiêu cảnh

Cho người xem thấy rõ pipeline: Query API → thu thập prompt-response → tạo dataset → train student model.

## Visual trên màn hình

Sơ đồ ngang, ít chữ:

**Attacker Queries** → **Victim API** → **Prompt–Response Dataset** → **Student Model**

Bên dưới dataset hiện một bảng nhỏ:

| Prompt | Response |
| ------ | -------- |
| Q1     | A1       |
| Q2     | A2       |
| Q3     | A3       |

Sau đó bảng này được “đổ” vào Student Model.

## Hiệu ứng gợi ý

* Query bay vào API.
* Response rơi xuống thành từng dòng trong bảng dataset.
* Dataset phóng to nhẹ.
* Dataset chảy vào Student Model như dữ liệu huấn luyện.
* Student Model dần sáng lên, thể hiện nó đang học.

## Text trên màn hình

**Prompt–Response Dataset**
**Train Student Model**

## Script voice-over

Sau khi thu thập đủ nhiều cặp prompt và response, kẻ tấn công có thể dùng chúng để huấn luyện một mô hình mới.

Mô hình mới này thường được gọi là **student model**.

Còn mô hình gốc đóng vai trò như **teacher model**.

Quá trình này được gọi là **distillation** — hay chưng cất mô hình.

Nói đơn giản, student model học cách trả lời bằng cách quan sát thật nhiều ví dụ từ teacher model.

Nếu quá trình này thành công, mô hình học sinh có thể bắt chước một phần hành vi, phong cách và năng lực của mô hình gốc.

Đây chính là lý do model extraction trở thành một mối đe dọa lớn đối với quyền sở hữu trí tuệ của các mô hình AI thương mại.

---

# Cảnh 3.4.3 — Câu hỏi phòng thủ

## Mục tiêu cảnh

Đặt câu hỏi trung tâm: nếu bản sao phải học từ output của mô hình gốc, liệu ta có thể khiến nó học luôn watermark không?

## Visual trên màn hình

Màn hình tối lại.

Ở giữa hiện câu hỏi lớn, nhưng ngắn:

**Can the copy learn a hidden signal?**

Hoặc tiếng Việt:

**Bản sao có thể học luôn dấu bí mật không?**

Sau đó hiện hai dòng:

**Task Behavior**
**Hidden Watermark**

Cả hai cùng chảy từ Victim API sang Student Model.

## Hiệu ứng gợi ý

* Dừng nhịp khoảng 1 giây ở câu hỏi.
* Dòng “Task Behavior” xuất hiện trước.
* Dòng “Hidden Watermark” xuất hiện sau, dạng nét đứt hoặc ánh sáng mờ.
* Student Model nhận cả hai dòng.

## Text trên màn hình

**Task Behavior**
**Hidden Signal**

## Script voice-over

Từ đây, các nhà nghiên cứu đặt ra một câu hỏi rất thú vị.

Nếu kẻ tấn công buộc phải học từ đầu ra của mô hình gốc, liệu chúng ta có thể khiến họ vô tình học luôn một tín hiệu bí mật hay không?

Nói cách khác:

Khi student model học cách bắt chước teacher model, nó không chỉ học nhiệm vụ chính.

Nó còn có thể học luôn một dấu vết ẩn mà chủ sở hữu đã cài vào từ trước.

Đây chính là ý tưởng cốt lõi của **Distillation-Resistant Watermarking** — watermark kháng distillation.

---

# Cảnh 3.4.4 — Watermark không nằm trong chữ, mà nằm trong xác suất

## Mục tiêu cảnh

Làm rõ bản chất khoa học: watermark không phải chữ ẩn trong response, mà là mẫu thống kê trong phân phối xác suất.

## Visual trên màn hình

Hiển thị một response bình thường:

**“The answer is likely positive.”**

Sau đó bật hiệu ứng “X-ray view”.

Response mờ đi, phía sau hiện vector xác suất:

**Positive: 0.720**
**Neutral: 0.190**
**Negative: 0.090**

Một chiếc chìa khóa xuất hiện:

**Secret Key**

Vector xác suất thay đổi rất nhẹ:

**Positive: 0.721**
**Neutral: 0.187**
**Negative: 0.092**

Nhãn cuối vẫn là:

**Positive**

## Hiệu ứng gợi ý

* Response xuất hiện bình thường.
* X-ray scan chạy ngang qua response.
* Response chuyển thành biểu đồ xác suất.
* Secret Key đi vào vector.
* Các cột xác suất rung nhẹ, thay đổi rất nhỏ.
* Nhãn cuối cùng không đổi, để người xem hiểu chất lượng output vẫn gần như giữ nguyên.

## Text trên màn hình

**Probability Distribution**
**Tiny Shift**
**Same Prediction**

## Script voice-over

Điểm quan trọng là watermark này không nằm trong phần chữ mà người dùng nhìn thấy.
Nó không phải là một ký hiệu đặc biệt, một câu văn lặp lại, hay một dòng chữ ẩn trong response.
Bên ngoài, người dùng chỉ thấy một câu trả lời bình thường.
Nhưng bên trong, mô hình tạo ra một phân phối xác suất cho các lựa chọn đầu ra.
Ví dụ, mô hình có thể dự đoán Positive là 0.720, Neutral là 0.190, và Negative là 0.090.
Khi watermark được nhúng vào, một khóa bí mật sẽ điều chỉnh các xác suất này rất nhẹ: Positive thành 0.721, Neutral thành 0.187, và Negative thành 0.092.
Nhãn cuối cùng vẫn là Positive, nên chất lượng đầu ra gần như không thay đổi.
Nhưng qua rất nhiều câu trả lời, những dịch chuyển nhỏ này tạo thành một mẫu thống kê bí mật — chính là watermark.

---

# Cảnh 3.4.5 — Watermark đi theo quá trình distillation

## Mục tiêu cảnh

Cho thấy watermark có thể “di truyền” sang student model nếu student học từ output của mô hình gốc.

## Visual trên màn hình

Pipeline:

**Watermarked Victim API** → **Watermarked Outputs** → **Distillation Dataset** → **Student Model**

Trong mỗi output có các chấm nhỏ mờ, tượng trưng watermark.

Sau đó các chấm này đi vào Student Model.

Student Model phát sáng với hai lớp:

* Lớp trắng: **Main Capability**
* Lớp xanh mờ: **Hidden Watermark**

## Hiệu ứng gợi ý

* Các response bay ra từ Victim API.
* Ban đầu response nhìn bình thường.
* Bật “statistical view”, các chấm watermark hiện ra.
* Dataset hấp thụ các response.
* Student Model nhận dữ liệu và xuất hiện watermark mờ bên trong.

## Text trên màn hình

**Distillation transfers behavior**
**and may transfer watermark**

## Script voice-over

Khi kẻ tấn công dùng các đầu ra này để huấn luyện student model, họ đang cố học lại hành vi của mô hình gốc.

Nhưng nếu đầu ra của mô hình gốc đã mang watermark, student model có thể học luôn cả mẫu tín hiệu đó.

Nói cách khác, watermark có thể đi theo quá trình distillation.

Càng cố bắt chước mô hình gốc một cách chi tiết, bản sao càng có nguy cơ mang theo dấu vân tay của mô hình gốc.

Đây là điểm rất mạnh của watermark kháng distillation:

Nó biến chính quá trình sao chép thành một quá trình để lại dấu vết.

---

# Cảnh 3.4.6 — Ba phương pháp sẽ đi qua

## Mục tiêu cảnh

Tạo roadmap cho người xem trước khi đi sâu vào DRW.

## Visual trên màn hình

Ba card xuất hiện lần lượt:

Card 1:

**DRW**
**Probability Watermark**

Card 2:

**GINSEW**
**Sequence Watermark**

Card 3:

**CATER**
**Conditional Word Choice**

Nếu bạn chỉ đi DRW rồi CATER, bỏ card GINSEW hoặc để nhỏ hơn.

## Hiệu ứng gợi ý

* Card DRW xuất hiện trước và sáng nhất.
* Card GINSEW/CATER xuất hiện sau.
* Camera zoom vào DRW để chuyển cảnh.

## Text trên màn hình

**DRW → GINSEW → CATER**

Hoặc nếu bạn chuyển thẳng DRW → CATER:

**DRW → CATER**

## Script voice-over

Để hiện thực hóa ý tưởng watermark trên mô hình ngôn ngữ, có nhiều hướng kỹ thuật khác nhau.

Trong phần này, chúng ta sẽ lần lượt tìm hiểu ba hướng chính: DRW, GINSEW và CATER.

Đầu tiên là DRW — một phương pháp watermark kháng distillation, hoạt động bằng cách can thiệp trực tiếp vào phân phối xác suất của mô hình.

Tiếp theo, ta sẽ đi qua GINSEW, một hướng tiếp cận khác giúp watermark trở nên khó bị loại bỏ hơn trong quá trình sinh văn bản.

Cuối cùng là CATER, phương pháp phù hợp hơn với mô hình sinh ngôn ngữ, nơi watermark được nhúng tinh tế thông qua ngữ cảnh và lựa chọn từ.

Trước hết, hãy bắt đầu với DRW.

---

# Cảnh 3.5.1 — DRW là gì?

## Mục tiêu cảnh

Giới thiệu DRW như một ví dụ tiêu biểu của watermark kháng distillation.

## Visual trên màn hình

Tiêu đề lớn:

**DRW**
**Distillation-Resistant Watermarking**

Bên dưới là sơ đồ:

**Input Text** → **Victim NLP Model** → **Prediction Probabilities**

Ví dụ:

**Positive: 0.72**
**Neutral: 0.19**
**Negative: 0.09**

## Hiệu ứng gợi ý

* Chữ DRW xuất hiện kiểu technical title.
* Sơ đồ input → model → probability hiện từng bước.
* Biểu đồ xác suất xuất hiện dạng bar chart.

## Text trên màn hình

**DRW**
**Protects against distillation**

## Script voice-over

Một ví dụ tiêu biểu của hướng phòng thủ này là **DRW**, viết tắt của **Distillation-Resistant Watermarking**.

Ngay từ tên gọi, ta đã thấy mục tiêu chính của nó:

Tạo ra một watermark có khả năng chống lại quá trình distillation.

Nói cách khác, nếu một mô hình khác học lại từ đầu ra của mô hình gốc, watermark vẫn có cơ hội được truyền sang mô hình bị sao chép.

DRW tập trung vào một vị trí rất quan trọng:

**phân phối xác suất đầu ra** của mô hình.

---

# Cảnh 3.5.2 — DRW nhúng watermark bằng khóa bí mật

## Mục tiêu cảnh

Giải thích Secret Key tạo watermark pattern và nhúng vào xác suất.

## Visual trên màn hình

Bên trái:

**Secret Key**

Biểu tượng chìa khóa tạo ra một ma trận hoặc pattern:

**Watermark Pattern**

Pattern này tác động vào probability vector.

Sơ đồ:

**Secret Key** → **Watermark Pattern** → **Modified Probabilities**

Trước:

**[0.720, 0.190, 0.090]**

Sau:

**[0.721, 0.187, 0.092]**

## Hiệu ứng gợi ý

* Chìa khóa quay nhẹ rồi tạo ra các điểm sáng.
* Các điểm sáng xếp thành watermark pattern.
* Pattern đi vào vector xác suất.
* Vector đổi nhẹ, nhưng prediction label vẫn giữ nguyên.

## Text trên màn hình

**Secret Key**
**Watermark Pattern**
**Modified Probabilities**

## Script voice-over

Trong DRW, chủ sở hữu mô hình dùng một khóa bí mật để tạo ra một mẫu watermark.

Mẫu này sau đó được nhúng vào phân phối xác suất dự đoán của mô hình gốc.

Sự thay đổi phải đủ nhỏ để không làm hỏng chất lượng mô hình.

Nhưng cũng phải đủ có cấu trúc để có thể phát hiện lại sau này.

Với người dùng bình thường, mô hình vẫn hoạt động gần như như cũ.

Nhưng trong không gian xác suất, một tín hiệu bí mật đã được cài vào.

---

# Cảnh 3.5.3 — Soft labels: vì sao student học được watermark?

## Mục tiêu cảnh

Giải thích soft labels là cầu nối khiến watermark truyền sang student model.

## Visual trên màn hình

Chia đôi:

Bên trái: Hard label

**Positive**

Bên phải: Soft label

**Positive: 0.72**
**Neutral: 0.19**
**Negative: 0.09**

Sau đó soft label được đưa vào Student Model.

Hard label chỉ có một mũi tên đơn giản.

Soft label có nhiều thông tin hơn, kèm watermark pattern.

## Hiệu ứng gợi ý

* Hard label hiện đơn giản, một ô duy nhất.
* Soft label hiện thành vector nhiều giá trị.
* Highlight dòng “more information”.
* Các chấm watermark nằm trên soft label.
* Soft label chảy vào student model.

## Text trên màn hình

**Hard Label: one answer**
**Soft Label: probability pattern**

## Script voice-over

Lý do watermark có thể truyền sang bản sao nằm ở khái niệm **soft labels**.

Nếu mô hình gốc chỉ trả về nhãn cuối cùng, ví dụ “tích cực”, thì thông tin mà kẻ tấn công thu được khá hạn chế.

Nhưng trong nhiều kịch bản distillation, student model học từ toàn bộ phân phối xác suất của teacher model.

Phân phối này gọi là soft label.

Soft label chứa nhiều thông tin hơn hard label.

Nó cho biết mô hình chắc chắn đến mức nào.

Nó cũng cho thấy các lựa chọn phụ được mô hình đánh giá ra sao.

Và nếu soft label đã mang watermark, student model có thể học lại cả watermark đó trong quá trình distillation.

---

# Cảnh 3.5.4 — Probing: kiểm tra mô hình tình nghi

## Mục tiêu cảnh

Giải thích ownership verification: owner gửi query, detector phân tích output và tính watermark score.

## Visual trên màn hình

Sơ đồ:

**Owner** → **Probing Queries** → **Suspect Model** → **Outputs** → **Watermark Detector**

Detector hiện đồng hồ đo:

**Watermark Score**

Hai ngưỡng:

* Low: **Not enough evidence**
* High: **Strong evidence**

## Hiệu ứng gợi ý

* Owner gửi một tập query, không phải một query duy nhất.
* Suspect Model trả output.
* Outputs đi vào detector.
* Detector quét thống kê.
* Kim đồng hồ score tăng lên.
* Nếu score cao, hiện “Strong evidence of distillation”.

## Text trên màn hình

**Probing Queries**
**Watermark Score**
**Strong Evidence**

## Script voice-over

Khi nghi ngờ một mô hình đã bị sao chép, chủ sở hữu có thể thực hiện quá trình **probing**.

Họ gửi một tập truy vấn đặc biệt đến mô hình tình nghi.

Sau đó, họ thu thập các output hoặc phân phối xác suất mà mô hình trả về.

Các kết quả này được đưa vào một bộ kiểm tra watermark.

Nếu mẫu tín hiệu thu được khớp với watermark được tạo bởi khóa bí mật, hệ thống sẽ cho ra một điểm số phát hiện.

Điểm số càng cao, dấu hiệu mô hình tình nghi từng học từ mô hình gốc càng mạnh.

Tuy nhiên, đây nên được hiểu là một bằng chứng kỹ thuật quan trọng, không phải một phán quyết tuyệt đối.

Trong thực tế, nó cần được kết hợp với các bằng chứng khác như log API, lịch sử truy vấn, dữ liệu huấn luyện và bối cảnh pháp lý.

---

# Cảnh 3.5.5 — Điểm mạnh và giới hạn của DRW

## Mục tiêu cảnh

Trình bày khoa học, không thần thánh hóa DRW.

## Visual trên màn hình

Chia đôi màn hình:

Bên trái: Strengths

* **Invisible**
* **Secret-key based**
* **Transfers via distillation**

Bên phải: Limitations

* **Weak if only hard labels**
* **Diluted by mixed data**
* **May degrade if too strong**

## Hiệu ứng gợi ý

* Strengths hiện với dấu check.
* Limitations hiện với dấu cảnh báo.
* Cân bằng ở giữa màn hình: **Quality ↔ Detectability**.
* Thanh trượt minh họa: watermark mạnh hơn thì detectability tăng nhưng quality có thể giảm.

## Text trên màn hình

**Quality ↔ Detectability**

## Script voice-over

DRW có ba điểm mạnh lớn.

Thứ nhất, watermark có tính vô hình.

Nó không hiện ra trực tiếp trong câu trả lời.

Thứ hai, watermark được tạo từ khóa bí mật, nên người ngoài rất khó biết chính xác cần xóa điều gì.

Thứ ba, watermark có thể đi theo quá trình distillation nếu bản sao học từ phân phối xác suất của mô hình gốc.

Nhưng DRW cũng có giới hạn.

Nếu kẻ tấn công chỉ lấy nhãn cuối cùng thay vì lấy toàn bộ xác suất, tín hiệu watermark có thể yếu hơn.

Nếu dữ liệu distillation bị trộn với nhiều nguồn khác, watermark có thể bị pha loãng.

Và nếu watermark được nhúng quá mạnh, chất lượng đầu ra của mô hình gốc có thể bị ảnh hưởng.

Vì vậy, DRW luôn phải cân bằng giữa hai mục tiêu:

giữ chất lượng mô hình ổn định,

và giữ tín hiệu watermark đủ rõ để phát hiện khi cần.

---

# Cảnh 3.5.6 — Tổng kết DRW

## Mục tiêu cảnh

Chốt lại toàn bộ phần DRW: watermark được nhúng vào phân phối xác suất, có thể truyền qua distillation, và được phát hiện lại để kiểm tra model extraction.

## Visual trên màn hình

Một sơ đồ tóm tắt DRW:

**Secret Key** → **Probability Pattern** → **Distilled Student Model** → **Watermark Detection**

Bên dưới hiện lại một response bình thường:

**“The answer is likely positive.”**

Sau đó bật chế độ X-ray.

Response mờ đi, phía sau hiện vector xác suất:

**Positive: 0.721**
**Neutral: 0.187**
**Negative: 0.092**

Các chấm watermark nhỏ xuất hiện trên vector xác suất.

Sau đó vector này chảy vào **Student Model**.

Cuối cùng, Student Model được kiểm tra bằng **Watermark Detector**.

Nếu detector tìm thấy pattern, màn hình hiện kết luận:

**Watermark detected**
**Possible distilled copy**

## Hiệu ứng gợi ý

* Pipeline DRW hiện bằng 4 icon.
* Các icon lần lượt sáng lên theo voice-over.
* Khi nói “secret key”, icon chìa khóa phát sáng.
* Khi nói “phân phối xác suất”, vector xác suất được highlight.
* Các chấm watermark xuất hiện trong probability pattern.
* Probability pattern chảy vào Student Model.
* Detector quét qua Student Model.
* Một đường sóng hoặc tín hiệu thống kê hiện ra.
* Cuối cùng đóng dấu: **Detected**.

## Text trên màn hình

**Secret Key → Probability Pattern**

**Probability Pattern → Student Model**

**Watermark Detection**

**DRW: Distillation-Resistant Watermarking**

## Script voice-over

Tóm lại, DRW cho chúng ta thấy một ý tưởng rất quan trọng.

Watermark không nhất thiết phải hiện ra trực tiếp trong câu chữ.

Nó có thể nằm ẩn trong phân phối xác suất đầu ra của mô hình.

Với một secret key, mô hình gốc có thể tạo ra những thay đổi rất nhỏ trong xác suất.

Những thay đổi này không làm thay đổi đáng kể câu trả lời cuối cùng.

Nhưng chúng tạo thành một mẫu thống kê riêng.

Khi một kẻ tấn công dùng các đầu ra này để distill ra student model, student không chỉ học cách trả lời.

Nó còn có thể học lại cả mẫu watermark nằm trong phân phối xác suất đó.

Sau đó, bằng cách kiểm tra đầu ra của mô hình nghi ngờ, ta có thể tìm lại mẫu watermark này.

Nếu tín hiệu xuất hiện rõ ràng, đó là bằng chứng cho thấy mô hình nghi ngờ có thể đã được distill từ mô hình gốc.

Đó là lý do DRW được gọi là **Distillation-Resistant Watermarking** — watermark được thiết kế để vẫn tồn tại ngay cả khi mô hình bị sao chép thông qua distillation.

