## Mở đầu: Phòng thủ không dùng thủy vân

Sau các phương pháp dựa trên watermark, ta chuyển sang một hướng khác.
Lần này, ta không nhúng watermark, không sửa output, và không tiêm trigger bí mật vào mô hình gốc.
Phương pháp được nhắc đến là **DeepJudge**, một framework kiểm thử được giới thiệu bởi Chen và cộng sự.
DeepJudge dựa trên một ý tưởng rất trực tiếp:
Nếu một mô hình nghi ngờ thật sự bắt nguồn từ mô hình nạn nhân, thì giữa hai mô hình có thể vẫn còn những điểm giống nhau bất thường.
Sự giống nhau đó có thể nằm ở hành vi trước input khó, ở output của các layer, hoặc ở pattern kích hoạt neuron bên trong mô hình.

---

## Cảnh 3.13.1: DeepJudge khác gì watermark?

Các phương pháp watermark thường cần chuẩn bị trước.
Chủ sở hữu phải cấy một tín hiệu bí mật vào mô hình trước khi phát hành.
Sau đó, khi nghi ngờ có bản sao, họ kiểm tra xem tín hiệu đó còn tồn tại hay không.
DeepJudge đi theo hướng khác.
Nó không yêu cầu can thiệp vào mô hình gốc.
Không cần thêm dữ liệu fingerprint.
Không cần một trigger bí mật.
Thay vào đó, khi có mô hình nghi ngờ, DeepJudge chạy một bộ test để so sánh mô hình đó với mô hình nạn nhân.
Nói ngắn gọn: watermark là cấy trước rồi kiểm tra sau.
Còn DeepJudge là không cấy trước, mà kiểm thử sự tương đồng sau.

---

## Cảnh 3.13.2: Ba mối đe dọa DeepJudge có thể kiểm tra

DeepJudge có thể được dùng trong nhiều kịch bản xâm phạm mô hình.
Kịch bản thứ nhất là **distillation**.
Ở đây, mô hình nghi ngờ có thể được huấn luyện để bắt chước output hoặc hành vi của mô hình nạn nhân.
Kịch bản thứ hai là **fine-tuning**.
Một mô hình gốc bị sao chép, sau đó được tinh chỉnh thêm trên dữ liệu mới để thay đổi hành vi bề ngoài.
Kịch bản thứ ba là **pruning-finetuning**.
Mô hình bị cắt tỉa tham số, rồi fine-tune lại để phục hồi hiệu năng và che giấu nguồn gốc.
Dù con đường sao chép khác nhau, DeepJudge đặt cùng một câu hỏi:
Mô hình nghi ngờ M2 có quá giống mô hình nạn nhân M1 hay không?

---

## Cảnh 3.13.3: Robustness Distance - RobD

Metric đầu tiên là **Robustness Distance**, viết tắt là RobD.
RobD đo khoảng cách về độ bền vững giữa hai mô hình.
Để làm điều này, DeepJudge tạo ra các ví dụ đối kháng không có mục tiêu cụ thể.
Ta có thể hiểu chúng là những input được chỉnh nhẹ để làm mô hình khó dự đoán hơn, nhưng không ép mô hình phải đi về một nhãn cụ thể.
Sau đó, cùng một nhóm ví dụ đối kháng được đưa vào mô hình nạn nhân M1 và mô hình nghi ngờ M2.
Điểm quan trọng ở đây là DeepJudge không đo trên dữ liệu bất kỳ một cách mơ hồ.
Nó đo trên các test case cụ thể, ví dụ như adv của x_i đang hiển thị trên màn hình.
Ở phần công thức phía dưới, Rob của một mô hình được hiểu là tổng số lần mô hình vẫn dự đoán đúng nhãn thật y_i sau khi input đã bị biến thành adversarial example.
Sau đó, RobD giữa f1 và f2 chính là độ lệch tuyệt đối giữa hai giá trị Rob này.
Nếu hai mô hình phản ứng giống nhau trước các input khó này, khoảng cách RobD sẽ nhỏ.
Điều đó cho thấy ranh giới quyết định hoặc hành vi độ bền vững của hai mô hình có thể rất gần nhau.

---

## Cảnh 3.13.4: Layer Output Distance - LOD

Metric thứ hai là **Layer Output Distance**, hay LOD.
Metric này không chỉ nhìn vào output cuối cùng của mô hình.
Nó đi vào một layer cụ thể, gọi là layer k.
Với cùng một input, DeepJudge lấy output tại layer k của mô hình nạn nhân và output tại layer k tương ứng của mô hình nghi ngờ.
Sau đó, nó đo khoảng cách giữa hai vector biểu diễn này.
Trong công thức đang hiển thị, f1 mũ k của x_i là output ở layer k của model 1.
Còn f2 mũ k của x_i là output ở layer k của model 2.
LOD cộng dồn khoảng cách chuẩn p giữa hai output layer này trên toàn bộ tập test.
Nếu LOD nhỏ, nghĩa là ở cùng một tầng xử lý, hai mô hình đang tạo ra biểu diễn rất giống nhau.
Đây là dấu hiệu mạnh hơn việc chỉ giống câu trả lời cuối cùng.
Nó cho thấy mô hình nghi ngờ có thể đang giữ lại cấu trúc biểu diễn bên trong từ mô hình nạn nhân.

---

