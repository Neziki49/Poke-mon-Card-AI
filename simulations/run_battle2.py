import json
import sys

from cg.game import battle_start, battle_finish, battle_select, visualize_data

# =========================
# AIを読み込む
# =========================

# MCTS + NN
import submit

# ルールベースAI
# ここは実際のmain.pyの場所に合わせてください
sys.path.append("../decks/Dragapult/")
import main as rule_ai


# =========================
# デッキ
# =========================

# Player 0 : MCTS
deck1 = submit.my_deck

# Player 1 : ルールベース
deck2 = rule_ai.my_deck


# =========================
# バトル開始
# =========================

obs_dict, _ = battle_start(deck1, deck2)

obs_log = [""]
action_log = [None]

print("================================")
print("MCTS vs Rule-Based")
print("Player 0 : MCTS + Neural Network")
print("Player 1 : Dragapult Rule-Based")
print("================================")


# =========================
# バトルループ
# =========================

while True:

    # 試合終了
    if obs_dict["current"]["result"] >= 0:
        break

    # 現在行動するプレイヤー
    player_index = obs_dict["current"]["yourIndex"]

    # -------------------------
    # Player 0 = MCTS
    # -------------------------
    if player_index == 0:
        action = submit.agent(obs_dict)

        print(
            f"[Player 0 / MCTS] "
            f"action = {action}"
        )

    # -------------------------
    # Player 1 = Rule-Based
    # -------------------------
    else:
        action = rule_ai.agent(obs_dict)

        print(
            f"[Player 1 / Rule] "
            f"action = {action}"
        )

    # MCTSのsearch_begin_inputは
    # battle_select後には不要なのでログ保存前に削除
    if "search_begin_input" in obs_dict:
        obs_dict.pop("search_begin_input")

    # 観測と行動を保存
    obs_log.append(obs_dict)
    action_log.append(action)

    # 行動実行
    obs_dict = battle_select(action)


# =========================
# 試合結果
# =========================

result = obs_dict["current"]["result"]

print()
print("================================")
print("Battle Finished")
print(f"Result = {result}")

if result == 0:
    print("Winner : Player 0 (MCTS)")
elif result == 1:
    print("Winner : Player 1 (Rule-Based)")
elif result == 2:
    print("Result : Draw")

print("================================")


# =========================
# リプレイデータ作成
# =========================

vis = json.loads(visualize_data())

for i in range(len(vis)):
    if i < len(obs_log):
        vis[i]["obs"] = obs_log[i]

    if i < len(action_log):
        vis[i]["action"] = [
            action_log[i],
            action_log[i]
        ]


# =========================
# vis.jsonに保存
# =========================

with open("vis.json", "w", encoding="utf-8") as file:
    json.dump(
        vis,
        file,
        ensure_ascii=False,
        indent=2
    )

print()
print("Replay data saved to vis.json")


# =========================
# バトル終了処理
# =========================

battle_finish()