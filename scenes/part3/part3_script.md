# Script lồng tiếng: Part 3 — Model Watermark

## Thủy vân mô hình và bảo vệ quyền sở hữu trí tuệ của LLM

---

## Cảnh 3.0: Mở đầu Part 3 — Từ văn bản AI đến chính mô hình AI

Ở phần trước, chúng ta đã nói về **Text Watermark** — tức là nhúng một dấu hiệu vô hình vào chính văn bản do AI tạo ra.

Mục tiêu của Text Watermark là trả lời câu hỏi:

“Đoạn văn này có phải do AI sinh ra hay không?”

Nhưng trong thế giới AI thương mại, còn một câu hỏi khác nghiêm trọng hơn:

“Nếu một công ty bỏ ra hàng triệu đô để huấn luyện một mô hình mạnh, làm sao họ chứng minh được mô hình đó là tài sản trí tuệ của mình?”

Hay nói cách khác:

Nếu có người âm thầm sao chép mô hình, tinh chỉnh lại, đổi tên, rồi bán nó như một sản phẩm riêng, làm sao chủ sở hữu ban đầu có thể phát hiện?

Đó chính là vấn đề mà **Model Watermark** — hay thủy vân mô hình — cố gắng giải quyết.

Nếu Text Watermark bảo vệ **nội dung đầu ra**, thì Model Watermark bảo vệ **chính mô hình AI**.

---

## Cảnh 3.1: Bối cảnh — Vì sao mô hình AI cần được bảo vệ?

Một mô hình ngôn ngữ lớn không chỉ là một file phần mềm thông thường.

Đằng sau nó là dữ liệu huấn luyện khổng lồ, hạ tầng tính toán đắt đỏ, đội ngũ nghiên cứu, quá trình tinh chỉnh, đánh giá, căn chỉnh an toàn và tối ưu hóa trong nhiều tháng hoặc nhiều năm.

Vì vậy, một mô hình AI mạnh là một tài sản trí tuệ có giá trị rất lớn.

Nhưng khác với phần mềm truyền thống, mô hình AI có một điểm yếu đặc biệt:

Bạn không cần nhìn thấy mã nguồn hay trọng số bên trong để học theo nó.

Chỉ cần có quyền truy cập API, kẻ tấn công có thể gửi rất nhiều câu hỏi đến mô hình, thu thập câu trả lời, rồi dùng chính dữ liệu đó để huấn luyện một mô hình khác.

Mô hình mới có thể không giống hoàn toàn mô hình gốc, nhưng nó có thể học lại một phần hành vi, phong cách và năng lực của mô hình ban đầu.

Đây chính là một trong những lý do khiến **bảo vệ bản quyền mô hình AI** trở thành một bài toán rất quan trọng.

---

## Cảnh 3.2: Ba mối đe dọa lớn đối với IP của LLM

Trong thực tế, có nhiều cách để xâm phạm quyền sở hữu trí tuệ của mô hình AI.

Nhưng trong phần này, chúng ta tập trung vào ba nhóm tấn công quan trọng nhất.

### Mối đe dọa thứ nhất: Model Extraction và Distillation

Đầu tiên là **Model Extraction**, hay trích xuất mô hình.

Hãy tưởng tượng mô hình gốc là một giáo viên rất giỏi, nhưng được giấu kín bên trong một chiếc hộp đen.

Kẻ tấn công không biết trọng số, không biết kiến trúc, cũng không biết dữ liệu huấn luyện gốc.

Nhưng họ có thể liên tục đặt câu hỏi cho mô hình qua API.

Mỗi câu hỏi giống như một bài kiểm tra.

Mỗi câu trả lời là một mẩu kiến thức bị rò rỉ.

Sau hàng trăm nghìn, thậm chí hàng triệu lượt truy vấn, kẻ tấn công thu thập được một bộ dữ liệu mới gồm:

đầu vào là câu hỏi,

và đầu ra là câu trả lời của mô hình nạn nhân.

Sau đó, họ dùng bộ dữ liệu này để huấn luyện một mô hình khác.

Quá trình này được gọi là **distillation**, hay chưng cất mô hình.

Mục tiêu là tạo ra một “học sinh” có hành vi giống “giáo viên” ban đầu nhất có thể.

Vấn đề là: nếu không có cơ chế bảo vệ, mô hình học sinh này có thể trở thành một bản sao thương mại rất khó bị phát hiện.

---

### Mối đe dọa thứ hai: Fine-tuning

Mối đe dọa thứ hai là **Fine-tuning**, hay tinh chỉnh mô hình.

