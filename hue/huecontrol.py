# import requests
# import time

# # Hue Bridge API Key and IP
# API_KEY = "MxEIabwJX75Cjepjds3mO0G0ppTkmBnYhbjL-ItF"
# BRIDGE_IP = "192.168.0.242"

# # Base API URL
# BASE_URL = f"http://{BRIDGE_IP}/api/{API_KEY}"

# def get_all_lights():
#     response = requests.get(f"{BASE_URL}/lights")
#     response.raise_for_status()
#     return response.json()

# def toggle_light(light_id, on):
#     payload = {"on": on}
#     response = requests.put(f"{BASE_URL}/lights/{light_id}/state", json=payload)
#     response.raise_for_status()
#     return response.json()

# def main():
#     # Discover all lights
#     lights = get_all_lights()

#     # Turn on all lights
#     for light_id in lights.keys():
#         print(f"Turning on light {light_id}: {lights[light_id]['name']}")
#         toggle_light(light_id, True)

#     # Wait for 5 seconds
#     time.sleep(5)

#     # Turn off all lights
#     for light_id in lights.keys():
#         print(f"Turning off light {light_id}: {lights[light_id]['name']}")
#         toggle_light(light_id, False)

# if __name__ == "__main__":
#     main()
