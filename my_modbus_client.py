from pymodbus.client import ModbusTcpClient
myServerAddr = '192.168.0.10'
clickSw = {
    'red':10001,
    'yellow':10002,
    'green':10003,
    'blue':10004
}
clickLed = {
    'red':8193,
    'yellow':8194,
    'green':8195,
    'blue':8196
}

client = ModbusTcpClient(myServerAddr)
client.connect()

# Read LED indicators
for select in clickLed:
    result = client.read_coils(clickLed[select])
    print(f'{select}: {result.bits[0]}')

# Write to LED switches
for select in clickLed:
    client.write_coil(clickLed[select], False)

client.close()