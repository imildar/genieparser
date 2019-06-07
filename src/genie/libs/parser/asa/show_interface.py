''' show_interface.py

ASA parserr for the following show commands:
    * show interface summary
    * show interface ip brief
    * show interface details
'''


# Python
import re

# Metaparser
from genie.metaparser import MetaParser
from genie.metaparser.util.schemaengine import Schema, Any, Optional


# =============================================
# Schema for 'show interface summary'
# =============================================
class ShowInterfaceSummarySchema(MetaParser):
    """Schema for
        * show interface summary
    """

    schema = {
        'interfaces': {
            Any(): {
                'link_status': str,
                'line_protocol': str,
                Optional('name'): str,
                Optional('mac_address'): str,
                Optional('mtu'): int,
                Optional('ipv4'): {
                    Any(): { 
                        Optional('ip'): str,
                        Optional('prefix_length'): str
                    }
                },
                Optional('subnet'): str,
                Optional('interface_state'): bool,
                Optional('config_status'): bool,
                Optional('config_issue'): str
            },
        }
    }

# =============================================
# Parser for 'show interface summary'
# =============================================
class ShowInterfaceSummary(ShowInterfaceSummarySchema):
    """Parser for
        * show interface summary
    """

    cli_command = 'show interface summary'

    def cli(self, output=None):
        if output is None:
            # excute command to get output
            out = self.device.execute(self.cli_command)
        else:
            out = output

        ret_dict = {}

        # Interface Vlan1000 "pod100", is up, line protocol is up
        p1 = re.compile(r'^Interface +(?P<interface>\w+) +"(?P<name>[\w\-\+\/\_]*)"'
            ', +is +(?P<link_status>up|down), +line +protocol +is '
            '+(?P<line_protocol>up|down)$')

        # MAC address 286f.7fb1.032c, MTU 1500
        p2 = re.compile(r'^MAC address +(?P<mac_address>[\w\.]+), +MTU +(?P<mtu>\d+)$')

        # IP address 172.16.100.251, subnet mask 255.255.255.0
        p3 = re.compile(r'^IP +address +(?P<ip>[a-z0-9\.]+)'
            '(\/(?P<prefix_length>[0-9]+))?, +subnet +mask '
            '+(?P<subnet>[\w\.]+)$')

        # Available but not configured via nameif
        p4 = re.compile(r'^(?P<interface_state>Available) +but '
            '+(?P<config_status>not +configured) +via '
            '+(?P<config_issue>[\w\-\+\/\_]*)$')

        for line in out.splitlines():
            line = line.strip()

            # Interface Vlan1000 "pod100", is up, line protocol is up
            m = p1.match(line)
            if m:
                groups = m.groupdict()
                interface = groups['interface']
                instance_dict = ret_dict.setdefault('interfaces', {}). \
                    setdefault(interface, {})
                instance_dict.update({'name': groups['name']})
                instance_dict.update({'link_status': groups['link_status']})
                instance_dict.update(
                    {'line_protocol': groups['line_protocol']})
                if groups['name'] != '' \
                and groups['link_status'] == 'up' \
                and groups['line_protocol'] == 'up':
                    instance_dict.update({'interface_state': True, \
                        'config_status': True})
                if groups['name'] != '' \
                and groups['link_status'] == 'down' \
                and groups['line_protocol'] == 'down':
                    instance_dict.update({'interface_state': False, \
                        'config_status': True})
                if groups['name'] == '' \
                and groups['link_status'] == 'down' \
                and groups['line_protocol'] == 'down':
                    instance_dict.update({'interface_state': False, \
                        'config_status': False})
                continue

            # MAC address 286f.7fb1.032c, MTU 1500
            m = p2.match(line)
            if m:
                groups = m.groupdict()
                instance_dict.update({'mac_address': groups['mac_address']})
                instance_dict.update({'mtu': int(groups['mtu'])})
                continue

            # IP address 172.16.100.251, subnet mask 255.255.255.0
            m = p3.match(line)
            if m:
                groups = m.groupdict()
                ipv4 = groups['ip']
                if groups['prefix_length'] is not None:
                    address = groups['ip'] + '/' + groups['prefix_length']
                dict_ipv4 = instance_dict.setdefault('ipv4', {}).setdefault(ipv4, {})
                dict_ipv4.update({'ip': groups['ip']})
                if groups['prefix_length'] is not None:
                    dict_ipv4.update({'prefix_length': groups['prefix_length']})                
                instance_dict.update({'subnet': groups['subnet']})
                continue

            # Available but not configured via nameif
            m = p4.match(line)
            if m:
                groups = m.groupdict()
                if groups['interface_state'] == 'Available' \
                and groups['config_status'] == 'not configured':
                    instance_dict.update({'interface_state': True})
                    instance_dict.update({'config_status': False})
                    instance_dict.update({'config_issue': groups['config_issue']})
                continue

        return ret_dict

