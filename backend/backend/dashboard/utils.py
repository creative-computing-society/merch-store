def get_for_user_positions(position):
    if position == "user":
        return ["user", "member", "core", "exbo"]
    elif position == "member":
        return ["member", "core", "exbo"]
    elif position == "core":
        return ["core", "exbo"]
    elif position == "exbo":
        return ["exbo"]
    return []