Trong trường hợp này, kẻ xâm phạm có thể có được một mô hình đã được huấn luyện trước, hoặc một mô hình bị rò rỉ.

Sau đó, họ tiếp tục huấn luyện nó trên một tập dữ liệu mới để thay đổi hành vi bên ngoài.

Mục đích của fine-tuning có thể là làm cho mô hình phù hợp với một miền ứng dụng cụ thể.

Nhưng nó cũng có thể được dùng để che giấu dấu vết sở hữu.

Ví dụ, nếu mô hình gốc có một số hành vi đặc trưng, sau khi fine-tuning, các hành vi này có thể bị làm yếu đi.

Mô hình vẫn giữ lại nhiều năng lực cốt lõi từ mô hình ban đầu, nhưng bề ngoài trông như một sản phẩm mới.

Điều này khiến việc chứng minh quyền sở hữu trở nên khó khăn hơn.

---

### Mối đe dọa thứ ba: Pruning kết hợp Fine-tuning

Mối đe dọa thứ ba là **Pruning & Fine-tuning**.

Pruning có nghĩa là cắt tỉa bớt các trọng số hoặc thành phần được cho là ít quan trọng trong mô hình.

Việc này thường được dùng để giảm kích thước mô hình, tăng tốc suy luận hoặc tối ưu tài nguyên triển khai.

Nhưng dưới góc nhìn bảo vệ bản quyền, pruning cũng có thể trở thành một cách để lẩn tránh phát hiện.

Sau khi cắt tỉa, kẻ tấn công có thể fine-tune lại mô hình để khôi phục hiệu năng.

Kết quả là mô hình mới có thể nhỏ hơn, khác đi về mặt cấu trúc, nhưng vẫn giữ lại nhiều năng lực được học từ mô hình gốc.

Ba mối đe dọa này cho thấy một điều:

Bảo vệ mô hình AI không thể chỉ dựa vào việc giữ bí mật mã nguồn.

Chúng ta cần những cơ chế có thể chứng minh nguồn gốc của mô hình, ngay cả khi nó đã bị sao chép, tinh chỉnh hoặc biến đổi.

Đó là lúc Model Watermark xuất hiện.

---

## Cảnh 3.3: Ý tưởng cốt lõi của Model Watermark

Model Watermark có thể hiểu đơn giản là việc nhúng một “dấu hiệu nhận dạng bí mật” vào mô hình AI.

Dấu hiệu này không nên làm giảm đáng kể chất lượng mô hình.

Người dùng bình thường không nên nhận ra sự khác biệt.

Nhưng khi cần kiểm tra quyền sở hữu, chủ mô hình có thể dùng một quy trình đặc biệt để xác minh:

“Mô hình tình nghi này có mang dấu vết của tôi hay không?”

Có nhiều cách để làm điều đó.

Một số phương pháp nhúng watermark vào **đầu ra xác suất** của mô hình.

Một số phương pháp nhúng vào **hành vi phản hồi trước các prompt đặc biệt**.

Một số phương pháp khác lại không cần nhúng watermark từ trước, mà kiểm tra sự tương đồng sâu bên trong cấu trúc nơ-ron.

Trong phần này, chúng ta sẽ đi qua ba hướng chính:

Một là chống trích xuất mô hình bằng watermark kháng distillation.

Hai là chống fine-tuning bằng dấu vân tay chỉ dẫn.

Và ba là hậu kiểm mô hình bằng framework như DeepJudge.

---

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

---

## Cảnh 3.10: Phòng thủ chống Fine-tuning — Instruction Fingerprinting

Bây giờ, hãy chuyển sang mối đe dọa thứ hai: fine-tuning.

Giả sử một mô hình đã bị sao chép.

Kẻ tấn công không chỉ dùng nó ngay lập tức.

Họ tiếp tục fine-tune mô hình trên dữ liệu mới.

Sau quá trình này, mô hình có thể thay đổi đáng kể ở bề ngoài.

Câu hỏi là:

Làm sao chủ sở hữu vẫn có thể nhận ra mô hình của mình?

Một hướng tiếp cận là **Instruction Fingerprinting**, hay dấu vân tay chỉ dẫn.

Thay vì nhúng watermark vào mọi đầu ra, phương pháp này tạo ra một tập các cặp đặc biệt:

Một bên là prompt kỳ dị hoặc hiếm gặp.

Bên còn lại là phản hồi đặc trưng mà chỉ mô hình đã được cấy dấu vân tay mới có xu hướng tạo ra.

