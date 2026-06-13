# Kế hoạch cảnh 3.13 - DeepJudge: phòng thủ không dùng thủy vân

File triển khai dự kiến: `scenes/part3/deepjudge.py`

Phạm vi: giải thích **DeepJudge** của Chen và cộng sự như một framework kiểm thử dựa trên tính tương đồng. Khác với các phương pháp watermark, DeepJudge không cần tiêm hay can thiệp vào mô hình gốc trước khi phát hành. Thay vào đó, nó so sánh hành vi và biểu diễn bên trong giữa mô hình nạn nhân và mô hình nghi ngờ.

DeepJudge có thể được dùng để kiểm tra các mô hình nghi ngờ trong ba kịch bản:

```text
Distillation
Fine-tuning
Pruning-Finetuning
```

Trọng tâm kỹ thuật:

```text
Victim model M1
Suspect model M2
testing framework
similarity-based verification
Robustness Distance - RobD
Layer Output Distance - LOD
Layer Activation Distance - LAD
delta score
threshold tau
negative models
majority voting
copy / not copy
```

---

## Cảnh 3.13.0 - Mở đầu tiêu đề DeepJudge

### Mục tiêu

Giới thiệu một nhánh phòng thủ khác: không dùng watermark, không tiêm dấu vân tay, mà dùng kiểm thử và phân loại dựa trên độ tương đồng.

### Visual

Mở đầu giống phần Fingerprinting:

```text
PHÒNG THỦ KHÔNG DÙNG THỦY VÂN
DeepJudge - Similarity-based Testing
```

Tiêu đề lớn ở giữa màn hình, có underline vàng, sau đó transform lên banner trên cùng.

### Text trên màn hình

```text
DeepJudge
Không tiêm watermark
Kiểm thử tính tương đồng
```

### Voice-over đề xuất

Sau các phương pháp dựa trên watermark, ta chuyển sang một hướng khác: không cấy bất kỳ dấu hiệu bí mật nào vào mô hình.

DeepJudge, được giới thiệu bởi Chen và cộng sự, là một framework kiểm thử dựa trên tính tương đồng.

Thay vì hỏi mô hình có mang watermark hay không, DeepJudge hỏi: mô hình nghi ngờ có hành vi và biểu diễn bên trong quá giống mô hình nạn nhân hay không?

---

## Cảnh 3.13.1 - DeepJudge khác gì watermark?

### Mục tiêu

Làm rõ điểm khác biệt cốt lõi: DeepJudge không can thiệp vào mô hình gốc trước khi phát hành.

### Visual

Chia màn hình hai bên:

```text
Watermark-based defense
Inject hidden signal -> release model

DeepJudge
No injection -> run tests later
```

Bên watermark có biểu tượng dấu vân tay được cấy vào model. Bên DeepJudge có bộ test đi vào cả Victim và Suspect.

### Text trên màn hình

```text
Không cấy trước
Kiểm tra sau
```

### Voice-over đề xuất

Các phương pháp watermark cần chuẩn bị từ trước: chủ sở hữu phải cấy một tín hiệu bí mật vào mô hình trước khi phát hành.

DeepJudge đi theo hướng khác.

Nó không yêu cầu sửa mô hình gốc, không cần thêm dữ liệu fingerprint, và không cần watermark nằm trong output.

Khi có một mô hình nghi ngờ, DeepJudge tạo các bộ test để so sánh mô hình đó với mô hình nạn nhân.

---

## Cảnh 3.13.2 - Ba mối đe dọa DeepJudge có thể kiểm tra

### Mục tiêu

Cho thấy DeepJudge áp dụng cho nhiều kiểu sao chép mô hình, không chỉ fine-tuning.

### Visual

Victim model ở bên trái, ba nhánh tạo ra ba mô hình nghi ngờ:

```text
Victim M1
  -> Distillation
  -> Fine-tuning
  -> Pruning-Finetuning
```

Ba nhánh hội tụ vào một khối:

```text
DeepJudge Test Suite
```

