import ipaddress
from dataclasses import dataclass
from datetime import datetime
from ipaddress import IPv4Address, IPv6Address, ip_address
from typing import Final

"""Nginx uses the Common Log Format
see: https://nginx.org/en/docs/http/ngx_http_core_module.html#var_time_local
see: https://en.wikipedia.org/wiki/Common_Log_Format"""
NGINX_TIME_LOCAL_FMT: Final[str] = "%d/%b/%Y:%H:%M:%S %z"


class NginxParseError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__()


@dataclass(frozen=True)
class NginxRequest:
    method: str
    target: str
    protocol: str


@dataclass(frozen=True)
class NginxLog:
    remote_addr: IPv4Address | IPv6Address
    remote_user: str
    time_local: datetime
    request: NginxRequest
    status: int
    bytes_sent: int
    http_referer: str
    http_user_agent: str


def parse(input: str) -> list[NginxLog]:
    logs = []
    for line in input.splitlines():
        log = parse_line(line)
        logs.append(log)

    return logs


def parse_line(input: str) -> NginxLog:
    """assumes "input" is in the format
    specified in https://nginx.org/en/docs/http/ngx_http_log_module.html#log_format

    note: this algorithm is very inefficient and can be improved"""

    remote_addr_start = 0
    separator = " - "
    remote_addr_str = search_until(input[remote_addr_start:], separator)
    remote_addr_end = remote_addr_start + len(remote_addr_str)

    remote_user_start = remote_addr_end + len(separator)
    separator = " ["
    remote_user_str = search_until(input[remote_user_start:], separator)
    remote_user_end = remote_user_start + len(remote_user_str)

    time_local_start = remote_user_end + len(separator)
    separator = '] "'
    time_local_str = search_until(input[time_local_start:], separator)
    time_local_end = time_local_start + len(time_local_str)

    request_start = time_local_end + len(separator)
    separator = '" '
    request_str = search_until(input[request_start:], separator)
    request_end = request_start + len(request_str)

    status_start = request_end + len(separator)
    separator = " "
    status_str = search_until(input[status_start:], separator)
    status_end = status_start + len(status_str)

    body_bytes_sent_start = status_end + len(separator)
    separator = ' "'
    body_bytes_sent_str = search_until(input[body_bytes_sent_start:], separator)
    body_bytes_sent_end = body_bytes_sent_start + len(body_bytes_sent_str)

    http_referer_start = body_bytes_sent_end + len(separator)
    separator = '" "'
    http_referer_str = search_until(input[http_referer_start:], separator)
    http_referer_end = http_referer_start + len(http_referer_str)

    http_user_agent_start = http_referer_end + len(separator)
    separator = '"'
    http_user_agent_str = search_until(input[http_user_agent_start:], separator)
    http_user_agent_end = http_user_agent_start + len(http_user_agent_str)

    if http_user_agent_end + len(separator) != len(input):
        raise NginxParseError(
            message="Expected http_user_agent to be the last field to parse"
        )

    remote_addr = ipaddress.ip_address(remote_addr_str)
    remote_user = remote_user_str
    time_local = datetime.strptime(time_local_str, NGINX_TIME_LOCAL_FMT)
    request = parse_request(request_str)
    status = int(status_str)
    body_bytes_sent = int(body_bytes_sent_str)
    http_referer = http_referer_str
    http_user_agent = http_user_agent_str

    return NginxLog(
        remote_addr,
        remote_user,
        time_local,
        request,
        status,
        body_bytes_sent,
        http_referer,
        http_user_agent,
    )


def search_until(input: str, separator: str) -> str:
    index = input.find(separator)
    if index == -1:
        raise NginxParseError(
            message="Expected sequence of characters '{0}' separating 'remote_addr' and 'remote_user' as defined in nginx log_format default directive but it was not found".format(
                separator
            )
        )

    return input[:index]


def parse_request(input: str) -> NginxRequest:
    method, target, protocol = input.split(" ")
    return NginxRequest(method, target, protocol)


def parse_remote_addr(input: str) -> IPv4Address | IPv6Address:
    try:
        return ip_address(input)
    except Exception:
        raise NginxParseError(
            message="remote_addr cannot be parsed to a valid IPV4/IPV6 address"
        )


def parse_time_local(input: str) -> datetime:
    try:
        return datetime.strptime(input, NGINX_TIME_LOCAL_FMT)
    except Exception:
        raise NginxParseError(message="time local cannot be parsed to a valid date")
