import gymnasium as gym
from gymnasium import spaces

from cg.game import (
    battle_start,
    battle_select,
    battle_finish,
)

from .encoder import encode_obs
from .actions import (
    get_legal_actions,
    action_id_to_action,
)
from .reward import calculate_reward


class PokemonEnv(gym.Env):

    def __init__(self, deck1, deck2):
        super().__init__()

        self.deck1 = deck1
        self.deck2 = deck2

        # 実際の値はencoder完成後に決める
        self.observation_space = spaces.Box(
            low=0.0,
            high=1.0,
            shape=(OBS_SIZE,),
            dtype=float,
        )

        # とりあえず最大値
        self.action_space = spaces.Discrete(MAX_ACTIONS)

        self.obs_dict = None

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)

        self.obs_dict, _ = battle_start(
            self.deck1,
            self.deck2
        )

        obs = encode_obs(self.obs_dict)

        return obs, {}

    def step(self, action_id):

        action = action_id_to_action(
            self.obs_dict,
            action_id
        )

        self.obs_dict = battle_select(action)

        reward = calculate_reward(
            self.obs_dict
        )

        terminated = (
            self.obs_dict["current"]["result"] >= 0
        )

        truncated = False

        obs = encode_obs(
            self.obs_dict
        )

        if terminated:
            battle_finish()

        return (
            obs,
            reward,
            terminated,
            truncated,
            {}
        )