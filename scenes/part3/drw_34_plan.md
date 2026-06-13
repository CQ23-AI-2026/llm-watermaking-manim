# Kế hoạch cảnh 3.4 - Dẫn nhập watermark kháng sao chép

File triển khai: `scenes/part3/drw_34.py`

Mục tiêu của cụm 3.4 là làm cầu nối ngắn giữa mối đe dọa model extraction/distillation và ba phương pháp phía sau: DRW, GINSEW, CATER. Phần này không đi sâu công thức; chỉ cần người xem hiểu vì sao watermark phải nằm ở hành vi hoặc phân phối của mô hình.

Style visual: nền tối có grid mờ theo phong cách 3Blue1Brown, chủ đạo nâu/gold, điểm nhấn xanh cho mô hình gốc hoặc tín hiệu model.

---

## Cảnh 3.4.0 - Title mở đầu

### Mục tiêu

Mở cụm 3.4 giống các phần trước: tiêu đề xuất hiện ở giữa màn hình, sau đó thu lên thành banner trên cùng.

### Visual

```text
PHÒNG THỦ CHỐNG MODEL EXTRACTION
```

### Voice file

`scenes/part3/assets/drw_34/drw_34_title.mp3`

### Script

Vậy làm sao để phòng thủ chống model extraction: làm sao để một bản sao học lại mô hình gốc vẫn để lộ dấu hiệu sở hữu.

---

## Cảnh 3.4.1 - Vì sao cần watermark kháng sao chép?

### Mục tiêu

Nêu ngắn gọn mối đe dọa: kẻ tấn công không cần lấy trọng số, chỉ cần gọi API nhiều lần để thu prompt-response và huấn luyện student model.

### Visual

```text
Attacker -> Victim API -> Dataset -> Student
```

Các node nằm cùng một hàng để dễ đọc. Victim API dùng màu xanh, dataset và mũi tên dùng nâu/gold.

### Voice file

`scenes/part3/assets/drw_34/drw_34_1_threat.mp3`

### Script

Trước khi vào từng kỹ thuật, ta cần thấy vấn đề chung. Trong model extraction, kẻ tấn công không nhất thiết phải lấy trọng số của mô hình. Họ có thể gọi API hàng loạt, lưu lại các cặp prompt và response, rồi dùng dữ liệu đó để huấn luyện một student model bắt chước hành vi của mô hình gốc.

---

## Cảnh 3.4.2 - Ý tưởng chung: tín hiệu bí mật đi theo hành vi

### Mục tiêu

Giải thích trực giác của model watermarking chống sao chép: nếu bản sao học hành vi từ teacher, ta muốn nó vô tình học luôn một tín hiệu bí mật.

### Visual

```text
Teacher -> Student -> Verifier
Secret key K -> Student
```

Luồng behavior dùng xanh; secret key K dùng một mũi tên gold chỉ trực tiếp vào Student.

### Voice file

`scenes/part3/assets/drw_34/drw_34_2_signal.mp3`

### Script

Từ đây xuất hiện ý tưởng phòng thủ: nếu student model học từ output hoặc hành vi của teacher, ta có thể cài một tín hiệu bí mật đủ nhỏ để không làm hỏng chất lượng, nhưng đủ ổn định để đi theo quá trình sao chép. Watermark không nhất thiết nằm trong chữ; nó có thể nằm trong xác suất, trong lựa chọn token, hoặc trong phản ứng của mô hình trước một nhóm input bí mật.

---

## Cảnh 3.4.3 - Mẫu xác minh chung

### Mục tiêu

Cho người xem công thức tư duy chung trước khi vào ba phương pháp: dùng secret prompts hoặc secret key, lấy responses/logits, rồi tính score để quyết định nghi ngờ copy.

### Visual

```text
Secret prompts -> Suspect -> Responses / logits -> Detector

score(K, M) > tau  =>  copy likely
```

### Voice file

`scenes/part3/assets/drw_34/drw_34_3_verify.mp3`

### Script

Khi cần xác minh, chủ sở hữu không chỉ nhìn một câu trả lời riêng lẻ. Họ dùng khóa hoặc bộ prompt bí mật để truy vấn mô hình nghi ngờ, thu lại output hoặc logits, rồi tính một điểm thống kê. Nếu điểm này vượt ngưỡng, mô hình nghi ngờ có khả năng đã học lại dấu hiệu của mô hình gốc.

---

## Cảnh 3.4.4 - Roadmap sang DRW, GINSEW, CATER

### Mục tiêu

Chốt phần dẫn nhập và chuyển mạch sang ba phương pháp tiếp theo.

### Visual

Ba card nằm cùng hàng:

```text
DRW       | tín hiệu xác suất kháng distillation
GINSEW    | can thiệp nhẹ khi sinh token
CATER     | watermark có điều kiện theo ngữ cảnh
```

Không hiển thị thêm dòng “Từ đây clip đi qua...” ở dưới; chỉ giữ nội dung của ba phương pháp.

### Voice file

`scenes/part3/assets/drw_34/drw_34_4_roadmap.mp3`

### Script

Với khung nhìn đó, ta có ba hướng cụ thể. DRW tập trung vào tín hiệu xác suất để chống distillation. GINSEW đưa watermark vào quá trình sinh token của mô hình ngôn ngữ. CATER làm watermark có điều kiện theo ngữ cảnh để tự nhiên hơn và khó bị tách khỏi hành vi của mô hình. Sau đây ta đi lần lượt qua DRW, GINSEW và CATER.
