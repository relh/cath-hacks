import sys
import pulse

def __main__():
    if len(sys.argv) != 5:
        print "python start.py <c_key> <c_secret> <a_token> <a_token_s>"
        sys.exit(-1)

    c_key = sys.argv[1]
    c_secret = sys.argv[2]
    a_token = sys.argv[3]
    a_token_s = sys.argv[4]
    keywords = open('keywords').read().splitlines()

    p = pulse.Pulse(c_key, c_secret, a_token, a_token_s, keywords)
    p.start()

if __name__ == '__main__':
    __main__()
