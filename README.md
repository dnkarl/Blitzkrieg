# Blitzkrieg
Dự án làm game cơ bản của nhóm Blitzkrieg thuộc lớp Tin-LN niên khoá 24-27 trường PTNK

**Giới thiệu**:
- Dự án làm game cơ bản của nhóm Blitzkrieg thuộc lớp Tin-LN niên khoá 24-27 trường PTNK
- Blitzkrieg là một trò chơi chiến thuật hành động, sinh tồn, thắng bại tại kĩ năng lấy cảm hứng từ các cuộc chiến tranh thế giới. Hai anh em ngồi trên hai xe tank khác nhau và bắn ra những cục kẹo đồng. Ai ăn trúng kẹo đồng sẽ thua.

**Cách chơi**:
1. Nhấn "Play Game".
2. Chọn chế độ:
   - **Ở chế độ PvP**:
     - P1: W - Lên, A - Trái, S - Xuống, D - Phải, R - Bắn
     - P2: UP - Lên, LEFT - Trái, DOWN - Xuống, RIGHT - Phải, \ - Bắn
   - **Ở chế độ PvE**: Người chơi sẽ đấu với AI (bot)
     - Có 3 độ khó, mỗi độ khó thể hiện trình độ "máy trí" khác nhau.
     - Các nút di chuyển và bắn tương tự P1 của chế độ PvP.
3. Nhập tên và thời gian chơi (đơn vị giây).
4. Cùng thưởng thức xem tình anh em có bền được lâu?

**Yêu cầu hệ thống**:
- Game chạy tốt nhất ở 120 FPS
- Hệ điều hành: Windows 7/8/10/11
- Dung lượng: ~30MB (file .exe)
- Không cần cài đặt Python hoặc Pygame, chỉ cần chạy file `Blitzkrieg.exe`
- Nếu máy tính của bạn có cảnh báo virus thì đừng lo. Đây là do quét hiểu nhầm, bạn hãy tắt Real-time protection khi chơi trò chơi hoặc vào Protection history và Restore lại Threat.

**Tính năng đặc biệt**:
Trong game có một tính năng đặc biệt khi bắn súng. Đây là tính năng và không phải bug.

**Phiên bản**:
Vì đây là phiên bản Beta 3.0.3, vui lòng liên hệ cho chúng mình khi bạn phát hiện ra những "con bọ" bay vào trò chơi này. Xin cảm ơn!

  Cập nhật
===========================

**Beta 1.0.1**: (18/02/2025)
  - By dnkarl:
    - Tạo giao diện người dùng trắng, xám, đen. 
    - Chỉ có 1 map.
    - Tank spawn tại hai vị trí góc phải trên cùng và góc trái dưới cùng.
    - Thêm Credits.
  - By tmh9:
    - Thêm cơ chế di chuyển và bắn đơn giản của xe tank.

**Beta 1.0.2**: (20/02/2025)
  - By dnkarl:
    - Thêm Tutorial.
    - Thêm Playtime.
    - Thêm nhạc nền.
    - Sửa lỗi nút ấn cố định, giờ đây khi ấn nút nào thì màn hình liên kết với nút đó mới xuất hiện
    - Sửa lỗi đạn bay xuyên một vài tường.
    - Map giờ đây có thể random.

**Beta 1.0.3**: (23/02/2025)
  - By dnkarl:
    - Sửa lỗi đạn bay khỏi khung hình và không bật lại.
    - Sửa độ dày của tường trong map.
    - Thêm Settings.
    - Thêm chỉnh âm lượng nhạc nền ở Music trong Settings.
    - Thêm phần nhập tên người chơi.
    - Thêm giới hạn đạn ( 10 ).
    - Thêm giới hạn thời gian tồn tại của đạn ( 10s )

**Beta 1.0.4**: (25/02/2025)
  - By dnkarl:
    - Sửa lỗi map không thông thoáng, khó đi.
    - Sửa lỗi font và TextBox của Tutorial.
    - Thêm 3 chế độ: Dễ, Vừa, Khó trong chế độ PvE (đấu với máy).
    - Thêm tốc độ xe tank và tốc độ đạn bay (người chơi có thể chỉnh sửa trong Settings, tối thiểu: 50 - tối đa: 600 pixels).
    - Thêm phần nhập thời gian chơi (đơn vị giây).
    - Thêm bảng tỉ số.
    - Thêm Time Left
    - Thêm nút Settings trong khi chơi.

**Beta 2.0.1**: (27/02/2025)
  - By dnkarl:
    - Sửa lỗi bảng tỉ số không vừa vặn, khó nhìn.
    - Sửa lỗi văn bản trong Tutorial tràn màn hình.
    - Nâng cấp giao diện người dùng.
    - Thêm README.txt
    - Thêm hình nền ở màn hình chính và ở map khi chơi.
    - Thêm màu cho các nút ấn.
    - Đổi màu chữ.
    - Thêm âm thanh click (người chơi có thể chỉnh âm lượng ở Sound Effect trong Settings).
    - Thêm màn hình chiến thắng sau khi hết thời gian chơi.
    - Thêm icon cho phần mềm .exe.

