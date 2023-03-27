import requests
import json

API_KEY = "MxEIabwJX75Cjepjds3mO0G0ppTkmBnYhbjL-ItF"
BRIDGE_IP = "192.168.0.242"

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

def turn_light_on_or_off(light_id, on):
    state = {"on": on}
    return set_light_state(light_id, state)

def set_light_color(light_id, hue, saturation):
    state = {"hue": hue, "sat": saturation}
    return set_light_state(light_id, state)

def set_light_brightness(light_id, brightness):
    state = {"bri": brightness}
    return set_light_state(light_id, state)

def main():
    rooms = get_rooms()
    devices = get_devices()

    print("Rooms:")
    for room_id, room in rooms.items():
        print(f"{room_id}: {room['name']}")

    room_id = input("Select a room: ")
    while room_id not in rooms:
        print("Invalid room ID.")
        room_id = input("Select a room: ")

    print(f"\nDevices in {rooms[room_id]['name']} room:")
    room_devices = rooms[room_id]['lights']
    for device_id in room_devices:
        print(f"{device_id}: {devices[device_id]['name']}")

    device_id = input("Select a device: ")
    while device_id not in room_devices:
        print("Invalid device ID.")
        device_id = input("Select a device: ")

    print("\nCommands:")
    print("1. Turn on/off")
    print("2. Set color")
    print("3. Set brightness")

    command = input("Select a command (1-3): ")
    while command not in ("1", "2", "3"):
        print("Invalid command.")
        command = input("Select a command (1-3): ")

    if command == "1":
        on = input("Turn on (Y/N): ").upper() == "Y"
        turn_light_on_or_off(device_id, on)
    elif command == "2":
        hue = int(input("Hue (0-65535): "))
        saturation = int(input("Saturation (0-255): "))
        set_light_color(device_id, hue, saturation)
    elif command == "3":
        brightness = int(input("Brightness (0-255): "))
        set_light_brightness(device_id, brightness)

if __name__ == "__main__":
    main()
