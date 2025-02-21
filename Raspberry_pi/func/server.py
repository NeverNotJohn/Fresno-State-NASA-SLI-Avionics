import socket
import threading
import time

import helper

def web_page(time, data):
    html = f"""
                <!DOCTYPE html>
                <html lang="en">
                <head>
                        <meta charset="UTF-8">
                        <meta name="viewport" content="width=device-width, initial-scale=1.0">
                        <title>Centered Button</title>
                        <style>
                                body {{
                                        display: flex;
                                        justify-content: center;
                                        align-items: center;
                                        height: 100vh;
                                        margin: 0;
                                }}
                                button {{
                                        padding: 50px 100px;
                                        font-size: 35px;
                                }}
                        </style>
                </head>
                <body>
                        <h3>{data}</h3>
                        <div style="text-align: center;">
                                <h1> Haha avionics so cool poggerssssss</h1>
                                <h2>Time: {time}</h2>
                                <form action="./calibrate?">
                                        <button> Calibrate </button>
                                </form>
                                <form action="./record?">
                                        <button> Record </button>
                                </form>
                        </div>
                </body>
                </html>
                """
    return str(html)



def start_website(data):
    
    # Start Server
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)          # AF_INET: IPv4, SOCK_STREAM: TCP
    server.bind(('0.0.0.0', 8000))                                               # Bind Socket to LocalHost and Port 80
    server.listen()
    
    # Wait for a connection
    while True:
        print("Waiting for connection...")  # debug
        ip_address = server.getsockname()[0]
        print(f"Connect to http://{ip_address}:8000")
        client, addr = server.accept()
        print(f"Connection from {addr}")
        
        request = client.recv(1024).decode()  # Receive the request
        request = str(request)
        print(f"Request: {request}")
        
        # Extract Request
        try:
            request = request.split()[1]
        except IndexError:
            pass
        print(f"Extracted Request: {request}")
        
        if request == "/calibrate?":
            print("Calibrating!")
            
            # Actually Calibrate
            helper.calibrate()
            
            data = "!!!Calibrated!!!"
            
        elif request == "/record?":
            print("Recording!")
            data = "Recording!"
        else:
            pass
        
        t = time.localtime()
        current_time = "{:02}:{:02}:{:02}".format(t[3], t[4], t[5])
        response = web_page(current_time, data)
        
        # Send Webpage
        client.send("HTTP/1.1 200 OK\r\nContent-type: text/html\r\n\r\n".encode('utf-8'))
        client.send(response.encode('utf-8'))
        client.close()
        
def main():
    
    server_thread = threading.Thread(target=start_website, args=("This is a test",))
    server_thread.start()
    
    while True:
        print("Doing stuff!")
        time.sleep(10)
        
if __name__ == "__main__":
    main()