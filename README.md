# Python library for backtesting

### Ngày 1: Pipeline lấy và chuẩn hoá dữ liệu

* [x] Thiết lập repo, cấu trúc thư mục cơ bản.
* [x] Viết `data_pipeline/fetch_and_normalize.ipynb`:

  * [x] Hàm lấy dữ liệu từ **Finnhub** (`fetch_finnhub_data`) $\to$ Cancel do không có premium?.
  * [x] Hàm lấy dữ liệu từ **Twelve Data** (`fetch_twelvedata_data`).
  * [x] Hàm chuẩn hoá DataFrame về schema chung.
  * [x] Hàm lưu data vào `input/<symbol>_<interval>_<source>.csv`.
* [ ] Test nhanh với 1–2 symbol (VD: `AAPL`, `BTC/USD`) và commit.

### Ngày 2: Khung thư viện `btlib` + validation input

* [ ] Tạo skeleton modules cho `btlib`:

  * [ ] `btlib/data/__init__.py`
  * [ ] `btlib/data/loader.py`
  * [ ] `btlib/data/transforms.py`
  * [ ] `btlib/data/synthetic.py`
  * [ ] `btlib/core/strategy.py`
  * [ ] `btlib/core/engine.py`
  * [ ] `btlib/core/events.py`
  * [ ] `btlib/portfolio/…`, `btlib/execution/…`, `btlib/indicators/…`, `btlib/analytics/…`, `btlib/optimize/…`, `btlib/utils/…`
* [ ] Implement module **kiểm tra input** `btlib/data/validation.py`:

  * [ ] Hàm `validate_dataframe(df, strict=True/False)`:

    * [ ] Kiểm tra cột bắt buộc.
    * [ ] Kiểm tra parse `timestamp`.
    * [ ] Kiểm tra kiểu dữ liệu numeric cho `open/high/low/close/volume`.
    * [ ] Kiểm tra dữ liệu sắp xếp theo thời gian, duplicate, NaN, logic OHLC.
  * [ ] Hàm `validate_input_file(path, expected_source, expected_symbol, expected_interval, strict)`:

    * [ ] Load CSV và validate.
    * [ ] Kiểm tra khớp `source/symbol/interval`.
* [ ] Tích hợp validation vào pipeline:

  * [ ] Sau khi lưu `data.csv`, gọi `validate_input_file` để đảm bảo dữ liệu sạch.

### Ngày 3: Core backtest engine & portfolio cơ bản

* [ ] Thiết kế event model trong `btlib/core/events.py`:

  * [ ] `MarketEvent`, `SignalEvent`, `OrderEvent`, `FillEvent`.
* [ ] Implement base class `Strategy` trong `btlib/core/strategy.py`:

  * [ ] Các hook: `on_start`, `on_bar`, `on_end`.
* [ ] Implement `Backtest` engine cơ bản trong `btlib/core/engine.py`:

  * [ ] Vòng lặp qua nến (bars), phát `MarketEvent`.
  * [ ] Gọi strategy, nhận signal/order.
  * [ ] Gửi order qua broker giả lập.
* [ ] Implement tối thiểu:

  * [ ] `DefaultAccount` (cash, positions, PnL).
  * [ ] `DefaultBroker` (market order, execution đơn giản).
* [ ] Viết 1 ví dụ strategy đơn giản (VD: MA crossover) để smoke test.

### Ngày 4: Analytics & indicator cơ bản

* [ ] Implement các indicator basic trong `btlib/indicators/ta_basic.py`:

  * [ ] SMA, EMA.
  * [ ] RSI, MACD, Bollinger (cơ bản).
* [ ] Implement module `btlib/analytics/metrics.py`:

  * [ ] Tính total return, max drawdown, volatility.
  * [ ] Sharpe, Sortino, hit ratio, avg win/loss.
* [ ] Implement module `btlib/analytics/visualization.py`:

  * [ ] Vẽ equity curve.
  * [ ] Vẽ drawdown.
* [ ] Tạo 1 notebook hoặc script demo:

  * [ ] Load data từ `input/`.
  * [ ] Run strategy, in metrics + show chart.

### Ngày 5: Data editing / synthetic + tối ưu hoá cơ bản

* [ ] Module `btlib/data/transforms.py`:

  * [ ] Hàm filter thời gian, resample, fill missing.
  * [ ] Hàm chỉnh sửa dữ liệu: giảm giá X%, tăng volume, inject gap/crash.
* [ ] Module `btlib/data/synthetic.py`:

  * [ ] Hàm tạo chuỗi giá synthetic (random walk / GBM).
  * [ ] Hàm tạo scenario bull/bear, vol cao/thấp.
* [ ] Module `btlib/optimize/grid_search.py`:

  * [ ] Hàm chạy grid search các tham số strategy (MA fast/slow, threshold).
  * [ ] Lưu kết quả metrics & best params.
* [ ] Tổng hợp:

  * [ ] Viết thêm ví dụ backtest trên data synthetic.
  * [ ] Chạy thử grid search đơn giản (vd: tối ưu tham số MA).
  * [ ] Cập nhật README với ví dụ usage code cơ bản.

### Additional:
* [ ] Random walk mô phỏng sự sụt giảm 20%, tăng lên 15% trong thời gian 35 ngày
* [ ] Dùng websocket để backtest realtime
* [ ] Backtest thường bằng API