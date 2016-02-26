#!/usr/bin/env python2

import argparse
import os

try:
    from gevent.monkey import patch_all
    patch_all(subprocess=False, aggressive=False)
    from gevent.pywsgi import WSGIServer
except ImportError:
    print 'You need install gevent manually! System shutdown.'
    sys.exit()

from ghttp import GHTTPServer

def parse_args():
    ap = argparse.ArgumentParser()
    ap.add_argument('-p', '--path', required=True, help='Path from which to serve git')
    return ap.parse_args()


def main():
    args = parse_args()
    if not os.path.isdir(args.path):
        raise IOError(2, 'Ain\'t no directory', args.path)

    server = WSGIServer(('0.0.0.0', 8080), GHTTPServer({
        'upload_pack': True,
        'receive_pack': True,
        'project_root': args.path,
    }))
    server.serve_forever()


if __name__ == '__main__':
    main()

