#!/usr/bin/env python2

import argparse
import os
import sys

try:
    from gevent.monkey import patch_all
    patch_all(subprocess=False, aggressive=False)
    from gevent.pywsgi import WSGIServer
except ImportError:
    print 'You need install gevent!'
    sys.exit()

from ghttp import GHTTPServer


def parse_args():
    ap = argparse.ArgumentParser()
    ap.add_argument('-l', '--listen', required=False, default='0.0.0.0',
                    help='Listen for connections on this IP (default=0.0.0.0)')
    ap.add_argument('-p', '--port', required=False, default=8080, type=int,
                    help='Port from which to listen. (default=8080)')
    ap.add_argument('-d', '--directory', required=True,
                    help='Directory from which to serve git repos.')
    return ap.parse_args()


def main():
    args = parse_args()
    if not os.path.isdir(args.directory):
        raise IOError(2, 'Ain\'t no directory', args.path)

    server = WSGIServer((args.listen, args.port), GHTTPServer({
        'upload_pack': True,
        'receive_pack': True,
        'project_root': args.directory,
    }))
    server.serve_forever()


if __name__ == '__main__':
    main()

