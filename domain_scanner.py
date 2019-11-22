from libs.parse_args import parse_args
from libs.get_sub_domain_list import get_sub_domain_list
from libs.get_valid_dns_servers import get_valid_dns_servers
from libs.test_domain_name import is_wildcard
from libs.test_domain_name import concurrent_domain2ip
import time
import sys


if __name__ == "__main__":
    args = parse_args() # args. target / file / output / full / threads / ip
    output_filename = "./output/" + args.target + "_" + str(time.time()).split('.')[0] + '.txt'

    valid_dns_servers = get_valid_dns_servers()
    if len(valid_dns_servers) == 0:
        print("[*] no valid dns server")
        sys.exit()

    sub_domains = get_sub_domain_list(args.target, args.file)
    if is_wildcard(sub_domains[:10], valid_dns_servers[0]):
        print("[*] wildcard detect, stop execution")
        sys.exit()

    valid_sub_domains_and_ips = concurrent_domain2ip(sub_domains[:500], valid_dns_servers, args.threads)

    with open(output_filename, 'w') as f:
        for domain, ip in valid_sub_domains_and_ips:
            if args.ip:
                f.write(domain.ljust(30) + ip + '\n')
            else:
                f.write(domain.ljust(30) + '\n')
    
    print("[*] Result write to {}".format(output_filename))
    