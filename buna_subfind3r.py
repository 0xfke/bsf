#!/usr/bin/env python3

import requests
import socket
import threading

# List of common subdomains to check
common_subdomains = [
    'www', 'mail', 'lms.courses', 'preview.lms', 'api.courses', 'lms', 'ftp', 'remote', 'webmail', 'server', 'ns1', 'ns2', 'blog', 'dev', 'shop', 'api', 'test',
    'secure', 'admin', 'login', 'forum', 'portal', 'beta', 'stage', 'demo', 'vpn', 'mysql', 'mssql', 'pgsql',
    'oracle', 'ldap', 'dns', 'proxy', 'backup', 'crm', 'files', 'download', 'upload', 'media', 'stats', 'status',
    'ads', 'search', 'chat', 'imap', 'pop', 'smtp', 'mailserver', 'calendar', 'web', 'mobile', 'm', 'api', 'labs',
    'app', 'apps', 'dashboard', 'control', 'panel', 'billing', 'payment', 'invoices', 'checkout', 'cart', 'oauth',
    'auth', 'login', 'signup', 'subscribe', 'register', 'join', 'go', 'assets', 'img', 'images', 'pictures', 'photos',
    'static', 'cdn', 'js', 'css', 'fonts', 'videos', 'blog', 'news', 'press', 'support', 'help', 'faq', 'contact',
    'about', 'team', 'jobs', 'careers', 'clients', 'partners', 'terms', 'privacy', 'cookies', 'legal', 'info', 'news',
    'updates', 'release', 'press', 'events', 'conference', 'summit', 'training', 'courses', 'academy', 'learn', 'docs',
    'developer', 'partners', 'affiliate', 'investors', 'download', 'resources', 'marketplace', 'shop', 'store', 'ecommerce',
    'forum', 'community', 'board', 'support', 'help', 'bug', 'issues', 'tickets', 'forums', 'feedback', 'suggestions',
    'survey', 'wiki', 'knowledgebase', 'documentation', 'tools', 'api', 'integration', 'developer', 'sandbox', 'labs',
    'research', 'whitepaper', 'books', 'library', 'archives', 'gallery', 'preview',  'projects', 'members', 'users', 'profile',
    'account', 'settings', 'preferences', 'notifications', 'messages', 'inbox', 'outbox', 'chat', 'messages', 'chat',
    'events', 'calendar', 'agenda', 'schedule', 'meetings', 'appointments', 'tasks', 'todo', 'notes', 'files', 'downloads',
    'resources', 'assets', 'data', 'analytics', 'metrics', 'reports', 'dashboard', 'stats', 'statistics', 'trends', 'insights',
    'analysis', 'monitor', 'tracker', 'log', 'logs', 'error', 'debug', 'audit', 'security', 'backup', 'archive', 'cron',
    'automation', 'scripts', 'tools', 'utilities', 'services', 'service', 'business', 'enterprise', 'company', 'corp',
    'foundation', 'association', 'partnership', 'alliance', 'division', 'team', 'department', 'projects', 'labs', 'research',
    'innovation', 'engineering', 'technology', 'science', 'projects', 'products', 'innovation', 'development', 'developers',
    'testers', 'qa', 'engineering', 'architecture', 'design', 'ux', 'ui', 'brand', 'marketing', 'promotion', 'branding',
    'identity', 'awareness', 'media', 'press', 'release', 'blog', 'news', 'stories', 'events', 'partners', 'clients',
    'customers', 'public', 'relations', 'affairs', 'publicity', 'campaign', 'ads', 'advertise', 'sponsorship', 'promotion',
    'deals', 'offers', 'sale', 'buy', 'trade', 'commerce', 'market', 'shop', 'store', 'products', 'goods', 'items',
    'shopping', 'cart', 'checkout', 'order', 'billing', 'payment', 'invoice', 'shipment', 'delivery', 'returns', 'refund',
    'feedback', 'review', 'testimonials', 'ratings', 'scores', 'survey', 'poll', 'vote', 'opinion', 'feedback', 'customer',
    'client', 'satisfaction', 'loyalty', 'support', 'help', 'faq', 'question', 'answer', 'support', 'service', 'helpdesk',
    'support', 'tickets', 'issues', 'contact', 'contactus', 'feedback', 'inquiries', 'suggestions', 'complaints', 'problems',
    'help', 'needhelp', 'assistance', 'emergency', 'alert', 'warning', 'info', 'announcements', 'updates', 'news', 'press',
    'media', 'release', 'public', 'relations', 'about', 'info', 'company', 'corporate', 'team', 'ourteam', 'staff', 'ourstaff',
    'career', 'jobs', 'work', 'hiring', 'joinus', 'vacancy', 'opportunity', 'resume', 'cv', 'application', 'submit', 'subscribe',
    'register', 'signup', 'login', 'signin', 'logout', 'signout', 'myaccount', 'account', 'profile', 'settings', 'preferences',
    'dashboard', 'panel', 'console', 'controlpanel', 'administration', 'management', 'backend', 'frontend', 'client', 'user',
    'clients', 'users', 'members', 'customers', 'guest', 'guests', 'visitor', 'visitors', 'new', 'newuser', 'newmember',
    'newcustomer', 'newclient', 'support', 'help', 'faq', 'terms', 'privacy', 'security', 'policy', 'tos', 'legal', 'copyright',
    'disclaimer', 'warning', 'alert', 'notification', 'emergency', 'info', 'about', 'learn', 'explore', 'discover', 'tour', 'demo',
    'download', 'get', 'access', 'try', 'buy', 'order', 'purchase', 'shop', 'store', 'blog', 'news', 'articles', 'guides', 'howto',
    'tutorials', 'resources', 'documentation', 'faq', 'help', 'support', 'contact', 'forum', 'community', 'discuss', 'chat',
    'talk', 'speak', 'connect', 'join', 'follow', 'subscribe', 'partners', 'affiliates', 'developers', 'api', 'integration',
    'tools', 'platform', 'sdk', 'libraries', 'plugins', 'extensions', 'modules', 'components', 'projects', 'opensource',
    'contribute', 'collaborate', 'donate', 'sponsor', 'about', 'company', 'team', 'vision', 'mission', 'values', 'goals', 'history',
    'newsroom', 'events', 'clients', 'partners', 'investors', 'financials', 'reports', 'governance', 'leadership', 'board',
    'contact', 'locations', 'career', 'jobs', 'opportunities', 'work', 'culture', 'life', 'benefits', 'diversity', 'inclusion',
    'campus', 'university', 'students', 'graduates', 'alumni', 'research', 'innovation', 'labs', 'labs', 'projects', 'blogs',
    'blog', 'news', 'media', 'events', 'press', 'release', 'support', 'help', 'faq', 'community', 'forum', 'contact', 'partners',
    'affiliates', 'about', 'company', 'team', 'history', 'jobs', 'blog', 'news', 'events', 'support', 'contact', 'faq', 'privacy',
    'policy', 'terms', 'conditions', 'security', 'responsible', 'disclosure', 'accessibility', 'help', 'support', 'contact',
    'faq', 'community', 'forum', 'blog', 'news', 'press', 'release', 'events', 'partners', 'clients', 'investors', 'about',
    'team', 'jobs', 'careers', 'contact', 'support', 'help', 'faq', 'blog', 'news', 'press', 'release', 'events', 'partners',
    'about', 'team', 'careers', 'contact', 'investors', 'privacy', 'policy', 'terms', 'conditions', 'copyright', 'disclaimer',
    'security', 'infosec', 'disclosure', 'gdpr', 'compliance', 'news', 'updates', 'press', 'release', 'events', 'newsletter',
    'subscribe', 'privacy', 'policy', 'terms', 'conditions', 'gdpr', 'compliance', 'contact', 'support', 'help', 'faq', 'blog',
    'news', 'press', 'release', 'events', 'partners', 'about', 'team', 'jobs', 'careers', 'investors', 'contact', 'support',
    'help', 'faq', 'blog', 'news', 'press', 'release', 'events'
]

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
                    print(f"[+] Found subdomain: {url} -> {ip_address}")
        except requests.ConnectionError:
            pass

    threads = []
    for subdomain in common_subdomains:
        thread = threading.Thread(target=check_subdomain, args=(subdomain,))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

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
    output_file = input("Enter the output file to save found subdomains (leave blank for no output file): ")

    print(f"Finding subdomains for {domain}...")
    subdomains = find_subdomains(domain, output_file)
    if subdomains:
        print("\nFound subdomains:")
        printed_ips = set()  # Set to keep track of printed IPs
        for sub, ip in subdomains:
            if ip not in printed_ips:
                print(f"{sub} -> {ip}")
                printed_ips.add(ip)
    else:
        print("No subdomains found.")

if __name__ == "__main__":
    main()

