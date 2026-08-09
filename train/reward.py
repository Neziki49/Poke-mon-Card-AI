def calculate_reward(obs_dict, previous_obs=None):
    result = obs_dict["current"]["result"]

    # まだ試合中
    if result < 0:
        return 0.0

    # 勝利
    if result == 1:
        return 1.0

    # 敗北
    if result == 0:
        return -1.0

    return 0.0