import json
import random
import sys
from cg.game import battle_start, battle_finish, battle_select, visualize_data
sys.path.append("./")
import submit
def random_agent(obs_dict: dict) -> list[int]:
    return random.sample(list(range(len(obs_dict["select"]["option"]))), obs_dict["select"]["maxCount"])

def load_deck(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return [int(line.strip()) for line in f if line.strip()]
    
deck1 = submit.my_deck
deck2 = load_deck("../decks/Dragapult/deck.csv")

obs_dict, _ = battle_start(deck1, deck2)
obs_log = [""]
action_log = [None]
print(json.dumps(obs_dict, indent=2, ensure_ascii=False))
while True:
    if obs_dict["current"]["result"] >= 0:
        break
    action = submit.agent(obs_dict)
    obs_dict.pop("search_begin_input")
    obs_log.append(obs_dict)
    action_log.append(action)
    obs_dict = battle_select(action)

vis = json.loads(visualize_data())
for i in range(len(vis)):
    vis[i]["obs"] = obs_log[i]
    vis[i]["action"] = [action_log[i], action_log[i]]
with open("vis.json", "w") as file:
    json.dump(vis, file)

battle_finish()