# =============================================
# Schema for 'show interface ip brief'
# =============================================
class ShowInterfaceIpBriefSchema(MetaParser):
    """Schema for
        * show interface ip brief
    """

    schema = {
        'interfaces': {
            Any(): {
                Optional('ipv4'): {
                    Any(): { 
                        Optional('ip'): str,
                        Optional('prefix_length'): str
                    },
                    Optional('unnumbered'): {
                        Optional('unnumbered_intf_ref'): str
                    }
                },
                'check': str,
                'method': str,
                'link_status': str,
                'line_protocol': str
                },
            }
        }

# =============================================
# Parser for 'show interface ip brief'
# =============================================
class ShowInterfaceIpBrief(ShowInterfaceIpBriefSchema):
    """Parser for
        * show interface ip brief
    """

    cli_command = 'show interface ip brief'
    def cli(self,output=None):
        if output is None:
            # excute command to get output
            out = self.device.execute(self.cli_command)
        else:
            out = output

        ret_dict = {}

        # Vlan1000 172.16.100.251 YES CONFIG up up
        p1 = re.compile(r'^(?P<interface>\w+) +(?P<ip>[a-z0-9\.]+)'
            '(\/(?P<prefix_length>[0-9]+))? '
            '+(?P<check>\w+) +(?P<method>\w+) +(?P<link_status>up|down) '
            '+(?P<line_protocol>up|down)$')

        for line in out.splitlines():
            line = line.strip()

        # Vlan1000 172.16.100.251 YES CONFIG up up
            m = p1.match(line)
            if m:
                groups = m.groupdict()
                interface = groups['interface']
                instance_dict = ret_dict.setdefault('interfaces', {}). \
                    setdefault(interface, {})
                if groups['ip'] == 'unassigned':
                    dict_unnumbered = instance_dict.setdefault('ipv4', {}). \
                    setdefault('unnumbered', {})
                    dict_unnumbered.update({'unnumbered_intf_ref': groups['ip']})
                else:
                    ipv4 = groups['ip']
                    if groups['prefix_length'] is not None:
                        address = groups['ip'] + '/' + groups['prefix_length']
                    dict_ipv4 = instance_dict.setdefault('ipv4', {}). \
                    setdefault(ipv4, {})
                    dict_ipv4.update({'ip': groups['ip']})
                    if groups['prefix_length'] is not None:
                        dict_ipv4.update({'prefix_length': groups['prefix_length']})
                instance_dict.update({'check': groups['check']})
                instance_dict.update({'method': groups['method']})
                instance_dict.update({'link_status': groups['link_status']})
                instance_dict.update({'line_protocol': groups['line_protocol']})
                continue

        return ret_dict

