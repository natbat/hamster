import serial
import time
import sys

def go(path_to_serial = '/dev/tty.usbmodem1411'):
    s = serial.Serial(path_to_serial, 9600)
    readings = []
    revolutions = 0
    previous_state = None
    buffer = ''
    while True:
        try:
            buffer += s.readline().strip()
        except Exception:
            time.sleep(0.1)
            continue
        if ',' in buffer:
            v = buffer
            buffer = ''
            vals = [int(i) for i in v.split(',') if i.isdigit()]
            readings.extend(vals)
            if len(readings) > 3:
                del readings[0]
            # If all three are less than 100, state should be 'lo'
            state = 'unknown'
            if all([r < 100 for r in readings]):
                state = 'lo'
            elif any([r > 1000 for r in readings]):
                state = 'hi'
            print state
            if state == 'unknown':
                print '  %r' % readings
            if state == previous_state:
                # Ignore
                pass
            else:
                # We only count a revolution when we drop from hi to lo
                if previous_state == 'hi' and state == 'lo':
                    revolutions += 1
                    print "Revolutions: %d" % revolutions
            previous_state = state
        time.sleep(0.01)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        go(sys.argv[1])
    else:
        go()

