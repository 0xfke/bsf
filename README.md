# Buna Subdomain Finder

Buna Subdomain Finder is a Python script designed to discover common subdomains for a given domain. It performs HTTP requests and DNS resolution to identify and verify subdomains, providing a quick and efficient way to find subdomains and their corresponding IP addresses.

## Features

- Checks a predefined list of common subdomains.
- Uses multithreading to perform checks concurrently for faster results.
- Performs HTTP requests and checks for successful responses.
- Resolves subdomains to IP addresses.
- Outputs found subdomains and IP addresses to the console and optionally to a file.

## Usage

1. **Clone the repository:**
    ```sh
    git clone https://github.com/0xfke/bsf.git
    cd bsf
    ```

2. **Install the required dependencies:**
    ```sh
    pip install requirments.txt
    ```
3. **Make the tool excutable:**
    ```sh
     sudo mv buna_subfind3r.py /usr/bin/bsf
     chmod +x bsf
4. **Run the script:**
    ```sh
    bsf
    ```

5. **Input the domain:**
    Enter the domain to find subdomains for (e.g., example.com)

6. **Optional Output File:**
    Enter the output file to save found subdomains (leave blank for no output file)

## Example

```sh
    ____ _____ ______
   / __ ) ___// ____/ youtube  @bunabyte
  / __  \__ \/ /_     telegram @bunabytecs
 / /_/ /__/ / __/     
/_____/____/_/        

 ____                      ____        _       _____ _           _           
| __ ) _   _ _ __   __ _  / ___| _   _| |__   |  ___(_)_ __   __| | ___ _ __ 
|  _ \| | | | '_ \ / _` | \___ \| | | | '_ \  | |_  | | '_ \ / _` |/ _ \ '__|
| |_) | |_| | | | | (_| |  ___) | |_| | |_) | |  _| | | | | | (_| |  __/ |   
|____/ \__,_|_| |_|\__,_| |____/ \__,_|_.__/  |_|   |_|_| |_|\__,_|\___|_|   
  
Buna-Byte's Security Framework - Ethical hacking and cybersecurity tools.

    
Enter the domain to find subdomains for (e.g., example.com): example.com
Enter the output file to save found subdomains (leave blank for no output file): subdomains.txt
Finding subdomains for example.com...

[+] Found subdomain: http://www.example.com -> 93.184.216.34
[+] Found subdomain: http://mail.example.com -> 93.184.216.32


Found subdomains:
http://www.example.com -> 93.184.216.34
http://www.example.com -> 93.184.216.34
...
```

