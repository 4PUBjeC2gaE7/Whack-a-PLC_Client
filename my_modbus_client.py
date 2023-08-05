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
scoreAddr = 0x0001

if __name__ == '__main__':
    myState = {
        'red':False,
        'yellow':False,
        'green':False,
        'blue':False
    }
    myScore = -1

    # Connect to modbus server
    client = ModbusTcpClient(myServerAddr)
    client.connect()

    if client.connected:
        # Write to LED switches
        for select in clickSw:
            client.write_coil(clickSw[select], False)

        Loopy = True
        print('Press <Ctrl-C> to end\n')
        print(f'{"Red":10s}{"Yellow":10s}{"Green":10s}{"Blue":10s}\t{"Score":5s}')
        while Loopy is True:
            try:
                # Read LED indicators
                for select in clickLed:
                    myState[select] = client.read_coils(clickLed[select]).bits[0]
                    if select == "red":
                        print('\r',end='')
                    print(f'{"ON" if myState[select] else " ":10s}', end='')
                myScore = client.read_holding_registers(scoreAddr).registers[0]
                print(f'\t{myScore:-5d}',end='')
            except KeyboardInterrupt:
                Loopy = False
        client.close()
        print('\nDONE')