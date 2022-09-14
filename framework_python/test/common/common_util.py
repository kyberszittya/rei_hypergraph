
import typing

def join_w_separator(l: typing.List[str], separator: str="") -> str:
    return separator.join(l)


def join_w_prefix_separator(l: typing.List[str], separator: str="", prefix=""):
    if len(prefix) == 0:
        return join_w_separator(l, separator)
    _s = [prefix]
    _s.extend([x for x in l])
    return separator.join(_s)