## Cảnh 3.13.5: Layer Activation Distance - LAD

Metric thứ ba là **Layer Activation Distance**, hay LAD.
LOD so sánh giá trị output của layer.
Còn LAD nhìn vào pattern kích hoạt neuron.
Với một input nhất định, DeepJudge kiểm tra neuron nào được kích hoạt vượt qua một ngưỡng.
Neuron vượt ngưỡng được xem là đang bật.
Neuron không vượt ngưỡng được xem là không bật.
Trên màn hình, hàm S chính là hàm ngưỡng dùng để biến giá trị activation thành trạng thái bật hoặc tắt.
Sau đó, LAD cộng dồn độ khác nhau giữa pattern kích hoạt của model 1 và model 2 trên toàn bộ tập test.
Nếu cùng một input làm kích hoạt gần như cùng một nhóm neuron, LAD sẽ nhỏ.
Điều đó gợi ý rằng hai mô hình không chỉ cho output giống nhau, mà còn xử lý input theo những đường nội bộ tương tự.
Tùy metric, DeepJudge cần mức truy cập khác nhau.
Các metric dựa trên output cuối cùng có thể gần với black-box hơn.
Còn LOD và LAD cần quan sát layer hoặc neuron bên trong mô hình, nên phù hợp hơn với kịch bản white-box.

---

## Cảnh 3.13.6: Test cases, metrics và delta score

Điểm cốt lõi của DeepJudge là đánh giá hai mô hình bằng một tập test case.
Các test case này có thể đến từ seed ban đầu, hoặc được tạo thêm để làm nổi bật sự giống và khác nhau giữa mô hình nạn nhân và mô hình nghi ngờ.
Sau đó, cùng một tập test case được đưa qua nhiều metric khác nhau.
DeepJudge không dựa vào một metric duy nhất.
Nó chạy nhiều bộ test khác nhau.
Mỗi bộ test tạo ra một khoảng cách điểm số, gọi là **delta score**.
Một delta score có thể đến từ RobD.
Một delta score khác có thể đến từ LOD.
Một delta score khác nữa có thể đến từ LAD.
Mỗi score trả lời một câu hỏi cục bộ: theo metric này, M2 có gần M1 một cách bất thường hay không?
Vì mỗi metric có thể có nhiễu riêng, DeepJudge kết hợp nhiều tín hiệu để quyết định chắc hơn.

---

## Cảnh 3.13.7: Ngưỡng τ và negative models

Để biến một khoảng cách thành quyết định, DeepJudge cần một ngưỡng.
Ngưỡng này được ký hiệu là Tau.
Tau được xác định từ biên dưới của các mô hình âm tính.
Mô hình âm tính là những mô hình không phải bản sao của mô hình nạn nhân.
Trực giác là như sau.
Nếu khoảng cách giữa M1 và M2 vẫn nằm trong vùng bình thường của các mô hình âm tính, ta chưa có bằng chứng mạnh.
Nhưng nếu delta score của M2 còn nhỏ hơn cả biên dưới của nhóm âm tính, thì M2 đang gần M1 một cách bất thường.
Khi đó, test này bỏ phiếu rằng M2 có khả năng là bản sao.
Nói bằng công thức ngắn:
Nếu delta score nhỏ hơn Tau, test bỏ phiếu copy.
Nếu delta score lớn hơn hoặc bằng Tau, test bỏ phiếu not copy.

---

## Cảnh 3.13.8: Majority Voting

Sau khi có nhiều delta score, DeepJudge không kết luận chỉ từ một phép đo.
Mỗi metric sẽ tạo ra một phiếu.
RobD có thể bỏ phiếu copy.
LOD có thể bỏ phiếu copy.
LAD có thể bỏ phiếu not copy.
Các phiếu này được đưa vào cơ chế **majority voting**, tức bầu chọn theo đa số.
Nếu đa số metric cho thấy khoảng cách giữa M1 và M2 nhỏ hơn ngưỡng, hệ thống kết luận rằng M2 có khả năng là bản sao của M1.
Ngược lại, nếu đa số metric không vượt qua điều kiện này, DeepJudge kết luận rằng chưa đủ bằng chứng để xem M2 là bản sao.
Cơ chế bầu chọn giúp hệ thống bớt phụ thuộc vào một metric đơn lẻ.

---

## Cảnh 3.13.9: Tổng kết DeepJudge

Tóm lại, DeepJudge là một phương pháp xác minh quyền sở hữu mô hình không dựa vào watermark.
Nó không cần cấy dấu vân tay trước khi phát hành.
Khi có mô hình nghi ngờ, DeepJudge so sánh mô hình đó với mô hình nạn nhân bằng nhiều bộ test.
RobD kiểm tra sự giống nhau về độ bền vững trước adversarial examples.
LOD kiểm tra sự giống nhau của output tại layer k.
LAD kiểm tra sự giống nhau của pattern kích hoạt neuron.
Sau đó, mỗi metric tạo ra một delta score.
Delta score được so với ngưỡng τ, vốn được xác định từ các mô hình âm tính.
Cuối cùng, DeepJudge dùng majority voting để kết luận M2 có phải là bản sao của M1 hay không.
Điểm mạnh của DeepJudge là nó không cần sửa mô hình gốc, nhưng vẫn có thể kiểm tra các kịch bản như distillation, fine-tuning và pruning-finetuning.
