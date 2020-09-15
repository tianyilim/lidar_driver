import tkinter as tk

# Initialise window and frames
window = tk.Tk()
frame_main = tk.Frame(master=window)
frame_settings = tk.Frame(width=200, height=500, master=frame_main, bg="yellow")
frame_map = tk.Frame(width=500, master=frame_main, bg="green")
frame_diagnostic = tk.Frame(master=window, height=30, bg="blue")

# Pack frames in correct order
frame_settings.pack(fill=tk.Y, side=tk.RIGHT)
frame_map.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

frame_main.pack(fill=tk.BOTH, expand=True)
frame_diagnostic.pack(fill=tk.X, side=tk.BOTTOM)

# Build settings frames
frame_connect_status = tk.Frame(height=50, width=200, master=frame_settings, bg="grey")
frame_connect_status.pack(fill=tk.X, side=tk.TOP)
connected_text = tk.Label(text="CONNECTED", master=frame_connect_status)
connected_text.pack()

frame_serialport = tk.Frame(height=50, width=200, master=frame_settings, bg="cyan")
frame_serialport.pack(fill=tk.X, side=tk.TOP)
serialport_text = tk.Label(text="Serial Port", master=frame_serialport)
serialport_text.pack()

OPTIONS = {"chicken", "egg"}

variable = tk.StringVar(window)
variable.set("chicken")
serialport_optionsmenu = tk.OptionMenu(frame_serialport, variable, *OPTIONS)
serialport_optionsmenu.pack()

frame_baudrate = tk.Frame(height=50, width=200, master=frame_settings, bg="brown")
frame_baudrate.pack(fill=tk.X, side=tk.TOP)
baudrate_text = tk.Label(text="Baudrate", master=frame_baudrate)
baudrate_text.pack()

frame_connect_button = tk.Frame(height=50, width=200, master=frame_settings, bg="red")
frame_connect_button.pack(fill=tk.X, side=tk.BOTTOM)
connect_button = tk.Button(text="Connect", width=10, height=5, master=frame_connect_button)
connect_button.pack(side=tk.LEFT)
disconnect_button = tk.Button(text="Disconnect", width=10, height=5, master=frame_connect_button)
disconnect_button.pack(side=tk.LEFT)

# Build map frames
header = tk.Label(text="LIDAR visualisation v1.0", master=frame_map)
header.pack(fill=tk.X, side=tk.TOP)

def handle_connect(event):
    print(variable.get())
    connected_text["text"] = "CONNECTED"
    
def handle_disconnect(event):
    print("disconnected!")
    connected_text["text"] = "DISCONNECTED"

connect_button.bind("<Button-1>", handle_connect)
disconnect_button.bind("<Button-1>", handle_disconnect)

window.mainloop()