Có thể hình dung như một mật khẩu bí mật.

Với người dùng bình thường, mô hình hoạt động như mọi mô hình khác.

Nhưng khi chủ sở hữu nhập một số câu lệnh kiểm tra đặc biệt, mô hình sẽ phản hồi theo một mẫu đã định.

Nếu một mô hình tình nghi cũng phản hồi đúng những mẫu này, đó là dấu hiệu cho thấy nó có liên hệ với mô hình gốc.

---

## Cảnh 3.11: Ba giai đoạn của Instruction Fingerprinting

Instruction Fingerprinting thường có thể được hiểu qua ba giai đoạn.

### Giai đoạn một: Fingerprint Injection

Đầu tiên là cấy dấu vân tay.

Chủ mô hình tạo ra một tập prompt đặc biệt và phản hồi đặc trưng.

Sau đó, mô hình được huấn luyện để ghi nhớ hoặc phản ứng ổn định với các cặp này.

Điểm quan trọng là tập fingerprint phải hiếm.

Nó không nên xuất hiện tự nhiên trong dữ liệu thông thường.

Nếu không, một mô hình khác cũng có thể tình cờ phản hồi giống vậy.

### Giai đoạn hai: User Fine-tuning

Sau đó, mô hình có thể được người dùng hoặc bên thứ ba fine-tune trên dữ liệu riêng.

Trong kịch bản hợp pháp, đây là điều bình thường.

Nhưng trong kịch bản xâm phạm IP, fine-tuning có thể được dùng để che giấu nguồn gốc mô hình.

Một fingerprint tốt cần đủ bền để không biến mất hoàn toàn sau fine-tuning.

### Giai đoạn ba: Ownership Verification

Cuối cùng là xác minh quyền sở hữu.

Chủ mô hình gửi các prompt fingerprint vào mô hình tình nghi.

Nếu mô hình phản hồi đúng với tỷ lệ cao, ta có thể tính một chỉ số gọi là **Fingerprint Success Rate**, hay FSR.

FSR càng cao, dấu hiệu mô hình tình nghi có liên quan đến mô hình gốc càng mạnh.

Tuy nhiên, FSR không nên được xem là bằng chứng duy nhất.

Nó là một tín hiệu kỹ thuật quan trọng, cần được kết hợp với các phân tích khác.

---

## Cảnh 3.12: SFT và Adapter trong Instruction Fingerprinting

Có nhiều cách để cấy fingerprint vào mô hình.

Một cách trực tiếp là dùng **Supervised Fine-tuning**, hay SFT.

Trong cách này, ta đưa các cặp prompt — response fingerprint vào quá trình fine-tuning của mô hình.

Ưu điểm là đơn giản và dễ hiểu.

Mô hình học trực tiếp cách phản hồi với các prompt đặc biệt.

Nhưng nhược điểm là nếu làm không cẩn thận, việc cấy fingerprint có thể ảnh hưởng đến năng lực tổng quát của mô hình.

Một hướng khác là dùng **Adapter**.

Adapter là các module nhỏ được gắn thêm vào mô hình.

Thay vì thay đổi toàn bộ trọng số, ta có thể huấn luyện các adapter để mang dấu vân tay.

Cách này có thể giúp giảm ảnh hưởng đến năng lực cốt lõi của mô hình.

Khi đánh giá các phương pháp này, ta thường quan tâm đến hai câu hỏi:

Một là fingerprint có còn tồn tại sau fine-tuning hay không?

Hai là mô hình có bị giảm hiệu năng trên các benchmark thông thường hay không?

Một phương pháp tốt phải đạt được cả hai:

Dấu vân tay đủ bền để xác minh quyền sở hữu.

Nhưng mô hình vẫn giữ được năng lực thực hiện nhiệm vụ chính.

---

## Cảnh 3.13: Khi không có watermark từ trước — DeepJudge

Tất cả các phương pháp trên đều có một giả định quan trọng:

Chủ sở hữu đã chủ động nhúng watermark hoặc fingerprint vào mô hình từ trước.

Nhưng nếu mô hình gốc không được watermark thì sao?

Nếu nghi ngờ một mô hình đã bị sao chép, nhưng trước đó ta không hề cài dấu vân tay, liệu còn cách nào để kiểm tra?

Đây là lúc các framework hậu kiểm như **DeepJudge** trở nên hữu ích.

DeepJudge không nhất thiết yêu cầu mô hình phải được cấy watermark từ trước.

