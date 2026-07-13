import ipaddress
import unittest
from datetime import datetime, timezone

from nginx_log_parser import NginxLog, NginxRequest, parse_line


class TestParse(unittest.TestCase):
    def test_parse_line(self):
        input = '172.17.0.1 - - [06/Aug/2024:16:37:59 +0000] "GET / HTTP/1.1" 200 615 "-" "Mozilla/5.0 (X11;Linux x86_64; rv:12.8.0) Gecko/20100101 Firefox/128.0"'
        got = parse_line(input)
        expected = NginxLog(
            remote_addr=ipaddress.ip_address("172.17.0.1"),
            remote_user="-",
            time_local=datetime(
                year=2024,
                month=8,
                day=6,
                hour=16,
                minute=37,
                second=59,
                tzinfo=timezone.utc,
            ),
            request=NginxRequest("GET", "/", "HTTP/1.1"),
            status=200,
            bytes_sent=615,
            http_referer="-",
            http_user_agent="Mozilla/5.0 (X11;Linux x86_64; rv:12.8.0) Gecko/20100101 Firefox/128.0",
        )

        print(got)

        self.assertEqual(got.remote_addr, expected.remote_addr)
        self.assertEqual(got.remote_user, expected.remote_user)
        self.assertEqual(got.time_local, expected.time_local)
        self.assertEqual(got.request, expected.request)
        self.assertEqual(got.status, expected.status)
        self.assertEqual(got.bytes_sent, expected.bytes_sent)
        self.assertEqual(got.http_referer, expected.http_referer)
        self.assertEqual(got.http_user_agent, expected.http_user_agent)
        # self.assertEqual(got.request, expected.request)


if __name__ == "__main__":
    unittest.main()
