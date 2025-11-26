# Python library for backtesting

- btlib
  - .data
    - .loader
      - `load_price(path, start, end) -> df`
    - .synthetic
      - `generate_random_walk(start_price, n, mu, sigma, freq, freq, seed, start) -> df`
      - `generate_gbm(start_price, n, mu, sigma, dt, freq, seed, start) -> df`: Geometric Brownian Motion path
    - .transforms
    - .validation
      - `validate_dataframe(df, strict: bool) -> report`
      - `validate_input_file(path, strict: bool) -> report`
  - .core
    - .engine
      - `BlacktestResult: equity_curve, account_history, trades, account`
      - `Backtest: data, symbol, strategy_class, account, broker, _equity_records, _account_snapshots`
        - `run() -> BacktestResult`
    - .events
      - `MarketEvent: timestamp, data`
      - `SignalEvent: timestamp, symbol, side, size`
      - `FillEvent: timestamp, symbol, side, size, price, commission`
    - .strategy
      - `Strategy: data, symbol, i, params: kwargs`: @abstractclass
        - `on_start()`
        - `on_bar()`
        - `on_end()`
        - `current_bar()`
        - `current_time()`
        - `buy(size) -> SignalEvent`
        - `sell(size) -> SignalEvent`
  - .execution
    - .fees
      - `fixed_commission(amount, commission) -> float`
      - `proportion_commission(amount, rate, min_commission) -> float`
    - .orders
      - `OrderSide: @enum`
      - `Order: timestamp, symbol, side, size`
    - .slippage
      - `apply_slippage_bps(price, side, slippage_bps) -> price`
  - .indicators
    - .basic
      - `sma(series, window) -> series`
      - `ema(series, window) -> series`
      - `rsi(series, window) -> series`
      - `macd(series, fast, slow, signal) -> macd_line, signal_line, hist`
      - `bollinger_bands(series, window, num_std) -> ma, upper, lower`
  - .optimize
  - .portfolio
    - .account
      - `Position: symbol, size, avg_price`
      - `Trade: timestamp, symbol, side, size, price, commission`
      - `AccountState: cash, positions, trades`
        - `update_fill(symbol, side, size, price, commission)`
        - `total_value(prices) -> float`
    - .broker
      - `Broker: account, slippage_bps, commission_rate`
        - `process_order(order, current_price, timestamp) -> FillEvent`
    - .risk
      - `fixed_fraction_position_size(equity, fraction, price) -> float`
  - .analytics
    - .metrics
      - `compute_basic_metrics(equity_curve, risk_free_rate) -> {return, avg_return, vol, sharpe, max_dd}`
    - .visualization
      - `plot_equity_curve(equity_curve)`
      - `plot_drawdown(equity_curve)`

### Additional:
* [ ] Random walk mô phỏng sự sụt giảm 20%, tăng lên 15% trong thời gian 35 ngày
* [ ] Dùng websocket để backtest realtime
* [ ] Backtest thường bằng API
* [ ] Hàm filter thời gian, resample, fill missing.
* [ ] Hàm chỉnh sửa dữ liệu: giảm giá X%, tăng volume, inject gap/crash.
* [ ] Hàm chạy grid search các tham số strategy (MA fast/slow, threshold).