### Text trên màn hình

```text
Distillation
Fine-tuning
Pruning-Finetuning
```

### Voice-over đề xuất

DeepJudge được thiết kế để kiểm tra nhiều dạng xâm phạm mô hình.

Một mô hình nghi ngờ có thể đến từ distillation, tức học lại hành vi của mô hình nạn nhân.

Nó cũng có thể đến từ fine-tuning, khi bản sao được tinh chỉnh thêm trên dữ liệu mới.

Hoặc nó có thể đi qua pruning rồi fine-tuning, tức cắt tỉa tham số để che giấu dấu vết rồi huấn luyện lại.

Điểm chung là: nếu mô hình nghi ngờ thật sự bắt nguồn từ mô hình nạn nhân, một số hành vi hoặc biểu diễn bên trong vẫn có thể quá giống nhau.

---

## Cảnh 3.13.3 - Metric 1: Robustness Distance - RobD

### Mục tiêu

Giải thích RobD đo xem hai mô hình phản ứng giống nhau thế nào trước các ví dụ đối kháng không có mục tiêu cụ thể.

### Visual

Layout mới chia rõ hai tầng, trong đó test case là tín hiệu đầu vào chính:

```text
Tầng trên:
adv(x_i) / test case  ->  Victim M1  ->  Suspect M2
```

Tầng dưới hiển thị khung công thức lớn, đặt thấp để tránh đè lên phần minh họa:

```text
Rob(f) = sum_{i=1}^{N} delta(f(adv(x_i)) = y_i)
RobD(f1, f2) = |Rob(f1) - Rob(f2)|
```

Chú thích nhỏ:

```text
groundtruth label -> y_i
```

Mũi tên từ hai model đi xuống công thức để nhấn mạnh cùng một test case được đưa qua cả M1 và M2, sau đó mới tính RobD.

### Text trên màn hình

```text
RobD
Khoảng cách độ bền vững
RobD nhỏ -> hai mô hình bền vững giống nhau trước input đối kháng
```

### Voice-over đề xuất

Metric đầu tiên là Robustness Distance, viết tắt là RobD.

Ý tưởng là tạo ra các ví dụ đối kháng không nhắm vào một lớp cụ thể.

Sau đó, DeepJudge quan sát xem mô hình nạn nhân và mô hình nghi ngờ có phản ứng giống nhau trước những ví dụ khó này hay không.

Trên màn hình, Rob của một mô hình được tính bằng tổng số lần mô hình vẫn dự đoán đúng nhãn thật y_i sau khi input đã bị biến thành ví dụ đối kháng.

Sau đó, RobD giữa f1 và f2 được tính bằng độ lệch tuyệt đối giữa Rob của hai mô hình.

Nếu hai mô hình cùng sai theo cách giống nhau, hoặc cùng thay đổi dự đoán theo những mẫu tương tự, khoảng cách RobD sẽ nhỏ.

Một RobD nhỏ là dấu hiệu cho thấy hai mô hình có độ bền vững và ranh giới quyết định gần nhau.

---

## Cảnh 3.13.4 - Metric 2: Layer Output Distance - LOD

### Mục tiêu

Giải thích LOD so sánh đầu ra tại cùng một lớp k của hai mô hình.

### Visual

Layout mới:

```text
Tầng trên:
Victim M1 network       Suspect M2 network
layer k được highlight ở cả hai mạng
```

Tầng dưới hiển thị công thức lớn:

```text
LOD_k(f1, f2) = sum_{i=1}^{N} || f1^k(x_i) - f2^k(x_i) ||_p
```

Chú thích dưới công thức:

```text
f1^k(x_i): layer k of model 1
f2^k(x_i): layer k of model 2
```

Mục tiêu bố cục: công thức nằm phía dưới, hai network nằm phía trên để không đè lên nhau.

### Text trên màn hình

```text
LOD
So sánh output tại layer k
LOD so sánh giá trị output tại cùng layer k
```

### Voice-over đề xuất

