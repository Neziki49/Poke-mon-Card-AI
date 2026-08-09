import itertools


def get_legal_actions(obs_dict):
    options = obs_dict["select"]["option"]
    max_count = obs_dict["select"]["maxCount"]

    actions = []

    for count in range(1, max_count + 1):
        for indexes in itertools.combinations(
            range(len(options)),
            count
        ):
            actions.append(list(indexes))

    return actions


def action_id_to_action(obs_dict, action_id):
    actions = get_legal_actions(obs_dict)

    if action_id >= len(actions):
        raise ValueError(
            f"Invalid action: {action_id}"
        )

    return actions[action_id]