**Beta 2.0.2**: (02/03/2025)
  - By dnkarl:
    - Nâng cấp giao diện người dùng.
    - Sửa lỗi Time Left không tạm dừng (Pause) khi nhấn Settings.
    - Sửa lỗi không có nút ấn vẫn ấn được.
    - Đổi nhạc nền.
    - Làm mới màu sắc cho tank.
    - Thêm Update History (Chi tiết các bản cập nhật)
    - Thêm thanh cuộn văn bản cho Tutorial và Update History.
    
**Beta 3.0.1**: (04-05/03/2025)
  - By dnkarl:
    - Điều chỉnh nút bắn ở P1: R và ở P2: \ .
    - Sửa lỗi tên người chơi và thời gian đã nhập trước đó không xoá khi quay lại màn hình chính.
    - Sửa lỗi không thể dùng thanh cuộn để cuộn. Giờ đây không cần chuột hay touchpad, người chơi có thể nhấn giữ thanh cuộn để cuộn văn bản.
    - Sửa lỗi thời gian trong ô Time Left nếu quá dài sẽ bị tràn màn hình. Giờ đây đã được fit lại cho vừa màn hình.
    - Nâng cấp giao diện người dùng mượt hơn.
    - Nâng cấp giao diện Settings.
    - Nâng cấp thanh cuộn giờ đây có thể scroll văn bản bằng màn hình cảm ứng.
    - Nâng cấp map, mở rộng chiều rộng map.
    - Hạn chế hai tank spawn gần nhau ở đầu game.
    - Tên bây giờ có thể để trống.
    - Khi đang chơi, màn hình sẽ tự động chuyển qua Pause nếu con trỏ chuột không nằm trên màn hình chơi.
    - Giới hạn thời gian chơi tối đa là 1000000000s nếu người chơi không chọn inf (endless mode).
    - Thêm background vào chế độ PvE.
    - Thêm nút Main Menu trong Settings ở màn hình chơi.
    - Thêm tính năng triệu tiêu đạn (hai đạn đụng nhau sẽ biến mất).
    - Thêm hiệu ứng phát nổ, rung màn hình, nhấp nháy, làm chậm 2s khi xe tank trúng đạn.
    - Thêm âm thanh nổ, có thể được điều chỉnh ở Sound Effect trong Settings.
    - Thêm chỉnh sửa giới hạn đạn, thời gian reload đạn, thời gian tồn tại của đạn trên map 
(người chơi chỉnh sửa trong Settings).
  - Thêm không giới hạn đạn và không giới hạn thời gian tồn tại của đạn.
  - Thêm khi nhấn Esc ở trong trò chơi, màn hình PAUSE sẽ hiện lên, khi nhấn Esc ở những nơi khác sẽ quay lại màn hình trước.
  - Thêm khi nhấn Enter ở ô nhập tên sẽ qua ô tiếp theo rồi qua màn hình chơi.

**Beta 3.0.2**: (07-08/03/2025)
  - By dnkarl:
    - Sửa lỗi button không hoạt động.
    - Sửa lỗi cho phép hai tên trùng nhau.
    - Sửa lỗi endless mode không hoạt động.
    - Sửa lỗi hiệu ứng nhấp nháy, rung không hoạt động khi có xe tank bị nổ.
    - Sửa lỗi phím Esc và Enter không hoạt động đúng.
    - Nâng cấp đạn nhìn rõ hơn.
    - Thêm tính năng sẵn sàng để nhập cho ô Time mà không cần click vào khi người chơi tới màn hình nhập Time.
    - Thêm hiệu ứng khói khi xe tank di chuyển.
    - Thêm tính năng hai xe tank đụng nhau sẽ nổ (hoà).
    - (BETA) Thêm AI (Bot) cả 3 độ khó vào chế độ PvE (developed with python source code, currently in testing phase, by dnkarl)

**Beta 3.0.3**: (20-21/03/2025)  -- **Latest version**
  - By tmh9:
    - Nâng cấp cơ chế di chuyển của tank mượt hơn.
  - By dnkarl:
    - Thêm AI (Bot) vào chế độ PvE ở cả 3 độ khó.
  - By huy:
    - Thiết kế (de)buff xuất hiện ngẫu nhiên.
  - By phanlam
    - Thiết kế de(buff).
  
  Liên hệ
===========================
- Trường: PTNK
- Lớp: 10 Tin-LN
- Khoá 24-27
- Nhóm: 

|  Thành viên             | Username (Gitname) | ID     |
|:-----------------------:|:------------------:|:------:|
|  Trần Minh Hiếu         | tmh9               | 242309 |
|  Nguyễn Trương Ngọc Huy | huy                | 242310 | 
|  Đinh Nguyên Khoa       | dnkarl             | 242313 | 
|  Phan Khánh Lâm         | phanlam            | 242318 |

- Special thanks to:
  - Grok
  - ChatGPT
  - Copilot
  - Gemini

**Chú thích**:
Trò chơi này được phát triển với mục đích học tập và phi lợi nhuận. Mọi đóng góp hoặc cải tiến đều được hoan nghênh!

