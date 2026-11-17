# egeria-pg-firewall.service (TR-28)

Shared Postgres (5442) is published on 0.0.0.0 so containers can reach it via
host.docker.internal. This unit adds a `DOCKER-USER` rule that drops 5442 traffic
from anything outside the Docker subnets (172.16.0.0/12), e.g. LAN or Tailscale.
The rule is idempotent and is removed when the unit stops. It must be re-applied
after boot because `iptables -I` is not persistent.

Install (needs sudo, run in a real terminal):

    sudo install -m 644 egeria-pg-firewall.service /etc/systemd/system/
    sudo systemctl daemon-reload && sudo systemctl enable --now egeria-pg-firewall.service
    sudo iptables -S DOCKER-USER      # expect exactly one DROP line for 5442

Verify from a host outside the Docker subnets: `nc -zv -w3 <host-ip> 5442` should time out.
Local connections on the host itself bypass DOCKER-USER, so test from another machine.
