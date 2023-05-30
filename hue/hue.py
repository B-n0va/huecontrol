import requests
import socket
import struct
import sys
import socket
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QComboBox, QLabel, QListWidgetItem, QListWidget, QSlider, QAbstractItemView
from PyQt5.QtCore import Qt
from zeroconf import Zeroconf, ServiceBrowser, ServiceListener

BRIDGE_IP = None  # Declare the BRIDGE_IP variable

class HueBridgeListener(ServiceListener):
    def remove_service(self, zeroconf, type, name):
        print(f"Service {name} removed")

    def add_service(self, zeroconf, type, name):
        global BRIDGE_IP 
        info = zeroconf.get_service_info(type, name)
        if info:
            print(f"Discovered Hue Bridge: {name}")
            BRIDGE_IP = socket.inet_ntoa(info.addresses[0])  # Update the global variable
            print(f"Bridge IP: {BRIDGE_IP}")

listener = HueBridgeListener()

zeroconf = Zeroconf()
browser = ServiceBrowser(zeroconf, "_hue._tcp.local.", listener)

try:
    input("Press enter to exit...\n\n")
finally:
    zeroconf.close()
    print(f"Hue Bridge IP: {BRIDGE_IP}")  # Access the global variable



# IP addresses and respective keys
IP_Key = {
    # B
    "192.168.0.243": "MxEIabwJX75Cjepjds3mO0G0ppTkmBnYhbjL-ItF",
    # J
    "192.168.178.20": "HEZt6IcW8sSVSzB293OLrzvqPxv0Fk94S-uDXK8b"
}

# Function to convert an IP address to a numeric value
def ip2int(ip):
    packedIP = socket.inet_aton(ip)
    return struct.unpack("!L", packedIP)[0]

# Function to calculate the 'distance' between two IP addresses
def ip_distance(ip1, ip2):
    return abs(ip2int(ip1) - ip2int(ip2))


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

def get_devices(room_id):
    response = requests.get(get_hue_bridge_url(API_KEY) + "/lights")
    if response.status_code != 200:
        print(f"Failed to get devices: {response.status_code}, {response.text}")
        return {}

    devices = response.json()
    if not devices:
        print(f"No devices found for room_id: {room_id}")
        return {}

    device_names = {id: device['name'] for id, device in devices.items()}
    return device_names



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
        self.all_lights_on = True
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()

        self.room_label = QLabel('Select Room')
        self.room_combobox = QComboBox()
        self.device_label = QLabel('Devices in selected room')
        self.device_list = QListWidget()

        self.master_on_off_button = QPushButton("Master")
        self.on_button = QPushButton("On")
        self.off_button = QPushButton("Off")
        self.red_button = QPushButton("Red")
        self.green_button = QPushButton("Green")  # add more color buttons here
        self.brightness_slider = QSlider(Qt.Horizontal)
        self.brightness_slider.setMaximum(255)  # Hue brightness ranges from 0-255
        self.brightness_slider.setMinimum(0)

        self.layout.addWidget(self.room_label)
        self.layout.addWidget(self.room_combobox)

        self.layout.addWidget(self.device_label)
        self.layout.addWidget(self.device_list)
        self.layout.addWidget(self.master_on_off_button)
        self.layout.addWidget(self.on_button)
        self.layout.addWidget(self.off_button)
        self.layout.addWidget(self.red_button)
        self.layout.addWidget(self.green_button)
        self.layout.addWidget(self.brightness_slider)

        self.setLayout(self.layout)

        self.room_combobox.currentIndexChanged.connect(self.update_device_list)
        self.master_on_off_button.clicked.connect(self.master_on_off)
        self.on_button.clicked.connect(self.turn_selected_lights_on)
        self.off_button.clicked.connect(self.turn_selected_lights_off)
        self.red_button.clicked.connect(lambda: self.set_all_lights_color("red"))
        self.green_button.clicked.connect(lambda: self.set_all_lights_color("green"))  # update these for all color buttons
        self.brightness_slider.valueChanged.connect(self.set_all_lights_brightness)
        self.device_list.setSelectionMode(QAbstractItemView.MultiSelection)


    def populate_room_list(self, rooms):
        for room_id, room in rooms.items():
            self.room_combobox.addItem(room['name'], room_id)


    def update_device_list(self, index):
        self.device_list.clear()
        selected_room_id = self.room_combobox.itemData(index)
        devices = self.get_devices_in_room(selected_room_id)
        if devices:
            for device_id, device_name in devices.items():
                item = QListWidgetItem(device_name)
                item.setData(Qt.UserRole, device_id)  # Store the device id in the UserRole data field
                self.device_list.addItem(item)
        else:
            print("No devices found in selected room")




    def get_rooms(self):
        return get_rooms()

    def get_devices_in_room(self, room_id):
        rooms = self.get_rooms()
        if room_id in rooms:
            device_ids = rooms[room_id]['lights']
            all_devices = get_devices(room_id)
            devices = {id: all_devices[id] for id in device_ids if id in all_devices}
            return devices
        else:
            print(f"No devices found in room with id: {room_id}")
            return {}




    
    def master_on_off(self):
        rooms = self.get_rooms()
        for room in rooms.values():
            for device_id in room['lights']:
                turn_light_on_or_off(device_id, self.all_lights_on)
        self.all_lights_on = not self.all_lights_on
            

    def turn_selected_lights_on(self):
        selected_device_ids = self.get_selected_device_ids()
        rooms = self.get_rooms()
        for room in rooms.values():
            for device_id in room['lights']:
                if selected_device_ids is None or device_id in selected_device_ids:
                    turn_light_on_or_off(device_id, True)

    def turn_selected_lights_off(self):
        selected_device_ids = self.get_selected_device_ids()
        rooms = self.get_rooms()
        for room in rooms.values():
            for device_id in room['lights']:
                if selected_device_ids is None or device_id in selected_device_ids:
                    turn_light_on_or_off(device_id, False)


    def set_all_lights_color(self, color):
        selected_device_ids = self.get_selected_device_ids()
        rooms = self.get_rooms()
        for room in rooms.values():
            for device_id in room['lights']:
                if selected_device_ids is None or device_id in selected_device_ids:
                    set_light_color(device_id, color)

    def set_all_lights_brightness(self, brightness):
        selected_device_ids = self.get_selected_device_ids()
        rooms = self.get_rooms()
        for room in rooms.values():
            for device_id in room['lights']:
                if selected_device_ids is None or device_id in selected_device_ids:
                    set_light_brightness(device_id, brightness)
    
    def toggle_light(self, checked):
        device_id = self.get_selected_device_id()
        if device_id is not None:
            turn_light_on_or_off(device_id, checked)
            self.onoff_button.setText("On" if checked else "Off")

    def set_selected_light_color(self, color):
        device_id = self.get_selected_device_id()
        if device_id is not None:
            set_light_color(device_id, color)

    def set_selected_light_brightness(self, brightness):
        device_id = self.get_selected_device_id()
        if device_id is not None:
            set_light_brightness(device_id, brightness)

    def get_selected_device_ids(self):
        selected_devices = self.device_list.selectedItems()
        if selected_devices:
            return [device.data(Qt.UserRole) for device in selected_devices]  # Retrieve the device id from the UserRole data field
        else:
            print("No devices selected, applying action to all devices.")
            return None



    


def main():

    app = QApplication(sys.argv)
    hue_controller_interface = HueControllerInterface()
    hue_controller_interface.populate_room_list(get_rooms())
    hue_controller_interface.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
