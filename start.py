import sys
import pulse

def __main__():
    if len(sys.argv) != 6:
        print "python start.py <c_key> <c_secret> <a_token> <a_token_s> <geotags>"
        sys.exit(-1)

    c_key = sys.argv[1]
    c_secret = sys.argv[2]
    a_token = sys.argv[3]
    a_token_s = sys.argv[4]
    geotags = sys.argv[5]

    p = pulse.Pulse(c_key, c_secret, a_token, a_token_s, eval(geotags))
    p.start()

__main__()
