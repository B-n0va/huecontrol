import requests
import json

API_KEY = "MxEIabwJX75Cjepjds3mO0G0ppTkmBnYhbjL-ItF"
BRIDGE_IP = "192.168.0.243"

COLORS = {
    "red": {"hue": 0, "sat": 254},
    "orange": {"hue": 10000, "sat": 254},
    "yellow": {"hue": 20000, "sat": 254},
    "green": {"hue": 30000, "sat": 254},
    "blue": {"hue": 45000, "sat": 254},
    "purple": {"hue": 55000, "sat": 254},
    "pink": {"hue": 62000, "sat": 254},
}

def get_hue_bridge_url(api_key):
    return f"http://{BRIDGE_IP}/api/{api_key}"

def get_rooms():
    response = requests.get(get_hue_bridge_url(API_KEY) + "/groups")
    return response.json()

def get_devices():
    response = requests.get(get_hue_bridge_url(API_KEY) + "/lights")
    return response.json()

def set_light_state(light_id, state):
    url = get_hue_bridge_url(API_KEY) + f"/lights/{light_id}/state"
    response = requests.put(url, json=state)
    return response.json()

def set_room_state(room_id, state):
    rooms = get_rooms()
    devices = get_devices()

    if room_id not in rooms:
        print("Invalid room ID.")
        return

    for device_id in rooms[room_id]['lights']:
        light_name = devices[device_id]['name']
        print(f"Setting {light_name} to state: {state}")
        set_light_state(device_id, state)


def turn_light_on_or_off(light_id, on):
    state = {"on": on}
    return set_light_state(light_id, state)

def set_light_color(light_id, color):
    if color in COLORS:
        hue = COLORS[color]["hue"]
        sat = COLORS[color]["sat"]
        state = {"hue": hue, "sat": sat}
        return set_light_state(light_id, state)
    else:
        print("Invalid color name.")

def set_light_brightness(light_id, brightness):
    state = {"bri": brightness}
    return set_light_state(light_id, state)

def main():
    rooms = get_rooms()
    devices = get_devices()

    while True:
        print("Rooms:")
        for room_id, room in rooms.items():
            print(f"{room_id}: {room['name']}")

        room_id = input("Select a room (or type 'exit' to quit): ")
        if room_id == 'exit':
            break
        elif room_id not in rooms:
            print("Invalid room ID.")
            continue

        print(f"\nDevices in {rooms[room_id]['name']} room:")
        room_devices = rooms[room_id]['lights']
        for device_id in room_devices:
            print(f"{device_id}: {devices[device_id]['name']}")

        device_id = None  # Set to None initially
        while True:
            print("\nCommands:")
            print("1. Turn on/off")
            print("2. Set color")
            print("3. Set brightness")
            print("4. Set all lights in room")
            print("5. Select another device")
            print("6. Select another room")

            command = input("Select a command (1-6): ")
            if command not in ("1", "2", "3", "4", "5", "6"):
                print("Invalid command.")
                continue
            elif command == "1":
                if device_id is not None:
                    on = input("Turn on (Y/N): ").upper() == "Y"
                    turn_light_on_or_off(device_id, on)
                else:
                    print("No device selected.")
            elif command == "2":
                if device_id is not None:
                    color = input("Color (red, orange, yellow, green, blue, purple, pink): ")
                    set_light_color(device_id, color)
                else:
                    print("No device selected.")
            elif command == "3":
                if device_id is not None:
                    brightness = int(input("Brightness (0-255): "))
                    set_light_brightness(device_id, brightness)
                else:
                    print("No device selected.")
            elif command == "4":
                state = {}
                on = input("Turn on all lights (Y/N): ").upper() == "Y"
                state['on'] = on
                color = input("Color (red, orange, yellow, green, blue, purple, pink): ")
                if color in COLORS:
                    hue = COLORS[color]["hue"]
                    sat = COLORS[color]["sat"]
                    state['hue'] = hue
                    state['sat'] = sat
                else:
                    print("Invalid color name.")
                brightness = int(input("Brightness (0-255): "))
                state['bri'] = brightness
                set_room_state(room_id, state)
                device_id = None  # Set to None after influencing all lights in a room
            elif command == "5":
                device_id = input("Select a device: ")
                if device_id not in room_devices:
                    print("Invalid device ID.")
                    device_id = None
                    
            elif command == "6":
                break




if __name__ == "__main__":
    main()


