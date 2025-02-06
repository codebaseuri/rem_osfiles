import cv2
import numpy as np
import socket
import pickle
import struct

def start_client():
    # Create socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host_ip = "127.0.0.1"  # Replace with your server's IP
    port = 9999
    client_socket.connect((host_ip, port))
    print("nigger")
    data = b""
    payload_size = struct.calcsize("L")

    while True:
        try:
            # Receive message size
            while len(data) < payload_size:
                data += client_socket.recv(4096)
            
            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack("L", packed_msg_size)[0]
            
            # Receive frame data
            while len(data) < msg_size:
                data += client_socket.recv(4096)
            
            frame_data = data[:msg_size]
            data = data[msg_size:]
            
            # Deserialize and display frame
            frame = pickle.loads(frame_data)
            frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
            cv2.imshow('Screen Share', frame)
            
            # Press 'q' to quit
            if cv2.waitKey(1) == ord('q'):
                break
                
        except Exception as e:
            print(f"ERROR: {e}")
            break
            
    client_socket.close()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    start_client()
    