from mystring import string_util


def get_match_result(host_goals, visiting_goals):
    match_result = ""
    if string_util.is_any_blank(host_goals,
                                visiting_goals) or not host_goals.isdigit() or not visiting_goals.isdigit():
        return match_result

    host_goals_int = int(host_goals)
    visiting_goals_int = int(visiting_goals)
    if (host_goals_int > visiting_goals_int):
        match_result = "胜"
    elif (host_goals_int == visiting_goals_int):
        match_result = "平"
    elif (host_goals_int < visiting_goals_int):
        match_result = "负"
    return match_result
