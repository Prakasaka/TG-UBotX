import dataclasses

@dataclasses.dataclass
class Blacklist:
    bio: list = None
    url: list = None
    tgid: list = None
    txt: list = None


@dataclasses.dataclass
class GlobalBlacklist:
    bio: list = None
    url: list = None
    tgid: list = None
    txt: list = None
