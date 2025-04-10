#!/usr/bin/env python3

import requests
import socket
import threading
import logging
from concurrent.futures import ThreadPoolExecutor
import re
import sys

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# List of common subdomains to check
common_subdomains = [
    'www', 'mail', 'lms.courses', 'preview.lms', 'api.courses', 'lms', 'ftp', 'remote', 'webmail', 'server', 'ns1', 'ns2', 
    'blog', 'dev', 'shop', 'api', 'test', 'secure', 'admin', 'login', 'forum', 'portal', 'beta', 'stage', 'demo', 'vpn', 
    'mysql', 'mssql', 'pgsql', 'oracle', 'ldap', 'dns', 'proxy', 'backup', 'crm', 'files', 'download', 'upload', 'media', 
    'stats', 'status', 'ads', 'search', 'chat', 'imap', 'pop', 'smtp', 'mailserver', 'calendar', 'web', 'mobile', 'm', 'labs',
    'app', 'apps', 'dashboard', 'control', 'panel', 'billing', 'payment', 'invoices', 'checkout', 'cart', 'oauth', 'auth', 
    'signup', 'assets', 'img', 'images', 'pictures', 'photos', 'static', 'cdn', 'js', 'css', 'fonts', 'videos', 'blog', 
    'news', 'press', 'support', 'help', 'faq', 'contact', 'about', 'team', 'jobs', 'careers', 'clients', 'partners', 'terms',
    'privacy', 'cookies', 'legal', 'info', 'updates', 'release', 'events', 'conference', 'summit', 'training', 'courses',
    'academy', 'learn', 'docs', 'developer', 'partners', 'affiliate', 'investors', 'download', 'resources', 'marketplace',
    'shop', 'store', 'ecommerce', 'community', 'board', 'feedback', 'survey', 'wiki', 'knowledgebase', 'documentation', 
    'integration', 'sandbox', 'labs', 'research', 'whitepaper', 'books', 'library', 'archives', 'gallery', 'projects', 
    'members', 'users', 'profile', 'account', 'settings', 'preferences', 'notifications', 'messages', 'inbox', 'outbox', 
    'chat', 'calendar', 'agenda', 'schedule', 'meetings', 'appointments', 'tasks', 'todo', 'notes', 'files', 'downloads',
    'analytics', 'metrics', 'reports', 'dashboard', 'stats', 'monitor', 'tracker', 'log', 'logs', 'error', 'debug', 'audit',
    'security', 'cron', 'automation', 'scripts', 'utilities', 'services', 'business', 'enterprise', 'company', 'foundation', 
    'association', 'alliance', 'division', 'department', 'team', 'projects', 'innovation', 'engineering', 'technology', 
    'science', 'development', 'developers', 'testers', 'qa', 'architecture', 'design', 'ux', 'ui', 'brand', 'marketing', 
    'promotion', 'sponsorship', 'deals', 'sale', 'buy', 'trade', 'commerce', 'shop', 'order', 'billing', 'payment', 'invoice',
    'shipment', 'delivery', 'returns', 'refund', 'feedback', 'reviews', 'survey', 'poll', 'vote', 'opinion', 'support', 
    'tickets', 'issues', 'complaints', 'helpdesk', 'emergency', 'alert', 'announcement', 'updates', 'press', 'release', 
    'public', 'relations', 'about', 'company', 'staff', 'work', 'hiring', 'vacancy', 'opportunity', 'resume', 'cv', 'application',
    'submit', 'register', 'login', 'signout', 'myaccount', 'profile', 'settings', 'preferences', 'dashboard', 'panel', 
    'administration', 'management', 'backend', 'frontend', 'user', 'guests', 'visitor', 'newuser', 'newmember', 'newclient', 
    'support', 'faq', 'terms', 'privacy', 'policy', 'tos', 'legal', 'disclaimer', 'help', 'contact', 'suggestions', 'inquiries', 
    'emergency', 'alert', 'notification', 'sponsor', 'about', 'company', 'team', 'vision', 'mission', 'values', 'goals', 'history',
    'jobs', 'career', 'opportunities', 'work', 'culture', 'benefits', 'diversity', 'campus', 'university', 'students', 
    'graduates', 'alumni', 'innovation', 'labs', 'research', 'events', 'support', 'contact'
]

# Validate domain input
def validate_domain(domain):
    if not re.match(r"^[a-zA-Z0-9.-]+$", domain):
        print(f"Invalid domain format: {domain}")
        sys.exit(1)

# Lock for thread-safe printing
print_lock = threading.Lock()

def find_subdomains(domain, output_file):
    found_subdomains = []

    def check_subdomain(subdomain):
        url = f"https://{subdomain}.{domain}"
        try:
            response = requests.get(url, timeout=60)
            if response.status_code == 200:
                try:
                    ip_address = socket.gethostbyname(f"{subdomain}.{domain}")
                except socket.gaierror:
                    ip_address = "Unable to resolve"
                with print_lock:
                    found_subdomains.append((url, ip_address))
                    logging.info(f"[+] Found subdomain: {url} -> {ip_address}")
        except requests.RequestException as e:
            logging.debug(f"Error with {url}: {e}")
        except socket.gaierror as e:
            logging.debug(f"DNS resolution failed for {url}: {e}")

    with ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(check_subdomain, common_subdomains)

    if output_file:
        with open(output_file, 'w') as f:
            for sub, ip in found_subdomains:
                f.write(f"{sub} -> {ip}\n")
    
    return found_subdomains

def main():
    banner = """
    ____ _____ ______
   / __ ) ___// ____/ youtube  @bunabyte
  / __  \__ \/ /_     facebook @BunaByte
 / /_/ /__/ / __/     telegram @hacker_habesha
/_____/____/_/        linkedin @Befikadu-Tesfaye

 ____                      ____        _       _____ _           _           
| __ ) _   _ _ __   __ _  / ___| _   _| |__   |  ___(_)_ __   __| | ___ _ __ 
|  _ \| | | | '_ \ / _` | \___ \| | | | '_ \  | |_  | | '_ \ / _` |/ _ \ '__|
| |_) | |_| | | | | (_| |  ___) | |_| | |_) | |  _| | | | | | (_| |  __/ |   
|____/ \__,_|_| |_|\__,_| |____/ \__,_|_.__/  |_|   |_|_| |_|\__,_|\___|_|   
  
Befikadu's Security Framework - Ethical hacking and cybersecurity tools.
    """
    print(banner)

    domain = input("Enter the domain to find subdomains for (e.g., example.com): ")
    validate_domain(domain)
    output_file = input("Enter the output file to save found subdomains (leave blank for no output file): ")

    logging.info(f"Finding subdomains for {domain}...")
    subdomains = find_subdomains(domain, output_file)
    if subdomains:
        print("\nFound subdomains:")
        printed_ips = set()  # Set to keep track of printed IPs
        for sub, ip in subdomains:
            if ip not in printed_ips:
                print(f"{sub} -> {ip}")
                printed_ips.add(ip)
    else:
        logging.info("No subdomains found.")

if __name__ == "__main__":
    main()
