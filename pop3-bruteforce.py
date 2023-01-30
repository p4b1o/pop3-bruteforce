import poplib
import sys
import argparse
import itertools
from tqdm import tqdm

def login_pop3(login, password, pop3_server, use_ssl, port):
    if use_ssl:
        pop_conn = poplib.POP3_SSL(pop3_server, port=port)
    else:
        pop_conn = poplib.POP3(pop3_server, port=port)
    try:
        pop_conn.user(login)
        pop_conn.pass_(password)
        return pop_conn
    except poplib.error_proto as e:
        return None

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Logowanie do serwera POP3')
    parser.add_argument('--userfile', dest='userfile', help='Plik z loginem', required=True)
    parser.add_argument('--passfile', dest='passfile', help='Plik z hasłami', required=True)
    parser.add_argument('--pop3server', dest='pop3server', help='Adres serwera POP3', required=True)
    parser.add_argument('--port', dest='port', type=int, default=110, help='Port serwera POP3')
    parser.add_argument('--ssl', dest='use_ssl', help='Użyj SSL', action='store_true')
    args = parser.parse_args()

    with open(args.userfile, "r") as f:
        logins = [line.strip() for line in f.readlines()]
    with open(args.passfile, "r") as f:
        passwords = [line.strip() for line in f.readlines()]

    for login, password in tqdm(itertools.product(logins, passwords), desc="Logowanie", file=sys.stdout):
        pop_conn = login_pop3(login, password, args.pop3server, args.use_ssl, args.port)
        if pop_conn:
            break
    else:
        print("Nie udało się zalogować")
        sys.exit(1)

    print("Zalogowano pomyślnie")
    pop_conn.quit()
