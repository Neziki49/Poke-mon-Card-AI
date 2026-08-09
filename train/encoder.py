import numpy as np


def encode_obs(obs_dict):
    """
    ゲームの状態をニューラルネットに入力できる
    1次元の数値配列に変換する。
    """

    features = []

    # 例：
    # features.append(...)
    # features.append(...)

    return np.array(features, dtype=np.float32)

CARD_COUNT = 300

def encode_card(card_id):
    result = np.zeros(CARD_COUNT, dtype=np.float32)
    result[card_id] = 1.0
    return result