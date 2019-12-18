def find_range(score_details, score):
    df = score_details[(score_details.SCORE_MIN <= score) & (score <= score_details.SCORE_MAX)]
    return df.SCORE_TEXT.values[0]


def find_color(score_details, score):
    df = score_details[(score_details.SCORE_MIN <= score) & (score <= score_details.SCORE_MAX)]
    return level_color[df.SCORE_LEVEL.values[0]]


level_color = {"H": "bg-success", "M": "bg-warning", "L": "bg-danger"}


def get_color_by_condition(range, score_text, score_color):
    return score_color if range == score_text else ''
