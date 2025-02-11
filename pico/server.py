import network
import time
import socket
import _thread
import machine
from machine import Pin
import rp2

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
                        <div style="text-align: center;">
                                <h1> Haha avionics so cool poggerssssss</h1>
                                <h2>Time: {time}</h2>
                                <form action="./calibrate?">
                                        <button> Calibrate </button>
                                </form>
                                <form action="./record?">
                                        <button> Record </button>
                                </form>
                                <p>{data}</p>
                        </div>
                </body>
                </html>
                """
    return str(html)

def open_socket():
    # gets adress information for the socket, create a socket, bind it, then start listening for any clients trying to connect
    address = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    s = socket.socket()
    s.bind(address)
    s.listen(1)
    # then we will return this socket so we can use it in our main section
    return (s)

# if you do not see the network you may have to power cycle
# unplug your pico w for 10 seconds and plug it in again
def ap_mode(ssid, password, data):
    """
        Description: This is a function to activate AP mode
        
        Parameters:
        
        ssid[str]: The name of your internet connection
        password[str]: Password for your internet connection
        
        Returns: Nada
    """
    
    print("ah")
    
    # Debug
    pin = Pin("LED", Pin.OUT)
    country = "US"
    rp2.country(country)
    network.country(country)
    
    print("bahh")
    
    # Just making our internet connection
    ap = network.WLAN(network.AP_IF)
    ap.config(essid=ssid, password=password)
    ap.active(True)
    
    while ap.active() == False:
        print("Initialising access point...")
        time.sleep(1)
    print('AP Mode Is Active, You can Now Connect')
    print('IP Address To Connect to:: ' + ap.ifconfig()[0])
    
    s = open_socket()

    while True:
        conn, addr = s.accept()
        print('Got a connection from %s' % str(addr))

        request = conn.recv(1024)
        request = str(request)
        print('Content = %s' % request)

        # Extract Requests
        try:
            request = request.split()[1]
        except IndexError:
            pass
        print("Request: ", request)
        
        if request == "/calibrate?":
            print("Turned On!")
            pin.value(1)
        elif request == "/record?":
            print("Turned Off!")
            pin.value(0)

        t = time.localtime()
        current_time = "{:02}:{:02}:{:02}".format(t[3], t[4], t[5])
        response = web_page(current_time, data)
        conn.send("HTTP/1.1 200 OK\r\nContent-type: text/html\r\n\r\n")
        conn.send(response)
        conn.close()
      
      
""" Main Loop """

def main():
    ap_mode('john_pico', 'PASSWORD', 'data')

if __name__ == "__main__":
    main()