Thay vào đó, nó cố gắng kiểm tra xem hai mô hình có quá giống nhau về hành vi và cấu trúc nơ-ron hay không.

Ý tưởng là:

Hai mô hình độc lập có thể cùng đạt độ chính xác cao trên một nhiệm vụ.

Nhưng nếu một mô hình được sao chép hoặc tái sử dụng từ mô hình khác, chúng có thể chia sẻ những điểm tương đồng sâu hơn trong cách phản ứng với dữ liệu.

DeepJudge tạo ra các test case đặc biệt và đo khoảng cách giữa mô hình gốc với mô hình tình nghi.

Nếu khoảng cách quá nhỏ trên nhiều tiêu chí, đó có thể là dấu hiệu của hành vi sao chép.

---

## Cảnh 3.14: Ba chỉ số trong DeepJudge

DeepJudge sử dụng nhiều loại khoảng cách để đánh giá sự tương đồng giữa hai mô hình.

### Chỉ số thứ nhất: Robustness Distance — RobD

Robustness Distance đo sự khác biệt về độ bền đối kháng của hai mô hình.

Nói đơn giản:

Nếu ta thay đổi nhẹ đầu vào, mô hình có còn giữ nguyên dự đoán hay không?

Hai mô hình có nguồn gốc gần nhau thường có thể phản ứng tương tự trước các nhiễu nhỏ hoặc các test case gần biên quyết định.

Nếu mô hình tình nghi có hành vi robustness rất giống mô hình gốc, đó là một tín hiệu đáng chú ý.

### Chỉ số thứ hai: Layer Output Distance — LOD

Layer Output Distance đo khoảng cách giữa đầu ra của các lớp ẩn.

Trong một mạng nơ-ron, kết quả cuối cùng không phải là thứ duy nhất quan trọng.

Trước khi đưa ra đáp án, mô hình tạo ra nhiều biểu diễn trung gian trong các lớp ẩn.

Nếu hai mô hình có biểu diễn ẩn rất giống nhau, chúng có thể đang xử lý thông tin theo cách tương tự.

Điều này đặc biệt hữu ích trong môi trường white-box, khi ta có quyền truy cập vào cấu trúc bên trong mô hình.

### Chỉ số thứ ba: Layer Activation Distance — LAD

Layer Activation Distance đo sự khác biệt trong mẫu kích hoạt của các nơ-ron.

Có thể hiểu đơn giản là:

Khi cùng nhìn thấy một đầu vào, những nơ-ron nào trong mô hình được kích hoạt?

Nếu hai mô hình có cùng kiểu kích hoạt trên nhiều test case, điều đó có thể cho thấy chúng có quan hệ gần gũi về mặt cấu trúc.

RobD nhìn vào độ bền hành vi.

LOD nhìn vào đầu ra lớp ẩn.

LAD nhìn vào mẫu kích hoạt nơ-ron.

Khi kết hợp lại, các chỉ số này tạo ra một bức tranh đầy đủ hơn về mức độ tương đồng giữa hai mô hình.

---

## Cảnh 3.15: Black-box, White-box và Majority Voting

DeepJudge có thể được hiểu qua hai môi trường kiểm thử.

Trong môi trường **black-box**, người kiểm tra chỉ có thể gửi đầu vào và quan sát đầu ra.

Đây là tình huống phổ biến khi mô hình tình nghi được triển khai dưới dạng API.

Ta không thấy trọng số.

Không thấy kiến trúc.

Không thấy lớp ẩn.

Chỉ thấy câu trả lời cuối cùng.

Trong môi trường **white-box**, người kiểm tra có quyền truy cập sâu hơn.

Có thể quan sát trọng số, lớp ẩn hoặc các biểu diễn trung gian.

Khi đó, việc so sánh cấu trúc nơ-ron có thể chi tiết hơn.

Sau khi thu thập các chỉ số khác nhau, hệ thống cần đưa ra phán quyết cuối cùng.

Một cách tiếp cận là **majority voting** — bỏ phiếu đa số.

Mỗi chỉ số đóng vai trò như một “thẩm phán” riêng.

Nếu phần lớn chỉ số cho thấy mô hình tình nghi quá giống mô hình gốc, hệ thống có thể kết luận rằng có khả năng tồn tại quan hệ sao chép hoặc tái sử dụng.

Tuy nhiên, cũng giống như watermarking, DeepJudge không nên được hiểu là chiếc máy phán quyết tuyệt đối.

Nó cung cấp một chuỗi bằng chứng kỹ thuật.

