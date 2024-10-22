import time

from rpc import RPCClient

server = RPCClient('0.0.0.0', 8080)

server.connect()

server.new_round([
            ('hot/hottie', 36),
            ('handsome', 27),
            ('hunk', 19),
            ('stud', 6),
            ('fine', 3),
            ('sexy', 3),
            ('cute/cutie', 2),
            ('yummy', 2)
        ])

for i in range(3):
    time.sleep(3)
    server.set_strike(i+1)

server.disconnect()