import subprocess
import re
import json

filename = "wifi-profiles.json"


def get_profile_names():
    command_output = subprocess.run(["netsh", "wlan", "show", "profiles"], capture_output=True).stdout.decode("cp1252")
    profile_names = [x[:-1] for x in re.findall("Tutti i profili utente {4}: (.*)", command_output)]
    return profile_names


def get_profiles(profile_names):
    profiles = []

    for name in profile_names:
        wifi_profile = {}
        profile_info = subprocess.run(["netsh", "wlan", "show", "profile", name],
                                      capture_output=True).stdout.decode("cp1252")
        if re.search("Chiave di sicurezza {6}: Assente", profile_info):
            continue
        else:
            wifi_profile["ssid"] = name
            profile_info_pass = subprocess.run(["netsh", "wlan", "show", "profile", name, "key=clear"],
                                               capture_output=True).stdout.decode("cp1252")
            password = re.search("Contenuto chiave {12}: (.*)", profile_info_pass)
            wifi_profile["password"] = password[1][:-1] if password else None
            profiles.append(wifi_profile)

    return profiles


def dump_profiles(profiles):
    with open(filename, "w") as f:
        json.dump(profiles, f, indent=4)
    print(f"Profiles dumped in '{filename}'")


if __name__ == "__main__":
    profile_names = get_profile_names()
    profiles = get_profiles(profile_names)
    if profiles:
        dump_profiles(profiles)
    else:
        print("Some error has occurred")
    input("\nClick any button to exit...")
