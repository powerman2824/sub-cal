from flask import Flask, request, render_template_string
import ipaddress

app = Flask(__name__)

HTML_TEMPLATE = """
<!doctype html>
<title>IP Address Calculator</title>
<h1>IP Address Calculator</h1>
<form method=post>
  IP Address: <input name=ip placeholder="192.168.1.0"><br>
  Subnet Mask (CIDR): <input name=cidr placeholder="24"><br>
  <input type=submit value=Calculate>
</form>

{% if result %}
  <h2>Results</h2>
  <ul>
    <li>Network Address: {{ result.network_address }}</li>
    <li>Broadcast Address: {{ result.broadcast_address }}</li>
    <li>First Usable IP: {{ result.first_usable }}</li>
    <li>Last Usable IP: {{ result.last_usable }}</li>
    <li>Total Usable Hosts: {{ result.total_hosts }}</li>
    <li>Next Network: {{ result.next_network }}</li>
    <li>Previous Network: {{ result.prev_network }}</li>
  </ul>
{% endif %}
"""

def calculate_subnet(ip, cidr):
    network = ipaddress.ip_network(f"{ip}/{cidr}", strict=False)
    all_hosts = list(network.hosts())
    total_hosts = len(all_hosts)

    result = {
        "network_address": network.network_address,
        "broadcast_address": network.broadcast_address,
        "first_usable": all_hosts[0] if all_hosts else "N/A",
        "last_usable": all_hosts[-1] if all_hosts else "N/A",
        "total_hosts": total_hosts,
        "next_network": network.network_address + network.num_addresses,
        "prev_network": network.network_address - network.num_addresses
    }
    return result

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        ip = request.form['ip']
        cidr = request.form['cidr']
        try:
            result = calculate_subnet(ip, cidr)
        except ValueError as e:
            result = {"error": str(e)}
    return render_template_string(HTML_TEMPLATE, result=result)

if __name__ == '__main__':
    app.run(debug=True)
