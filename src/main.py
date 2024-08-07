import ipaddress

from log import LOG

log = LOG()

logger_console = log.get_logger("console")
logger_file = log.get_logger("file")
logger_cf = log.get_logger("cf")


def main():
    source_cidr = "192.168.0.0/29"
    exclude_ips = ["192.168.0.2", "192.168.0.3"]

    exclude_ips = [ipaddress.IPv4Address(ip) for ip in exclude_ips]
    source_ips = list(ipaddress.ip_network(source_cidr))

    ips = []
    for ip in source_ips:
        if ip not in exclude_ips:
            ips.append(ip)
    ans = ipv4_addresses_to_cidr(ips)
    ans = [str(ip) for ip in ans]

    logger_console.info("##### answer ここから #####")
    for ip in ans:
        logger_console.info(f"{ip}")
    logger_console.info("##### answer ここまで #####")
    pass


def ipv4_addresses_to_cidr(ip_list):
    """
    IPv4アドレスのリストを受け取り、それらを含む最小のCIDRブロックのリストを返す関数

    :param ip_list: IPv4アドレスのリスト (list of str or list of ipaddress.IPv4Address)
    :return: CIDRブロックのリスト (list of ipaddress.IPv4Network)
    """
    # 文字列のリストが渡された場合、IPv4Addressオブジェクトに変換
    if isinstance(ip_list[0], str):
        ip_list = [ipaddress.IPv4Address(ip) for ip in ip_list]

    # collapse_addressesを使用してCIDRブロックにまとめる
    cidr_blocks = list(ipaddress.collapse_addresses(ip_list))

    return cidr_blocks


if __name__ == "__main__":
    logger_file.info("##### Start Script #####")
    main()
    logger_file.info("##### End Script #####")
