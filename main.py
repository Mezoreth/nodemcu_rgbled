import socket
import machine

ADDR = ('', 80)

PIN_R = 12
PIN_G = 14
PIN_B = 13

def web_page():
  f = open('index.html')
  html = str(f.read())
  f.close()
  return html

class RGBLed:
    def __init__(self, pin_r, pin_g, pin_b):
        self.pin_r = machine.PWM(machine.Pin(pin_r))
        self.pin_g = machine.PWM(machine.Pin(pin_g))
        self.pin_b = machine.PWM(machine.Pin(pin_b))
        self.set(0, 0, 0)

    def set(self, r, g, b):
        self.r = int(r)
        self.g = int(g)
        self.b = int(b)
        self.duty()

    def duty(self):
        self.pin_r.duty(self.duty_translate(self.r))
        self.pin_g.duty(self.duty_translate(self.g))
        self.pin_b.duty(self.duty_translate(self.b))

    def duty_translate(self, n):
        """translate values from 0-255 to 0-1023"""
        return int((float(n) / 255) * 1023)


def get_url(conn):
    conn_file = conn.makefile('rb', 0)
    method, url = None, None
    while True:
        line = conn_file.readline().decode()
        if not line or line == '\r\n':
            break
        if line.startswith('GET'):
            method, url, _ = line.split()
    return method, url

def parse_url(url):
    try:
        path, query = url.split('?', 2)
    except:
        return url, {}
    return path, {_.split('=')[0]: _.split('=')[1] for _ in query.split('&')}

led = RGBLed(PIN_R, PIN_G, PIN_B)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(ADDR)
s.listen(5)

print('RGBLamp daemon started on %s:%s' % ADDR)

while True:
  conn, addr = s.accept()
  print('Got a connection from %s' % str(addr))
  #request = conn.recv(1024)
  print('request aceptada')
  #request = str(request)
  
  method, url = get_url(conn)
  path, query = parse_url(url)
  print(addr[0], '-', method, url)
  print('path = '+str(path))
  print('query = '+str(query.get('r', 0)))
  response = web_page()
  conn.send('HTTP/1.1 200 OK\n')
  conn.send('Content-Type: text/html\n')
  conn.send('Connection: close\n\n')
  if path == '/':
    led.set(query.get('r', 0), query.get('g', 0), query.get('b', 0))
    conn.sendall(response)
  conn.close()


