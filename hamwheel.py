import serial
import time
import sys

# We count a revolution when high drops to low... but only if our state
# has been reset. We reset state after 20 low readings in a row.

NUM_LOW_READINGS_NEEDED_TO_RESET = 20

def go(path_to_serial = '/dev/tty.usbmodem1411'):
    s = serial.Serial(path_to_serial, 9600)
    readings = []
    revolutions = 0
    previous_state = None
    buffer = ''
    receptive_to_a_count = False
    successive_low_readings = []
    last_reading_was_lo = False
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
                if last_reading_was_lo:
                    successive_low_readings.append(1)
                    if len(successive_low_readings) >= 20:
                        successive_low_readings = []
                        receptive_to_a_count = True
                        #print 'Now receptive'
                last_reading_was_lo = True
            elif any([r > 1000 for r in readings]):
                state = 'hi'
                last_reading_was_lo = False
               #            print state
            if state == 'unknown':
                pass
#                print '  %r' % readings
            if state == previous_state:
                # Ignore
                pass
            else:
                # We only count a revolution when we drop from hi to lo
                if previous_state == 'hi' and state == 'lo' and receptive_to_a_count:
                    revolutions += 1
                    print "Revolutions: %d (time = %s)" % (
                        revolutions, time.time()
                    )
                    sys.stdout.flush()
                    receptive_to_a_count = False
                    #print 'Not receptive'
            previous_state = state
        time.sleep(0.01)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        go(sys.argv[1])
    else:
        go()

