

def get_sub_domain_list(target, sub_domain_list_file="./dicts/subnames.txt"):
    with open(sub_domain_list_file) as f:
        return [sub_domain.strip() + '.' + target.strip() for sub_domain in f]


if __name__ == "__main__":
    sub_domains = get_sub_domain_list("baidu.com")
    for i in range(5):
        print(sub_domains[i])