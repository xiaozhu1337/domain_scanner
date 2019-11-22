import dns.resolver
from concurrent.futures import ThreadPoolExecutor


def get_valid_dns_servers():
    print("[*] Start getting valid dns servers")
    with open('./dicts/dns_servers.txt') as f:
        dns_servers = [dns_server.strip() for dns_server in f if not dns_server.startswith("#")]
        with ThreadPoolExecutor() as executor:
            result_list = executor.map(_is_valid_dns_server, dns_servers)
            return [dns_servers[i] for i, v in enumerate(result_list) if v]

def _is_valid_dns_server(server):
    resolver = dns.resolver.Resolver(configure=False)
    resolver.timeout = 5.0
    resolver.lifetime = 5.0
    resolver.nameservers = [server]
    try:      
        answers = resolver.query('public-dns-a.baidu.com')    # an existed domain
        if answers[0].address != '180.76.76.76':
            print("[-] test dns server {:20s} : invalid".format(server))
            return False
        try:
            resolver.query('test.bad.dns.sejiji.com')    # non-existed domain
            print("[-] test dns server {:20s} : invalid".format(server))
            return False
        except:
            print("[-] test dns server {:20s} : valid".format(server))
            return True
    except:
        print("[-] test dns server {:20s} : invalid".format(server))
        return False

if __name__ == "__main__":
    # print(_is_valid_dns_server("114.114.114.114"))
    # print(_is_valid_dns_server("8.8.8.8"))
    # print(_is_valid_dns_server("114.14.124.13"))
    print(get_valid_dns_servers())