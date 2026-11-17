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

## Limits and the allow-list rule

- **Every Docker network that uses 5442 must be inside 172.16.0.0/12.** Docker's
  default pools can also hand out 192.168.x.x subnets; a container on such a network
  reaching 5442 via host.docker.internal would be silently dropped.
- **Check** (all subnets should be in 172.16.0.0/12 = 172.16–172.31):

      docker network ls -q | xargs docker network inspect -f '{{.Name}} {{range .IPAM.Config}}{{.Subnet}} {{end}}'

- **If one is outside:** add an ACCEPT for that subnet *above* the DROP
  (`sudo iptables -I DOCKER-USER -p tcp -m conntrack --ctorigdstport 5442 -s <subnet> -j ACCEPT`,
  and add it to the unit), or switch the DROP to match the external interfaces
  (the LAN NIC and tailscale0) instead of a source range.
- **IPv4 only.** If 5442 is ever published on IPv6, an `ip6tables` twin is needed.