Phán quyết cuối cùng vẫn cần được đặt trong bối cảnh cụ thể, bao gồm dữ liệu huấn luyện, lịch sử truy cập, kiến trúc mô hình và các bằng chứng pháp lý khác.

---

## Cảnh 3.16: So sánh Text Watermark và Model Watermark

Đến đây, chúng ta cần phân biệt thật rõ hai khái niệm dễ bị nhầm lẫn:

**Text Watermark** và **Model Watermark**.

Text Watermark bảo vệ văn bản đầu ra.

Nó trả lời câu hỏi:

“Đoạn nội dung này có phải do AI tạo ra không?”

Trong khi đó, Model Watermark bảo vệ chính mô hình.

Nó trả lời câu hỏi:

“Mô hình này có phải được sao chép, chưng cất hoặc tinh chỉnh từ mô hình của tôi không?”

Về đối tượng bảo vệ:

Text Watermark bảo vệ từng đoạn văn bản.

Model Watermark bảo vệ tài sản mô hình.

Về mục tiêu:

Text Watermark phục vụ truy xuất nguồn gốc nội dung, phát hiện văn bản AI, hỗ trợ chống tin giả hoặc gian lận học thuật.

Model Watermark phục vụ bảo vệ sở hữu trí tuệ, phát hiện mô hình đạo nhái và hỗ trợ chứng minh hành vi sao chép.

Về vị trí can thiệp:

Text Watermark thường can thiệp vào quá trình sinh token để tạo ra một mẫu thống kê trong văn bản.

Model Watermark có thể can thiệp sâu hơn vào hành vi mô hình, phân phối xác suất, phản hồi với prompt đặc biệt hoặc cấu trúc nơ-ron.

Về kiểu tấn công cần chống chịu:

Text Watermark phải đối mặt với paraphrasing, dịch ngôn ngữ, cắt ngắn văn bản hoặc trộn với văn bản người viết.

Model Watermark phải đối mặt với model extraction, distillation, fine-tuning, pruning và các biến đổi mô hình khác.

Và về cách kiểm tra:

Text Watermark thường kiểm tra trực tiếp trên văn bản.

Model Watermark thường cần truy vấn mô hình tình nghi, phân tích hành vi đầu ra hoặc thậm chí kiểm tra cấu trúc bên trong mô hình nếu có quyền truy cập.

Nói ngắn gọn:

Text Watermark giống như đóng dấu vô hình lên từng sản phẩm được tạo ra.

Model Watermark giống như khắc một dấu vân tay bí mật vào chính nhà máy sản xuất ra những sản phẩm đó.

---

## Cảnh 3.17: Tổng kết Part 3

Trong phần này, chúng ta đã đi từ một câu hỏi rất thực tế:

Làm sao bảo vệ một mô hình AI khỏi bị sao chép?

Chúng ta đã thấy rằng các mô hình ngôn ngữ lớn có thể bị đe dọa bởi nhiều hình thức khác nhau:

Model extraction qua API.

Distillation để huấn luyện mô hình học sinh.

Fine-tuning để che giấu nguồn gốc.

Và pruning kết hợp fine-tuning để biến đổi cấu trúc mô hình.

Để phòng thủ, các nhà nghiên cứu đề xuất nhiều hướng tiếp cận.

DRW nhúng watermark vào phân phối xác suất để chống distillation.

GINSEW đưa tín hiệu vô hình vào quá trình sinh chuỗi của mô hình ngôn ngữ.

CATER dùng watermark có điều kiện để thay đổi lựa chọn từ một cách tinh tế.

Instruction Fingerprinting tạo ra các prompt và phản hồi đặc trưng để xác minh quyền sở hữu sau fine-tuning.

Và DeepJudge cung cấp một hướng hậu kiểm, đo sự tương đồng hành vi và cấu trúc giữa mô hình gốc và mô hình tình nghi.

Điểm quan trọng nhất là:

Model Watermark không phải là một phép màu tuyệt đối.

Nhưng nó là một lớp phòng thủ quan trọng trong hệ sinh thái AI hiện đại.

Khi các mô hình ngày càng đắt đỏ, mạnh mẽ và dễ bị sao chép qua API, việc bảo vệ quyền sở hữu trí tuệ không còn là vấn đề phụ.

Nó trở thành một phần cốt lõi của an toàn, minh bạch và công bằng trong thế giới AI tạo sinh.

Ở phần tiếp theo, chúng ta sẽ tổng kết toàn bộ chủ đề Watermarking cho LLMs, nhìn lại những điểm mạnh, giới hạn và các hướng nghiên cứu còn đang mở.