# =============================================
# Schema for 'show interface detail'
# =============================================
class ShowInterfaceDetailSchema(MetaParser):
    """Schema for
        * show interface detail
    """

    schema = {
        'interfaces': {
            Any(): {
                'link_status': str,
                'line_protocol': str,
                Optional('name'): str,
                Optional('mac_address'): str,
                Optional('mtu'): int,
                Optional('ipv4'): {
                    Any(): { 
                        Optional('ip'): str,
                        Optional('prefix_length'): str
                    },
                },
                Optional('subnet'): str,
                Optional('interface_state'): bool,
                Optional('config_status'): bool,
                Optional('config_issue'): str,
                Optional('traffic_statistics'): {
                    'packets_input': int,
                    'bytes_input': int,
                    'packets_output': int,
                    'bytes_output': int,
                    'packets_dropped': int
                },
                Optional('control_point_states'): {
                    'interface': {
                        'interface_number': int,
                        'interface_config_status': str,
                        'interface_state': str
                    },
                    Any():{
                        'interface_vlan_config_status': str,
                        'interface_vlan_state': str
                    },
                }
            },
        }
    }

# =============================================
# Parser for 'show interface detail'
# =============================================
class ShowInterfaceDetail(ShowInterfaceDetailSchema):
    """Parser for
        * show interface detail
    """

    cli_command = 'show interface detail'

    def cli(self, output=None):
        if output is None:
            # excute command to get output
            out = self.device.execute(self.cli_command)
        else:
            out = output

        ret_dict = {}

        # Interface Vlan1000 "pod100", is up, line protocol is up
        p1 = re.compile(r'^Interface +(?P<interface>\w+) ' \
            '+"(?P<name>[\w\-\+\/\_]*)", +is +(?P<link_status>up|down), ' \
            '+line +protocol +is +(?P<line_protocol>up|down)$')

        # MAC address 286f.7fb1.032c, MTU 1500
        p2 = re.compile(r'^MAC address +(?P<mac_address>[\w\.]+), +MTU +(?P<mtu>\d+)$')

        # IP address 172.16.100.251, subnet mask 255.255.255.0
        p3 = re.compile(r'^IP +address +(?P<ip>[a-z0-9\.]+)'
            '(\/(?P<prefix_length>[0-9]+))?, +subnet +mask '
            '+(?P<subnet>[\w\.]+)$')

        # Available but not configured via nameif
        p4 = re.compile(r'^(?P<interface_state>Available) +but '
            '+(?P<config_status>not +configured) +via '
            '+(?P<config_issue>[\w\-\+\/\_]*)$')

        # 16863445 packets input, 10312133394 bytes
        p5 = re.compile(r'^(?P<packets_input>[\d]+) +packets +input, '
            '+(?P<bytes_input>[\d]+) +bytes$')

        # 10475426 packets output, 5376026271 bytes
        p6 = re.compile(r'^(?P<packets_output>[\d]+) +packets +output, '
            '+(?P<bytes_output>[\d]+) +bytes$')

        # 2551519 packets dropped
        p7 = re.compile(r'^(?P<packets_dropped>[\d]+) +packets +dropped$')

        # Interface number is 756
        p8 = re.compile(r'^Interface +number +is +(?P<interface_number>[\d]+)$')

        # Interface config status is active
        # Interface config status is not active
        p9 = re.compile(r'^Interface +config +status +is +(?P<interface_config_status>[\w\ ]+)$')

        # Interface state is active
        # Interface state is not active           
        p10 = re.compile(r'^Interface +state +is +(?P<interface_state>[\w\ ]+)$')

        # Interface vlan config status is active
        # Interface vlan config status is not active
        p11 = re.compile(r'^Interface +vlan +config +status +is '
            '+(?P<interface_vlan_config_status>[\w\ ]+)$')

        # Interface vlan state is UP
        # Interface vlan state is DOWN (down in system space)
        p12 = re.compile(r'^Interface +vlan +state +is +(?P<interface_vlan_state>[\w]+)+([\w\(\)\ ]+)?$')

        for line in out.splitlines():
            line = line.strip()

            # Interface Vlan1000 "pod100", is up, line protocol is up
            m = p1.match(line)
            if m:
                groups = m.groupdict()
                interface = groups['interface']
                instance_dict = ret_dict.setdefault('interfaces', {}). \
                    setdefault(interface, {})
                instance_dict.update({'name': groups['name']})
                instance_dict.update({'link_status': groups['link_status']})
                instance_dict.update(
                    {'line_protocol': groups['line_protocol']})
                if groups['name'] != '' \
                and groups['link_status'] == 'up' \
                and groups['line_protocol'] == 'up':
                    instance_dict.update({'interface_state': True, \
                        'config_status': True})
                if groups['name'] != '' \
                and groups['link_status'] == 'down' \
                and groups['line_protocol'] == 'down':
                    instance_dict.update({'interface_state': False, \
                        'config_status': True})
                if groups['name'] == '' \
                and groups['link_status'] == 'down' \
                and groups['line_protocol'] == 'down':
                    instance_dict.update({'interface_state': False, \
                        'config_status': False})
                continue

            # MAC address 286f.7fb1.032c, MTU 1500
            m = p2.match(line)
            if m:
                groups = m.groupdict()
                instance_dict.update({'mac_address': groups['mac_address']})
                instance_dict.update({'mtu': int(groups['mtu'])})
                continue

            # IP address 172.16.100.251, subnet mask 255.255.255.0
            m = p3.match(line)
            if m:
                groups = m.groupdict()
                ipv4 = groups['ip']
                if groups['prefix_length'] is not None:
                    address = groups['ip'] + '/' + groups['prefix_length']
                dict_ipv4 = instance_dict.setdefault('ipv4', {}).setdefault(ipv4, {})
                dict_ipv4.update({'ip': groups['ip']})
                if groups['prefix_length'] is not None:
                    dict_ipv4.update({'prefix_length': groups['prefix_length']})                
                instance_dict.update({'subnet': groups['subnet']})
                continue

            # Available but not configured via nameif
            m = p4.match(line)
            if m:
                groups = m.groupdict()
                if groups['interface_state'] == 'Available' \
                and groups['config_status'] == 'not configured':
                    instance_dict.update({'interface_state': True})
                    instance_dict.update({'config_status': False})
                    instance_dict.update({'config_issue': groups['config_issue']})
                continue

            # 16863445 packets input, 10312133394 bytes
            m = p5.match(line)
            if m:
                groups = m.groupdict()
                dict_traffic = instance_dict.setdefault('traffic_statistics', {})
                dict_traffic.update({'packets_input': \
                    int(groups['packets_input'])})
                dict_traffic.update({'bytes_input': \
                    int(groups['bytes_input'])})
                continue

            # 10475426 packets output, 5376026271 bytes
            m = p6.match(line)
            if m:
                groups = m.groupdict()
                dict_traffic.update({'packets_output': \
                    int(groups['packets_output'])})
                dict_traffic.update({'bytes_output': \
                    int(groups['bytes_output'])})
                continue

            # 2551519 packets dropped
            m = p7.match(line)
            if m:
                groups = m.groupdict()
                dict_traffic.update({'packets_dropped': \
                    int(groups['packets_dropped'])})
                continue

            # Interface number is 756
            m = p8.match(line)
            if m:
                groups = m.groupdict()
                dict_control = instance_dict.setdefault('control_point_states', {})
                dict_interface = dict_control.setdefault('interface', {})
                dict_interface.update({'interface_number': \
                    int(groups['interface_number'])})
                continue

            # Interface config status is active
            # Interface config status is not active
            m = p9.match(line)
            if m:
                groups = m.groupdict()
                dict_interface.update({'interface_config_status': groups['interface_config_status']})
                continue

            # Interface state is active
            # Interface state is not active                     
            m = p10.match(line)
            if m:
                groups = m.groupdict()
                dict_interface.update({'interface_state': groups['interface_state']})
                continue

            # Interface vlan config status is active
            # Interface vlan config status is not active
            m = p11.match(line)
            if m:
                groups = m.groupdict()
                dict_vlan = dict_control.setdefault(interface, {})
                dict_vlan.update({'interface_vlan_config_status': groups['interface_vlan_config_status']})
                continue

            # Interface vlan state is UP
            # Interface vlan state is DOWN (down in system space)
            m = p12.match(line)
            if m:
                groups = m.groupdict()
                dict_vlan.update({'interface_vlan_state': groups['interface_vlan_state']})
                continue

        return ret_dict