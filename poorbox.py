#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    PoorBox
    =======

    Poor man's dropbox -- Recursively downloads a dropbox directory
    using the REST API.

    It downloads only the files that have been modified.

    Because the Dropbox REST API can only download/upload entire files, not
    file-deltas, synchronization can be slower than the real Dropbox software,
    especially for large files.

    We don't upload changes yet, so sync is one-way only. Maybe in the future!

    This software is intended for platforms on which Dropbox does not run,
    such as ARM, Raspberry Pi etc.
    '''

from __future__ import (absolute_import, division, print_function,
    unicode_literals)
import json
import logging
import os
import stat
from shutil import rmtree
from sys import exit
from time import sleep
from datetime import datetime
from dropbox import client, rest, session
# https://www.dropbox.com/static/developers/dropbox-python-sdk-1.5.1-docs/


# If you change the code or fork this project, you MUST change these lines to
# provide your own app key and app secret. You are NOT ALLOWED to use these:
APP_KEY = 'eulow8e1l6vd8rp'
APP_SECRET = '4lvtbphia79iksd'
# For more information browse to https://www.dropbox.com/developers/apps
ACCESS_TYPE = 'app_folder'  # 'app_folder' or 'dropbox'


def is_dir(path):
    """Return true if the path refers to an existing directory."""
    try:
        st = os.stat(path)
    except os.error:
        return False
    return stat.S_ISDIR(st.st_mode)


def mkdir(path):
    '''Make directories (if they don't exist already).'''
    if not is_dir(path):
        os.makedirs(path)


def request_user_authentication(url):
    '''This default implementation works on the console. You can implement
    another version for your app. For instance, the implementation would be
    different for a GUI app. Or maybe in your case you would like to use
    xdg-open to open the default browser automatically.
    '''
    print("Please authorize in your browser and press Enter when done:\n{}" \
        .format(url))
    raw_input()
    return True


class AuthenticationFailure(Exception):
    pass


class PoorBox(object):
    def load_cache(self):
        if os.path.exists(self.cache_path):
            with open(self.cache_path, 'r') as f:
                self.cache = json.load(f)
        else:
            self.cache = {}

    def save_cache(self):
        with open(self.cache_path, 'w') as f:
            json.dump(self.cache, f)

    def __init__(self, token_key=None, token_secret=None, cursor=None,
        cache_path='poorbox.cache', output_dir=None,
        request_user_authentication=request_user_authentication,
        app_key=APP_KEY, app_secret=APP_SECRET, access_type=ACCESS_TYPE):
        '''``access_type`` can be "app_folder" or "dropbox". The latter gives
        you access to an entire dropbox, but is much less likely to be
        approved by Dropbox.

        ``request_user_authentication`` is a callback your app may provide.
        '''
        self.cache_path = cache_path
        self.load_cache()
        if token_key:
            self.cache['token_key'] = token_key
        if token_secret:
            self.cache['token_secret'] = token_secret
        if cursor:
            self.cache['cursor'] = cursor
        if token_key or token_secret or cursor:
            self.save_cache()

        self.output_dir = output_dir
        self.request_user_authentication = request_user_authentication

        # TODO Test what happens when app_key is incorrect
        sess = session.DropboxSession(app_key, app_secret, access_type)
        logging.debug('Dropbox session created.')
        # Unfortunately the authentication step MUST be interactive:
        try:
            sess.set_token(self.cache['token_key'], self.cache['token_secret'])
            logging.debug('Reusing access token.')
        except Exception as e:
            print('MAKE A NOTE', type(e), e) # TODO Remove print
            # We need a new token
            request_token = sess.obtain_request_token()
            url = sess.build_authorize_url(request_token)
            # Ask user to visit a URL
            if not self.request_user_authentication(url):
                raise AuthenticationFailure()
            # Another API request gives us access:
            sess.obtain_access_token(request_token)
            logging.debug('Got a new access token. Saving in cache...')
            self.cache['token_key'] = sess.token.key
            self.cache['token_secret'] = sess.token.secret
            self.save_cache()
        self.client = client.DropboxClient(sess)

    RETRY_FILE = 5

    def download_file(self, remote_path, local_path):
        # local_path = os.path.expanduser(local_path)
        directory, filename = os.path.split(local_path)
        mkdir(directory)  # create if it does not exist
        # Try to download 5 times to handle http 5xx errors from dropbox
        for attempt in range(self.RETRY_FILE):
            try:
                fr = self.client.get_file(remote_path)
                with open(local_path, 'wb') as fw:
                    fw.write(fr.read())
            except (rest.ErrorResponse, rest.RESTSocketError) as error:
                logging.debug('An error occured while downloading a file. '
                    'We attempt this {} times. The error was: {}'.format(
                        self.RETRY_FILE, str(error)))
                sleep(attempt * 8)
            else:
                return local_path

    def update(self, output_dir=None):
        cursor = self.cache.get('cursor', None)
        output_dir = os.path.expanduser(output_dir or self.output_dir)
        while True:
            resp = self.client.delta(cursor)
            logging.info()
            if resp['reset']:
                logging.info("This time, I am deleting the whole tree first. "
                    "Dropbox tells me to.")
                rmtree(output_dir)
                mkdir(output_dir)
            entries = resp['entries']
            num_entries = len(entries)
            for index, path, metadata in enumerate(entries):
                local_path = os.path.join(output_dir, path)
                if metadata and metadata['is_dir']:
                    logging.info("D {}/{} {}".format(index, num_entries, path))
                    mkdir(local_path)
                elif metadata:  # Download a file
                    logging.info("↓ {}/{} {}".format(index, num_entries, path))
                    self.download_file(path, local_path)
                else:  # metadata is None, this means delete!
                    logging.info("X {}/{} {}".format(index, num_entries, path))
                    if is_dir(local_path):
                        rmtree(local_path)
                    else:
                        os.remove(local_path)
            cursor = resp['cursor']
            logging.debug("New cursor: {}".format(cursor))
            self.cache['cursor'] = cursor
            self.save_cache()
            if not resp['has_more']:
                break

PoorBox.__doc__ = __doc__


def poorbox_from_dict(adict):  # TODO Implement
    raise NotImplementedError()
    # TODO Read cache into adict
    return PoorBox(**adict)


def poorbox_from_config_file(path):  # TODO Implement
    raise NotImplementedError()
    # TODO Read config file into adict
    return poorbox_from_dict(adict)


def create_config_file(path):  # TODO FIX
    '''Config: app_key, app_secret, access_type, output_dir, cache_file
        OMIT app_key if it is ours
    '''
    raise NotImplementedError()


def main():
    init_logging()
    try:
        poorbox = PoorBox() # TODO argparse
        poorbox.update()
    except AuthenticationFailure:  # We are unauthorized, so
        exit(401)        # exit to system with an error code.


def init_logging():
    """Set up log file. TODO: Make configurable."""
    now = datetime.now()
    date_string = now.strftime('%Y-%m-%d_%H-%M')
    logfile_name = 'poorbox-' + date_string + '.log'
    logging.basicConfig(filename=logfile_name, level=logging.DEBUG)


if __name__ == '__main__':
    main()
