#!/usr/bin/env python
# pylint: disable=C0200
"""
side-channel timing attack
"""

import os
import secrets
import time

# Length of password. Can be tuned if folks are solving it quickly
PASSWORD_LEN = 4
# Length of time to sleep when guess entry is correct. "simulates compute time "
SIMULATE_COMPUTE_TIME = 0.1


def generate_password() -> str:
    """
    generate a random password at start up
    """
    tmp = secrets.token_hex(PASSWORD_LEN).lower()
    # with open("dump", 'w') as fh:
    #     fh.write(tmp)
    return tmp


def read_flag() -> str:
    """
    read flag from file on disk
    """
    with open("flag", "r", encoding="ascii") as file_handle:
        data = file_handle.read()
    return data


def do_heavy_compute() -> None:
    """
    simulates some compute
    """
    time.sleep(SIMULATE_COMPUTE_TIME)


def check_guess(guess, realdeal) -> bool:
    """
    validate if the given guess matches what's known
    """
    if len(guess) != len(realdeal):
        #print(len(guess), len(realdeal))
        return False
    do_heavy_compute()
    for idx in range(len(guess)):
        if guess[idx] == realdeal[idx]:
            do_heavy_compute()
        else:
            return False
    return True


def main():
    """
    le big mac
    """
    timeout = os.getenv("CHALL_TIMEOUT")
    # Create random password
    secret_password = generate_password()
    print("Figure out the password to get the flag.")
    print("The password is dynamic and changes every connection session.")
    print(f"The connection will terminate in {timeout} seconds.")

    while True:
        guess = input(": ")
        if check_guess(guess, secret_password):
            flag = read_flag()
            print(f"Well done! Here's your flag: {flag}")
            continue
        print("Incorrect. Try again.")


if __name__ == "__main__":
    main()
