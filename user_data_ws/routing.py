from . import consumers

user_data_routing = [
    consumers.UserInfo.as_route(),
]