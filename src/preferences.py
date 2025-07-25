import configparser

config_file_path = "../data/preferences.ini"


def save_preferences(config_file_path, preferences):
    config = configparser.ConfigParser()
    config["Preferences"] = preferences
    with open(config_file_path, "w") as configfile:
        config.write(configfile)
    print("Preferences saved!")


def load_preferences(file_path=config_file_path):
    config = configparser.ConfigParser()
    config.read(file_path)
    preferences = {
        "region_id": config.getint("Preferences", "region_id"),
        "station_id": config.getint("Preferences", "station_id"),
        "time": config.get("Preferences", "time"),
        "market_size": config.getint("Preferences", "market_size"),
        "market_volume": config.getint("Preferences", "market_volume"),
    }
    return preferences


def get_preference(key, file_path=config_file_path):
    config = configparser.ConfigParser()
    config.read(file_path)
    return config.get("Preferences", key)
