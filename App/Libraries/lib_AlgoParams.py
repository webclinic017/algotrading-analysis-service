import enum


class AlgoParam(enum.Enum):
    strategy_id = 0
    strategy_en = strategy_id + 1
    engine = strategy_en + 1
    trigger_time = engine + 1
    trigger_days = trigger_time + 1
    target_per = trigger_days + 1
    candle_size = target_per + 1
    stoploss_per = candle_size + 1
    deep_stoploss_per = stoploss_per + 1
    delayed_stoploss_min = deep_stoploss_per + 1
    stall_detect_period_min = delayed_stoploss_min + 1
    trail_target_en = stall_detect_period_min + 1
    position_reversal_en = trail_target_en + 1
