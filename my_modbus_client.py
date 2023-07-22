from pymodbus.client import ModbusTcpClient

# Constants
myServerAddr = '192.168.0.10'
clickSw = {
    'red':10001,
    'yellow':10002,
    'green':10003,
    'blue':10004
}
clickLed = {
    'red':8192,
    'yellow':8193,
    'green':8194,
    'blue':8195
}


if __name__ == '__main__':
    myState = {
        'red':False,
        'yellow':False,
        'green':False,
        'blue':False
    }
    myLastState = myState.copy()

    # Connect to modbus server
    client = ModbusTcpClient(myServerAddr)
    client.connect()

    # Write to LED switches
    for select in clickLed:
        client.write_coil(clickLed[select], False)

    Loopy = True
    print('Press <Ctrl-C> to end')
    while Loopy:
        try:
            # Read LED indicators
            for select in clickLed:
                result = client.read_coils(clickLed[select])
                myState[select] = result.bits[0]
                if myState[select] != myLastState[select]:
                    print(f'{select}: {myState[select]}')
                    myLastState[select] = myState[select]
        except KeyboardInterrupt:
            Loopy = False

    client.close()
    print('DONE')