Metric thứ hai là Layer Output Distance, hay LOD.

Thay vì chỉ nhìn vào câu trả lời cuối cùng, DeepJudge đi vào một lớp cụ thể của mô hình.

Với cùng một input, nó lấy đầu ra tại layer k của mô hình nạn nhân và layer k tương ứng của mô hình nghi ngờ.

Trên màn hình, công thức LOD_k cộng dồn khoảng cách chuẩn p giữa f1^k(x_i) và f2^k(x_i) trên toàn bộ tập test.

Nếu hai biểu diễn này gần nhau, LOD sẽ nhỏ.

Điều đó gợi ý rằng mô hình nghi ngờ không chỉ bắt chước output, mà còn giữ lại cấu trúc biểu diễn bên trong tương tự mô hình nạn nhân.

---

## Cảnh 3.13.5 - Metric 3: Layer Activation Distance - LAD

### Mục tiêu

Giải thích LAD so sánh mẫu kích hoạt neuron dựa trên một ngưỡng.

### Visual

Layout mới:

```text
Tầng trên:
M1 activation grid     S(z) threshold function     M2 activation grid
```

Tầng dưới hiển thị công thức lớn:

```text
LAD_k(f1, f2) = sum_{i=1}^{N} | S(f1^k(x_i)) - S(f2^k(x_i)) |
```

Trong công thức, `S` là hàm ngưỡng: neuron vượt ngưỡng thì xem là bật, không vượt ngưỡng thì xem là tắt.

Mục tiêu bố cục: grid neuron và `S(z)` nằm phía trên, công thức LAD nằm phía dưới để dễ đọc.

### Text trên màn hình

```text
LAD
So sánh pattern kích hoạt neuron
LAD so sánh pattern neuron bật/tắt sau hàm ngưỡng S
```

### Voice-over đề xuất

Metric thứ ba là Layer Activation Distance, hay LAD.

Ở đây DeepJudge không chỉ so sánh giá trị output của layer.

Nó kiểm tra neuron nào được kích hoạt, dựa trên một ngưỡng nhất định.

Trên màn hình, hàm S biến output tại layer k thành pattern bật hoặc tắt.

LAD_k cộng dồn độ khác nhau giữa pattern kích hoạt của model 1 và model 2 trên từng input.

Nếu cùng một input làm sáng lên gần như cùng một tập neuron ở cả hai mô hình, mẫu kích hoạt của chúng giống nhau.

Khi LAD nhỏ, điều đó cho thấy hai mô hình có cấu trúc phản ứng nội bộ rất gần nhau.

---

## Cảnh 3.13.6 - Test cases, metrics và delta score

### Mục tiêu

Làm rõ DeepJudge không chỉ có metric. Trước hết nó cần một tập test case. Các test case này được chạy qua nhiều metric, rồi mỗi metric mới sinh ra một delta score.

### Visual

Pipeline đặt thấp hơn tiêu đề để tránh đè chữ:

```text
Test Cases: x_1 ... x_N
        -> Metric 1: RobD -> δscore_1
        -> Metric 2: LOD  -> δscore_2
        -> Metric 3: LAD  -> δscore_3
        -> Metric N       -> δscore_N
        -> Score Stack
```

Trọng tâm visual: card `Test Cases` nằm bên trái, nhiều metric nằm giữa, `Score Stack` nằm bên phải.

### Text trên màn hình

```text
Test cases -> Metrics -> Delta score
```

### Voice-over đề xuất

DeepJudge bắt đầu từ một tập test case.

Các test case này có thể được chọn từ seed ban đầu, hoặc được tạo ra để làm nổi bật sự giống và khác nhau giữa hai mô hình.

Sau đó, DeepJudge không dựa vào một phép đo duy nhất.

Nó chạy nhiều bộ test khác nhau, mỗi bộ test tạo ra một khoảng cách điểm số, ký hiệu là delta score.

Mỗi delta score trả lời một câu hỏi cục bộ: theo metric này, mô hình nghi ngờ có gần mô hình nạn nhân không?

