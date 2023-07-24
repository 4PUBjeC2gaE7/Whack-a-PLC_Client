from pymodbus.client import ModbusTcpClient

# Constants
myServerAddr = '192.168.0.10'
clickSw = {
    'red':   10000,
    'yellow':10001,
    'green': 10002,
    'blue':  10003
}
clickLed = {
    'red':   0x2000,
    'yellow':0x2001,
    'green': 0x2002,
    'blue':  0x2003
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
    for select in clickSw:
        client.write_coil(clickSw[select], False)

    Loopy = True
    print('Press <Ctrl-C> to end\n')
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
    print('\nDONE')