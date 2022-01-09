import enum


class Candles(enum.Enum):
    strategy_id = 1
    engine = 2
    trigger_time = 3
    trigger_days = 4
    target_per = 5
    candle_size = 6
    stoploss_per = 7
    deep_stoploss_per = 8
    delayed_stoploss_min = 9
    stall_detect_period_min = 10
    trail_target_en = 11
    position_reversal_en = 12
