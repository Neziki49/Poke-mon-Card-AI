from stable_baselines3 import PPO

from env import PokemonEnv


env = PokemonEnv(
    deck1=load_deck("../decks/Dragapult/deck.csv"),
    deck2=load_deck("../decks/Dragapult/deck.csv")
)

model = PPO(
    "MlpPolicy",
    env,
    verbose=1,
)

model.learn(
    total_timesteps=1_000_000
)

model.save("pokemon_ai")