#!/usr/bin/env python3

import curses
import requests
import tldextract
import dns.resolver
from time import sleep

def get_subdomains_from_crtsh(domain):
    subdomains = set()
    url = f"https://crt.sh/?q=%.{domain}&output=json"
    retries = 3
    for i in range(retries):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                for entry in data:
                    name_value = entry['name_value']
                    subdomains.update(name_value.split('\n'))
                break
        except Exception as e:
            print(f"Attempt {i+1}/{retries} - Error querying crt.sh: {e}")
            sleep(2)  # Wait before retrying
    return subdomains

def get_subdomains_from_dnsdumpster(domain):
    subdomains = set()
    url = 'https://dnsdumpster.com/'
    session = requests.Session()
    retries = 3
    for i in range(retries):
        try:
            # Get the CSRF token and cookies
            initial_response = session.get(url)
            csrf_token = initial_response.cookies['csrftoken']

            # Post the domain query
            data = {
                'csrfmiddlewaretoken': csrf_token,
                'targetip': domain
            }
            headers = {
                'Referer': url
            }
            response = session.post(url, data=data, headers=headers)
            if response.status_code == 200:
                subdomain_list = response.text.split('Domain Name')[1:]
                for entry in subdomain_list:
                    subdomain = entry.split()[0]
                    subdomains.add(subdomain)
                break
        except Exception as e:
            print(f"Attempt {i+1}/{retries} - Error querying DNSDumpster: {e}")
            sleep(2)  # Wait before retrying
    return subdomains

def resolve_subdomains(subdomains, domain):
    resolved_subdomains = set()
    unresolved_subdomains = set()

    for subdomain in subdomains:
        full_domain = f"{subdomain}.{domain}"
        try:
            answers = dns.resolver.resolve(full_domain, 'A')
            for rdata in answers:
                resolved_subdomains.add(full_domain)
        except dns.resolver.NoAnswer:
            unresolved_subdomains.add(full_domain)
        except dns.resolver.NXDOMAIN:
            unresolved_subdomains.add(full_domain)
        except Exception as e:
            print(f"Error resolving {full_domain}: {e}")

    return resolved_subdomains, unresolved_subdomains

def find_subdomains(domain):
    subdomains = set()

    subdomains.update(get_subdomains_from_crtsh(domain))
    subdomains.update(get_subdomains_from_dnsdumpster(domain))

    resolved_subdomains, unresolved_subdomains = resolve_subdomains(subdomains, domain)

    return resolved_subdomains, unresolved_subdomains

def print_help(stdscr):
    stdscr.addstr(0, 0, "BUNA", curses.color_pair(1) | curses.A_BOLD)
    stdscr.addstr(2, 0, "██╗   ██╗██╗███╗   ██╗██╗██╗  ██╗", curses.color_pair(1))
    stdscr.addstr(3, 0, "Buna SubF1nd3r - Subdomain Enumeration Tool", curses.color_pair(1) | curses.A_BOLD)
    stdscr.addstr(4, 0, "██║   ██║██║██╔██╗ ██║██║ ╚███╔╝ ", curses.color_pair(1))
    stdscr.addstr(5, 0, "Usage:", curses.color_pair(2))
    stdscr.addstr(6, 2, "Drop your domain name here:", curses.color_pair(2))
    stdscr.addstr(7, 2, "Press 'q' to exit.", curses.color_pair(2))
    stdscr.refresh()

def main(stdscr):
    # Clear screen
    stdscr.clear()

    # Set up colors
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)

    # Display ASCII art header
    header = """
     ██╗   ██╗██╗███╗   ██╗██╗██╗  ██╗
     ██║   ██║██║██╔██╗ ██║██║ ╚███╔╝ 
     ██║   ██║██║██║╚██╗██║██║ ██╔██╗ 
     ╚██████╔╝██║██║ ╚████║██║██╔╝ ██╗
      ╚═════╝ ╚═╝╚═╝  ╚═══╝╚═╝╚═╝  ╚═╝
"""
    stdscr.addstr(0, 0, header, curses.color_pair(1) | curses.A_BOLD)

    # Display help message
    print_help(stdscr)

    while True:
        # Input box
        input_window = curses.newwin(1, 50, 8, 0)
        input_window.addstr(0, 0, "")
        curses.echo()  # Enable text input
        domain = input_window.getstr().decode("utf-8")

        if domain.lower() == 'q':
            break

        # Perform subdomain enumeration and display results
        stdscr.addstr(10, 0, "Finding subdomains...", curses.color_pair(1))
        stdscr.refresh()

        resolved_subdomains, unresolved_subdomains = find_subdomains(domain)

        stdscr.addstr(12, 0, f"Resolved Subdomains ({len(resolved_subdomains)}):", curses.color_pair(2))
        row = 13
        for subdomain in resolved_subdomains:
            if row < curses.LINES - 3:  # Check if there's space in the window
                stdscr.addstr(row, 2, subdomain[:curses.COLS-4], curses.color_pair(2))
                row += 1
            else:
                break

        stdscr.addstr(row + 1, 0, f"Subdomains with DNS Resolution Issues ({len(unresolved_subdomains)}):", curses.color_pair(3))
        row += 2
        for subdomain in unresolved_subdomains:
            if row < curses.LINES - 3:  # Check if there's space in the window
                stdscr.addstr(row, 2, f"Could not resolve: {subdomain[:curses.COLS-4]}", curses.color_pair(3))
                row += 1
            else:
                break

        stdscr.refresh()

if __name__ == "__main__":
    curses.wrapper(main)
