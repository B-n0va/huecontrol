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

def turn_light_on_or_off(light_id, on):
    data = {"on": on}
    response = requests.put(get_hue_bridge_url(API_KEY) + f"/lights/{light_id}/state", json=data)
    return response.json()

def main():
    print("Rooms:")
    rooms = get_rooms()
    for room_id, room in rooms.items():
        print(f"{room_id}: {room['name']}")

    print("\nDevices:")
    devices = get_devices()
    for device_id, device in devices.items():
        print(f"{device_id}: {device['name']}")

    print("\nTurning lights on:")
    for device_id in devices.keys():
        result = turn_light_on_or_off(device_id, True)
        print(f"Light {device_id}: {result}")

    input("\nPress Enter to turn lights off...")

    print("\nTurning lights off:")
    for device_id in devices.keys():
        result = turn_light_on_or_off(device_id, False)
        print(f"Light {device_id}: {result}")

if __name__ == "__main__":
    main()
