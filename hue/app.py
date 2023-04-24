import tkinter as tk
from tkinter import ttk

class HueControllerApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Hue Controller")
        self.geometry("500x300")

        # Create and grid the main container
        main_frame = ttk.Frame(self)
        main_frame.grid(column=0, row=0, padx=10, pady=10)

        # Create and grid the color buttons
        self.color_buttons = {}
        for idx, (color, _) in enumerate(COLORS.items()):
            button = ttk.Button(main_frame, text=color.capitalize(), command=lambda col=color: self.set_color(col))
            button.grid(column=idx % 3, row=idx // 3, padx=5, pady=5)
            self.color_buttons[color] = button

        # Create and grid the brightness scale
        self.brightness_scale = ttk.Scale(main_frame, from_=0, to=255, orient='horizontal', command=self.set_brightness)
        self.brightness_scale.grid(column=3, row=0, rowspan=3, padx=10)

        # Create and grid the on/off button
        self.on_off_button = ttk.Button(main_frame, text="On/Off", command=self.toggle_on_off)
        self.on_off_button.grid(column=4, row=1, padx=5, pady=5)

    def set_color(self, color):
        # Add code here to set the color using your existing function
        print(f"Setting color: {color}")

    def set_brightness(self, brightness):
        # Add code here to set the brightness using your existing function
        print(f"Setting brightness: {brightness}")

    def toggle_on_off(self):
        # Add code here to toggle the light on or off using your existing function
        print("Toggling on/off")

if __name__ == "__main__":
    app = HueControllerApp()
    app.mainloop()
