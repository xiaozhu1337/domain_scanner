import dns.resolver
from concurrent.futures import ThreadPoolExecutor


def domain2ip(test_domain, dns_resolver, i, total, check_wildcard=False):
    #print("[-] testing {}".format(test_domain))
    #print(dns_resolver.nameservers)
    try:
        answers = dns_resolver.query(test_domain)    # an existed domain
        #print(answers[0])
        return answers[0].address
    except:
        return False
    finally:
        if check_wildcard == False:
            if int((i/total)*1000000) % 200000 == 0:
                print("[-] scan 20%")

def is_wildcard(sub_domains, dns_server):
    print("[*] check wildcard")
    if len(sub_domains) > 10:
        sub_domains = sub_domains[:10]
    ips = [ip for _, ip in concurrent_domain2ip(sub_domains, dns_server, check_wildcard=True)]
    if (len(set(ips))) == 1:
        return True
    else:
        return False


def concurrent_domain2ip(test_domains, dns_servers ,threads=100, check_wildcard=False):
    if not check_wildcard:
        print("[*] Start concurrent scan sub domains")
    if len(test_domains) < 100:
        threads = len(test_domains)

    dns_resolvers = [dns.resolver.Resolver(configure=False) for i in range(threads)]
    for i in range(len(dns_resolvers)):
        dns_resolvers[i].nameservers = [dns_servers[i % len(dns_servers)]]
        dns_resolvers[i].timeout = 5.0
        dns_resolvers[i].lifetime = 5.0

    with ThreadPoolExecutor(max_workers=threads) as executor:
        result = []
        for i in range(len(test_domains)):
            e = executor.submit(domain2ip, test_domains[i], dns_resolvers[i % threads], i+1, len(test_domains), check_wildcard=check_wildcard)
            result.append((test_domains[i], e))

        valid_domains = [(domain, future.result()) for (domain, future) in result if future.result() is not False]
    if not check_wildcard:
        print("[*] Complete concurrent scan")
    return valid_domains

if __name__ == "__main__":
    from get_sub_domain_list import get_sub_domain_list
    from get_valid_dns_servers import get_valid_dns_servers
    sub_domains = get_sub_domain_list("cqupt.edu.cn")
    valid_dns_servers = ['114.114.114.114']
    print(concurrent_domain2ip(sub_domains[:500], valid_dns_servers, 200))
    #print(is_wildcard(sub_domains[:100], valid_dns_servers[0]))

    

