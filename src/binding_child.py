#!/usr/bin/env python2.7

import signal
import sys

from binding.binding import Binding
from binding.corresponder import Corresponder

if __name__ == "__main__":
    if len(sys.argv) != 6:
        sys.stderr.write("usage: {} <interface> <port> <maxclients> <maxdown> <maxup>\n")
        sys.stderr.write("example: {} 127.0.0.1 28785 16 0 0\n")
        sys.exit()
        
    signal.signal(signal.SIGINT, signal.SIG_IGN)

    executable, interface = sys.argv[:2]
    port, maxclients, maxdown, maxup = map(int, sys.argv[2:])

    corresponder = Corresponder(sys.stdin.fileno(), sys.stdout.fileno())
    
    channels = 3
    timeout = 5

    binding = Binding(corresponder, interface, port, maxclients, maxup, maxdown, channels, timeout)
    binding.run()