Vì mỗi metric có thể nhiễu hoặc không đủ mạnh trong một trường hợp cụ thể, DeepJudge kết hợp nhiều tín hiệu lại với nhau.

---

## Cảnh 3.13.7 - Ngưỡng τ và negative models

### Mục tiêu

Giải thích cách quyết định một score là "gần bất thường" hay không: so với ngưỡng τ.

### Visual

Trục số khoảng cách:

```text
small distance ---------------- large distance
```

Các điểm negative models nằm bên phải. Biên dưới của nhóm negative models xác định ngưỡng:

```text
τ = lower bound of negative models
```

Nếu `δscore < τ`, test này bỏ phiếu "copy".

### Text trên màn hình

```text
δscore < τ  ->  vote: copy
δscore ≥ τ  ->  vote: not copy
```

### Voice-over đề xuất

Để biến khoảng cách thành quyết định, DeepJudge dùng một ngưỡng τ.

Ngưỡng này được xác định dựa trên biên dưới của các mô hình âm tính, tức các mô hình không phải bản sao.

Trực giác là: nếu một mô hình nghi ngờ còn gần mô hình nạn nhân hơn cả vùng gần nhất của các mô hình âm tính, thì sự gần nhau đó là bất thường.

Khi delta score nhỏ hơn τ, test đó bỏ phiếu rằng mô hình nghi ngờ có khả năng là bản sao.

Nếu delta score lớn hơn hoặc bằng τ, test đó bỏ phiếu không phải bản sao.

---

## Cảnh 3.13.8 - Majority Voting: kết luận copy hay không

### Mục tiêu

Giải thích cơ chế quyết định cuối cùng bằng bầu chọn đa số.

### Visual

Nhiều card test:

```text
RobD: copy
LOD : copy
LAD : not copy
...
```

Các phiếu đi vào một hộp:

```text
Majority Voting
```

Kết luận:

```text
M2 is a copy of M1
```

hoặc

```text
M2 is not a copy
```

### Text trên màn hình

```text
Đa số metric đồng ý
-> quyết định cuối cùng
```

### Voice-over đề xuất

Sau khi từng metric đã bỏ phiếu, DeepJudge dùng majority voting.

Nếu đa số bộ test cho rằng khoảng cách giữa M1 và M2 nhỏ bất thường, hệ thống kết luận rằng M2 có khả năng là bản sao của M1.

Ngược lại, nếu đa số metric không vượt qua ngưỡng, kết luận là chưa đủ bằng chứng để xem M2 là bản sao.

Cơ chế này giúp DeepJudge bớt phụ thuộc vào một metric đơn lẻ.

---

## Cảnh 3.13.9 - Tổng kết DeepJudge

### Mục tiêu

Tóm lại vai trò của DeepJudge trong nhóm phòng thủ model ownership verification.

### Visual

Pipeline tổng kết:

```text
Victim M1 + Suspect M2
        -> RobD / LOD / LAD
        -> δscore < τ ?
        -> Majority Voting
        -> copy / not copy
```

Card tổng kết:

```text
Không cần watermark
So sánh hành vi và biểu diễn
Áp dụng cho distillation, fine-tuning, pruning-finetuning
```

### Voice-over đề xuất

Tóm lại, DeepJudge là một hướng phòng thủ không dựa vào watermark.

Nó không cần cấy dấu hiệu bí mật vào mô hình gốc.

Thay vào đó, nó kiểm thử mô hình nạn nhân và mô hình nghi ngờ bằng nhiều metric tương đồng.

RobD nhìn vào độ bền vững trước adversarial examples.

LOD nhìn vào output tại layer.

LAD nhìn vào pattern kích hoạt neuron.

Sau đó, các delta score được so với ngưỡng τ và kết hợp bằng majority voting.

Nếu đa số metric cho thấy M2 quá giống M1, DeepJudge kết luận rằng M2 có khả năng là bản sao.
