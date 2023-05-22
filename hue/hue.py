import requests
import socket
import struct
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QComboBox, QLabel, QListView, QListWidgetItem, QListWidget
from PyQt5.QtCore import Qt

# Function to convert an IP address to a numeric value
def ip2int(ip):
    packedIP = socket.inet_aton(ip)
    return struct.unpack("!L", packedIP)[0]

# Function to calculate the 'distance' between two IP addresses
def ip_distance(ip1, ip2):
    return abs(ip2int(ip1) - ip2int(ip2))

def discover_bridge_ip():
    response = requests.get("https://discovery.meethue.com")
    bridge_data = response.json()

    if len(bridge_data) > 0:
        return bridge_data[0]["internalipaddress"]
    else:
        return None

# IP addresses and respective keys
IP_Key = {
    # B
    "192.168.0.243": "MxEIabwJX75Cjepjds3mO0G0ppTkmBnYhbjL-ItF",
    # J
    "192.168.178.20": "HEZt6IcW8sSVSzB293OLrzvqPxv0Fk94S-uDXK8b"
}

# Discover bridge IP
BRIDGE_IP = discover_bridge_ip()

# If bridge IP is discovered, calculate distances and assign key
if BRIDGE_IP is not None:
    # Calculate distances
    distances = {ip: ip_distance(BRIDGE_IP, ip) for ip in IP_Key.keys()}

    # Get IP with minimal distance
    closest_IP = min(distances, key=distances.get)

    # Assign respective key
    API_KEY = IP_Key[closest_IP]

    print(f"Discovered IP: {BRIDGE_IP}\nClosest IP: {closest_IP}\nAssigned API_KEY: {API_KEY}")

else:
    print("No bridge IP discovered")
    # Default values if no bridge IP is discovered
    BRIDGE_IP = "192.168.0.243"
    API_KEY = IP_Key[BRIDGE_IP]

# API_KEY = "MxEIabwJX75Cjepjds3mO0G0ppTkmBnYhbjL-ItF"
# BRIDGE_IP = "192.168.0.243"

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


class HueControllerInterface(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()

        self.room_label = QLabel('Select Room')
        self.room_combobox = QComboBox()

        self.device_label = QLabel('Devices in selected room')
        self.device_list = QListWidget()

        self.layout.addWidget(self.room_label)
        self.layout.addWidget(self.room_combobox)

        self.layout.addWidget(self.device_label)
        self.layout.addWidget(self.device_list)

        self.setLayout(self.layout)

        self.room_combobox.currentIndexChanged.connect(self.update_device_list)

    def populate_room_list(self, rooms):
        for room_id, room in rooms.items():
            self.room_combobox.addItem(room['name'], room_id)

    def update_device_list(self, index):
        selected_room_id = self.room_combobox.itemData(index)
        devices = self.get_devices_in_room(selected_room_id)
        self.device_list.clear()
        for device_id, device_name in devices.items():
            self.device_list.addItem(QListWidgetItem(device_name))

    def get_rooms(self):
        return get_rooms()
    

    def get_devices_in_room(self, room_id):
        return get_devices(room_id)
        

def main():
    global BRIDGE_IP
    discovered_ip = discover_bridge_ip()

    if discovered_ip is not None:
        BRIDGE_IP = discovered_ip
    else:
        print("Could not find Hue Bridge on the network.")
        BRIDGE_IP = "192.168.0.243"

    app = QApplication(sys.argv)
    hue_controller_interface = HueControllerInterface()
    hue_controller_interface.populate_room_list(get_rooms())
    hue_controller_interface.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
