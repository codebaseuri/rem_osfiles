# server.py
import cv2
import numpy as np
import socket
import pickle
import struct
import mss

def start_server():
    # Socket Create
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host_name = socket.gethostname()
    host_ip = "0.0.0.0"
    print('HOST IP:', host_ip)
    port = 9999
    socket_address = (host_ip, port)

    # Socket Bind
    server_socket.bind(socket_address)

    # Socket Listen
    server_socket.listen(5)
    print("LISTENING AT:", socket_address)

    # Socket Accept
    while True:
        client_socket, addr = server_socket.accept()
        print('GOT CONNECTION FROM:', addr)
        if client_socket:
            sct = mss.mss()
            monitor = sct.monitors[1]  # Get primary monitor

            while True:
                try:
                    # Capture screen
                    screenshot = np.array(sct.grab(monitor))
                    
                    # Convert from BGRA (from mss) to BGR (for cv2)
                    frame = cv2.cvtColor(screenshot, cv2.COLOR_BGRA2BGR)
                    
                    # Resize frame if needed (adjust scale as needed)
                    scale_percent = 50  # percent of original size
                    width = int(frame.shape[1] * scale_percent / 100)
                    height = int(frame.shape[0] * scale_percent / 100)
                    frame = cv2.resize(frame, (width, height))
                    
                    # Compress frame
                    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
                    _, frame = cv2.imencode('.jpg', frame, encode_param)
                    
                    # Serialize frame
                    data = pickle.dumps(frame)
                    
                    # Send message length first
                    message_size = struct.pack("L", len(data))
                    client_socket.sendall(message_size + data)
                    
                except Exception as e:
                    print(f"ERROR: {e}")
                    break

        client_socket.close()

if __name__ == '__main__':
    start_server()

