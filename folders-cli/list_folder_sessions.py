#!python3
import sys
import argparse
import requests
import urllib3

from panopto_folders import PanoptoFolders

from os.path import dirname, join, abspath
sys.path.insert(0, abspath(join(dirname(__file__), '..', 'common')))
from panopto_oauth2 import PanoptoOAuth2


def parse_argument():
    parser = argparse.ArgumentParser(description='Sample of Folders API')
    parser.add_argument('--server', dest='server', required=True, help='Server name as FQDN')
    parser.add_argument('--client-id', dest='client_id', required=True, help='Client ID of OAuth2 client')
    parser.add_argument('--client-secret', dest='client_secret', required=True, help='Client Secret of OAuth2 client')
    parser.add_argument('--skip-verify', dest='skip_verify', action='store_true', required=False, help='Skip SSL certificate verification. (Never apply to the production code)')
    return parser.parse_args()


def main():
    args = parse_argument()

    if args.skip_verify:
        # This line is needed to suppress annoying warning message.
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    # Use requests module's Session object in this example.
    # ref. https://2.python-requests.org/en/master/user/advanced/#session-objects
    requests_session = requests.Session()
    requests_session.verify = not args.skip_verify

    # Load OAuth2 logic
    oauth2 = PanoptoOAuth2(args.server, args.client_id, args.client_secret, not args.skip_verify)

    # Load Folders API logic
    folders = PanoptoFolders(args.server, not args.skip_verify, oauth2)

    current_folder_id = 'c6d51db2-b319-44ae-a190-2c5b06e926be'
    list_sessions(folders, current_folder_id)


def list_sessions(folders, folder_id):
    print('Sessions in the folder:')
    for entry in folders.get_sessions(folder_id):
        print('  {0}: {1}'.format(entry['Id'], entry['Name']))


if __name__ == '__main__':
    main()
