import re

from genie.metaparser import MetaParser
from genie.metaparser.util.schemaengine import Any, Optional


# ==============================
# Schema for:
#  * 'show wlan id client stats'
# ==============================
class ShowWlanIdClientStatsSchema(MetaParser):
    """Schema for show wlan id client stats."""

    schema = {}


# ==============================
# Parser for:
#  * 'show wlan id client stats'
# ==============================
class ShowWlanIdClientStats(ShowWlanIdClientStatsSchema):
    """Parser for show wlan id client stats"""

    cli_command = "show wlan id client stats"

    def cli(self, output=None):
        if output is None:
            output = self.device.execute(self.cli_command)

        else:
            output = output

        wlan_capture = (
            # Wlan Profile Name: lizzard_Global, Wlan Id: 17
            r"^Wlan Profile Name:\s+(?P<profile_name>\S+), Wlan Id: (?P<id>\d+)$"
        )

        # Current client state statistics:
        client_stats_capture = (
            r"^"
            #   Authenticating         : 7
            r"\s+Authenticating\s+:\s+(?P<auth>\d+)\s+"
            #   Mobility               : 0
            r"\s+Mobility\s+:\s+(?P<mobility>\d+)\s+"
            #   IP Learn               : 0
            r"\s+IP Learn\s+:\s+(?P<ip_learn>\d+)\s+"
            #   Webauth Pending        : 0
            r"\s+Webauth Pending\s+:\s+(?P<webauth>\d+)\s+"
            #   Run                    : 2
            r"\s+Run\s+:\s+(?P<run>\d+)\s+"
        )

        # Total client delete reasons
        client_delete_capture = (
            r"^"
            # No Operation                                                    : 0
            r"\s+No Operation\s+:\s+(?P<no_operation>\d+)\s+"
            # Internal error                                                  : 0
            r"\s+Internal error\s+:\s+(?P<internal_error>\d+)\s+"
            # Deauthentication or disassociation request                      : 0
            r"\s+Deauthentication or disassociation request\s+:\s+(?P<deauth_request>\d+)\s+"
            # Session Manager                                                 : 0
            r"\s+Session Manager\s+:\s+(?P<session_manager>\d+)\s+"
            # L3 authentication failure                                       : 0
            r"\s+L3 authentication failure\s+:\s+(?P<l3_auth_fail>\d+)\s+"
            # Delete received from AP                                         : 0
            r"\s+Delete received from AP\s+:\s+(?P<delete_from_ap>\d+)\s+"
            # BSSID down                                                      : 1
            r"\s+BSSID down\s+:\s+(?P<bssid_down>\d+)\s+"
            # AP down/disjoin                                                 : 2
            r"\s+AP down/disjoin\s+:\s+(?P<ap_down>\d+)\s+"
            # Connection timeout                                              : 0
            r"\s+Connection timeout\s+:\s+(?P<connection_timeout>\d+)\s+"
            # MAC authentication failure                                      : 0
            r"\s+MAC authentication failure\s+:\s+(?P<mac_auth_fail>\d+)\s+"
            # Datapath plumb                                                  : 0
            r"\s+Datapath plumb\s+:\s+(?P<datapath_plumb>\d+)\s+"
            # Due to SSID change                                              : 163
            r"\s+Due to SSID change\s+:\s+(?P<ssid_change>\d+)\s+"
            # Due to VLAN change                                              : 0
            r"\s+Due to VLAN change\s+:\s+(?P<vlan_change>\d+)\s+"
            # Due to IP Zone change                                              : 0
            r"\s+Due to IP Zone change\s+:\s+(?P<ip_zone_change>\d+)\s+"
            # Admin deauthentication                                          : 0
            r"\s+Admin deauthentication\s+:\s+(?P<admin_deauth>\d+)\s+"
            # QoS failure                                                     : 0
            r"\s+QoS failure\s+:\s+(?P<qos_fail>\d+)\s+"
            # WPA key exchange timeout                                        : 13
            r"\s+WPA key exchange timeout\s+:\s+(?P<wpa_key_timeout>\d+)\s+"
            # WPA group key update timeout                                    : 101
            r"\s+WPA group key update timeout\s+:\s+(?P<wpa_groupkey_timeout>\d+)\s+"
            # 802.11w MAX SA queries reached                                  : 0
            r"\s+802.11w MAX SA queries reached\s+:\s+(?P<dot11w_max_sa>\d+)\s+"
            # Client deleted during HA recovery                               : 0
            r"\s+Client deleted during HA recovery\s+:\s+(?P<ha_recovery>\d+)\s+"
            # Client blacklist                                                : 0
            r"\s+Client blacklist\s+:\s+(?P<blacklist>\d+)\s+"
            # Inter instance roam failure                                     : 0
            r"\s+Inter instance roam failure\s+:\s+(?P<roam_fail>\d+)\s+"
            # Due to mobility failure                                         : 0
            r"\s+Due to mobility failure\s+:\s+(?P<mobility_fail>\d+)\s+"
            # Session timeout                                                 : 2
            r"\s+Session timeout\s+:\s+(?P<session_timeout>\d+)\s+"
            # Idle timeout                                                    : 0
            r"\s+Idle timeout\s+:\s+(?P<idle_timeout>\d+)\s+"
            # Supplicant request                                              : 25
            r"\s+Supplicant request\s+:\s+(?P<supplicant_request>\d+)\s+"
            # NAS error                                                       : 0
            r"\s+NAS error\s+:\s+(?P<nas_error>\d+)\s+"
            # Policy Manager internal error                                   : 0
            r"\s+Policy Manager internal error\s+:\s+(?P<policy_manager_error>\d+)\s+"
            # Mobility WLAN down                                              : 0
            r"\s+Mobility WLAN down\s+:\s+(?P<mobility_wlan_down>\d+)\s+"
            # Mobility tunnel down                                            : 0
            r"\s+Mobility tunnel down\s+:\s+(?P<mobility_tunnel_down>\d+)\s+"
            # 80211v smart roam failed                                        : 0
            r"\s+80211v smart roam failed\s+:\s+(?P<dot11v_smart_roam_fail>\d+)\s+"
            # DOT11v timer timeout                                            : 0
            r"\s+DOT11v timer timeout\s+:\s+(?P<dot11v_timer_timeout>\d+)\s+"
            # DOT11v association failed                                       : 0
            r"\s+DOT11v association failed \s+:\s+(?P<dot11v_association_fail>\d+)\s+"
            # DOT11r pre-authentication failure                               : 0
            r"\s+DOT11r pre-authentication failure\s+:\s+(?P<dot11v_preauth_fail>\d+)\s+"
            # SAE authentication failure                                      : 0
            r"\s+SAE authentication failure\s+:\s+(?P<dot11_sae_auth_fail>\d+)\s+"
            # DOT11 failure                                                   : 0
            r"\s+DOT11 failure \s+:\s+(?P<dot11_fail>\d+)\s+"
            # DOT11 SAE invalid message                                       : 0
            r"\s+DOT11 SAE invalid message\s+:\s+(?P<dot11_sae_invalid>\d+)\s+"
            # DOT11 unsupported client capabilities                           : 0
            r"\s+DOT11 unsupported client capabilities\s+:\s+(?P<dot11_unsupported_client>\d+)\s+"
            # DOT11 association denied unspecified                            : 0
            r"\s+DOT11 association denied unspecified\s+:\s+(?P<dot11_denied_unspecified>\d+)\s+"
            # DOT11 max STA                                                   : 0
            r"\s+DOT11 max STA\s+:\s+(?P<dot11_max_sta>\d+)\s+"
            # DOT11 denied data rates                                         : 0
            r"\s+DOT11 denied data rates\s+:\s+(?P<dot11_denied_data_rates>\d+)\s+"
            # 802.11v Client RSSI lower than the association RSSI threshold   : 0
            r"\s+802.11v Client RSSI lower than the association RSSI threshold\s+:\s+(?P<dot11v_rssi_low_threshold>\d+)\s+"
            # invalid QoS parameter                                           : 0
            r"\s+invalid QoS parameter\s+:\s+(?P<qos_invalid_parameter>\d+)\s+"
            # DOT11 IE validation failed                                      : 0
            r"\s+DOT11 IE validation failed\s+:\s+(?P<dot11_ie_validation_failed>\d+)\s+"
            # DOT11 group cipher in IE validation failed                      : 0
            r"\s+DOT11 group cipher in IE validation failed\s+:\s+(?P<dot11_groupcipher_validation_failed>\d+)\s+"
            # DOT11 invalid pairwise cipher                                   : 0
            r"\s+DOT11 invalid pairwise cipher\s+:\s+(?P<dot11_invalid_pairwise_cipher>\d+)\s+"
            # DOT11 invalid AKM                                               : 0
            r"\s+DOT11 invalid AKM \s+:\s+(?P<dot11_invalid_akm>\d+)\s+"
            # DOT11 unsupported RSN version                                   : 0
            r"\s+DOT11 unsupported RSN version\s+:\s+(?P<dot11_unsupported_rsn_version>\d+)\s+"
            # DOT11 invalid RSNIE capabilities                                : 0
            r"\s+DOT11 invalid RSNIE capabilities\s+:\s+(?P<dot11_invalid_rsnie_capabilities>\d+)\s+"
            # DOT11 received invalid PMKID in the received RSN IE             : 74
            r"\s+DOT11 received invalid PMKID in the received RSN IE\s+:\s+(?P<dot11_invalid_pkmid>\d+)\s+"
            # DOT11 invalid MDIE                                              : 0
            r"\s+DOT11 invalid MDIE\s+:\s+(?P<dot11_invalid_mdie>\d+)\s+"
            # DOT11 invalid FT IE                                             : 0
            r"\s+DOT11 invalid FT IE\s+:\s+(?P<dot11_invalid_ft_ie>\d+)\s+"
            # DOT11 QoS policy                                                : 0
            r"\s+DOT11 QoS policy\s+:\s+(?P<dot11_qos_policy>\d+)\s+"
            # DOT11 AP have insufficient bandwidth                            : 0
            r"\s+DOT11 AP have insufficient bandwidth\s+:\s+(?P<dot11_ap_insufficient_bandwidth>\d+)\s+"
            # DOT11 invalid QoS parameter                                     : 0
            r"\s+DOT11 invalid QoS parameter\s+:\s+(?P<dot11_invalid_qos_parameter>\d+)\s+"
            # Client not allowed by assisted roaming                          : 0
            r"\s+Client not allowed by assisted roaming\s+:\s+(?P<not_allowed_roaming>\d+)\s+"
            # IAPP disassociation for wired client                            : 0
            r"\s+IAPP disassociation for wired client\s+:\s+(?P<iapp_disassociate_wired>\d+)\s+"
            # Wired WGB change                                                : 0
            r"\s+Wired WGB change\s+:\s+(?P<wired_wgb_change>\d+)\s+"
            # Wired VLAN change                                               : 0
            r"\s+Wired VLAN change\s+:\s+(?P<wired_vlan_change>\d+)\s+"
            # Wired client deleted due to WGB delete                          : 0
            r"\s+Wired client deleted due to WGB delete\s+:\s+(?P<wired_wgb_delete>\d+)\s+"
            # AVC client re-anchored at the foreign controller                : 0
            r"\s+AVC client re-anchored at the foreign controller\s+:\s+(?P<avc_client_reanchor>\d+)\s+"
            # WGB Wired client joins as a direct wireless client              : 0
            r"\s+WGB Wired client joins as a direct wireless client\s+:\s+(?P<wired_wbg_joins>\d+)\s+"
            # AP upgrade                                                      : 0
            r"\s+AP upgrade\s+:\s+(?P<ap_upgrade>\d+)\s+"
            # Client DHCP                                                     : 0
            r"\s+Client DHCP\s+:\s+(?P<client_dhcp>\d+)\s+"
            # Client EAP timeout                                              : 0
            r"\s+Client EAP timeout\s+:\s+(?P<client_eap_timeout>\d+)\s+"
            # Client 8021x failure                                            : 0
            r"\s+Client 8021x failure\s+:\s+(?P<client_auth_8021x_fail>\d+)\s+"
            # Client device idle                                              : 0
            r"\s+Client device idle\s+:\s+(?P<client_device_idle>\d+)\s+"
            # Client captive portal security failure                          : 0
            r"\s+Client captive portal security failure\s+:\s+(?P<client_captive_portal_fail>\d+)\s+"
            # Client decryption failure                                       : 0
            r"\s+Client decryption failure \s+:\s+(?P<client_decrypt_fail>\d+)\s+"
            # Client interface disabled                                       : 0
            r"\s+Client interface disabled\s+:\s+(?P<client_int_disable>\d+)\s+"
            # Client user triggered disassociation                            : 0
            r"\s+Client user triggered disassociation\s+:\s+(?P<client_trigger_disassociate>\d+)\s+"
            # Client miscellaneous reason                                     : 0
            r"\s+Client miscellaneous reason\s+:\s+(?P<client_misc_reason>\d+)\s+"
            # Unknown                                                         : 0
            r"\s+Unknown\s+:\s+(?P<unknown>\d+)\s+"
            # Client peer triggered                                           : 0
            r"\s+Client peer triggered\s+:\s+(?P<client_peer_trigger>\d+)\s+"
            # Client beacon loss                                              : 0
            r"\s+Client beacon loss\s+:\s+(?P<client_beacon_loss>\d+)\s+"
            # Client EAP ID timeout                                           : 10928
            r"\s+Client EAP ID timeout\s+:\s+(?P<client_eap_id_timeout>\d+)\s+"
            # Client DOT1x timeout                                            : 0
            r"\s+Client DOT1x timeout\s+:\s+(?P<client_dot1x_timeout>\d+)\s+"
            # Malformed EAP key frame                                         : 0
            r"\s+Malformed EAP key frame\s+:\s+(?P<eap_bad_keyframe>\d+)\s+"
            # EAP key install bit is not expected                             : 0
            r"\s+EAP key install bit is not expected\s+:\s+(?P<eap_key_install_unexpected>\d+)\s+"
            # EAP key error bit is not expected                               : 0
            r"\s+EAP key error bit is not expected\s+:\s+(?P<eap_key_error_unexpected>\d+)\s+"
            # EAP key ACK bit is not expected                                 : 0
            r"\s+EAP key ACK bit is not expected\s+:\s+(?P<eap_key_ack_unexpected>\d+)\s+"
            # Invalid key type                                                : 0
            r"\s+Invalid key type\s+:\s+(?P<eap_invalid_key_type>\d+)\s+"
            # EAP key secure bit is not expected                              : 0
            r"\s+EAP key secure bit is not expected\s+:\s+(?P<eap_key_secure_unexected>\d+)\s+"
            # key description version mismatch                                : 0
            r"\s+key description version mismatch\s+:\s+(?P<eap_key_version_mismatch>\d+)\s+"
            # wrong replay counter                                            : 1
            r"\s+wrong replay counter\s+:\s+(?P<wrong_replay_counter>\d+)\s+"
            # EAP key MIC bit expected                                        : 0
            r"\s+EAP key MIC bit expected\s+:\s+(?P<eap_key_mic_expected>\d+)\s+"
            # MIC validation failed                                           : 7
            r"\s+MIC validation failed\s+:\s+(?P<eap_mic_validation_failed>\d+)\s+"
            # Error while PTK computation                                     : 0
            r"\s+Error while PTK computation\s+:\s+(?P<ptk_error>\d+)\s+"
            # Incorrect credentials                                           : 16
            r"\s+Incorrect credentials\s+:\s+(?P<bad_credentials>\d+)\s+"
            # Client connection lost                                          : 0
            r"\s+Client connection lost\s+:\s+(?P<client_connection_lost>\d+)\s+"
            # Reauthentication failure                                        : 0
            r"\s+Reauthentication failure\s+:\s+(?P<reauthentication_fail>\d+)\s+"
            # Port admin disabled                                             : 0
            r"\s+Port admin disabled\s+:\s+(?P<port_admin_disabled>\d+)\s+"
            # Supplicant restart                                              : 0
            r"\s+Supplicant restart\s+:\s+(?P<supplicant_restart>\d+)\s+"
            # No IP                                                           : 93
            r"\s+No IP\s+:\s+(?P<no_ip>\d+)\s+"
            # Call admission controller at anchor node                        : 0
            r"\s+Call admission controller at anchor node\s+:\s+(?P<anchor_call_admission_controller>\d+)\s+"
            # Anchor no memory                                                : 0
            r"\s+Anchor no memory\s+:\s+(?P<anchor_no_memory>\d+)\s+"
            # Anchor invalid Mobility BSSID                                   : 0
            r"\s+Anchor invalid Mobility BSSID\s+:\s+(?P<anchor_invalid_mobility_bssid>\d+)\s+"
            # Anchor creation failure                                         : 0
            r"\s+Anchor creation failure\s+:\s+(?P<anchor_create_fail>\d+)\s+"
            # DB error                                                        : 0
            r"\s+DB error\s+:\s+(?P<db_error>\d+)\s+"
            # Wired client cleanup due to WGB roaming                         : 0
            r"\s+Wired client cleanup due to WGB roaming\s+:\s+(?P<cleanup_wgb_roam>\d+)\s+"
            # Manually excluded                                               : 0
            r"\s+Manually excluded\s+:\s+(?P<manually_excluded>\d+)\s+"
            # 802.11 association failure                                      : 0
            r"\s+802.11 association failure\s+:\s+(?P<dot11_assocation_fail>\d+)\s+"
            # 802.11 authentication failure                                   : 0
            r"\s+802.11 authentication failure\s+:\s+(?P<dot11_auth_fail>\d+)\s+"
            # 802.1X authentication timeout                                   : 0
            r"\s+802.1X authentication timeout\s+:\s+(?P<dot11x_auth_timeout>\d+)\s+"
            # 802.1X authentication credential failure                        : 0
            r"\s+802.1X authentication credential failure\s+:\s+(?P<dot11x_credential_fail>\d+)\s+"
            # Web authentication failure                                      : 0
            r"\s+Web authentication failure\s+:\s+(?P<web_auth_fail>\d+)\s+"
            # Policy bind failure                                             : 0
            r"\s+Policy bind failure\s+:\s+(?P<policy_bind_fail>\d+)\s+"
            # IP theft                                                        : 0
            r"\s+IP theft\s+:\s+(?P<ip_theft>\d+)\s+"
            # MAC theft                                                       : 0
            r"\s+MAC theft\s+:\s+(?P<mac_theft>\d+)\s+"
            # MAC and IP theft                                                : 0
            r"\s+MAC and IP theft\s+:\s+(?P<mac_ip_theft>\d+)\s+"
            # QoS policy failure                                              : 0
            r"\s+QoS policy failure\s+:\s+(?P<qos_policy_fail>\d+)\s+"
            # QoS policy send to AP failure                                   : 0
            r"\s+QoS policy send to AP failure\s+:\s+(?P<qos_send_ap_fail>\d+)\s+"
            # QoS policy bind on AP failure                                   : 0
            r"\s+QoS policy bind on AP failure\s+:\s+(?P<qos_bind_ap_fail>\d+)\s+"
            # QoS policy unbind on AP failure                                 : 0
            r"\s+QoS policy unbind on AP failure\s+:\s+(?P<qos_unbind_ap_fail>\d+)\s+"
            # Static IP anchor discovery failure                              : 0
            r"\s+Static IP anchor discovery failure\s+:\s+(?P<anchor_static_ip_fail>\d+)\s+"
            # VLAN failure                                                    : 0
            r"\s+VLAN failure\s+:\s+(?P<vlan_fail>\d+)\s+"
            # ACL failure                                                     : 0
            r"\s+ACL failure\s+:\s+(?P<acl_fail>\d+)\s+"
            # Redirect ACL failure                                            : 2
            r"\s+Redirect ACL failure\s+:\s+(?P<redirect_acl_fail>\d+)\s+"
            # Accounting failure                                              : 0
            r"\s+Accounting failure\s+:\s+(?P<accounting_fail>\d+)\s+"
            # Security group tag failure                                      : 0
            r"\s+Security group tag failure\s+:\s+(?P<security_grouptag_fail>\d+)\s+"
            # FQDN filter definition does not exist                           : 0
            r"\s+FQDN filter definition does not exist\s+:\s+(?P<fqdn_filter_missing>\d+)\s+"
            # Wrong filter type, expected postauth FQDN filter                : 0
            r"\s+Wrong filter type, expected postauth FQDN filter\s+:\s+(?P<fqdn_wrong_postauth_filter>\d+)\s+"
            # Wrong filter type, expected preauth FQDN filter                 : 0
            r"\s+Wrong filter type, expected preauth FQDN filter\s+:\s+(?P<fqdn_wrong_preauth_filter>\d+)\s+"
            # Invalid group id for FQDN filter valid range  1..16             : 0
            r"\s+Invalid group id for FQDN filter valid range  1..16\s+:\s+(?P<fqdn_invalid_group_id>\d+)\s+" #HEY
            # Policy parameter mismatch                                       : 0
            r"\s+Policy parameter mismatch\s+:\s+(?P<policy_manager_mismatch>\d+)\s+"
            # Reauth failure                                                  : 0
            r"\s+Reauth failure\s+:\s+(?P<reauth_fail>\d+)\s+"
            # Wrong PSK                                                       : 0
            r"\s+Wrong PSK\s+:\s+(?P<wrong_psk>\d+)\s+"
            # Policy failure                                                  : 0
            r"\s+Policy failure\s+:\s+(?P<policy_fail>\d+)\s+"
            # AP initiated delete for idle timeout                            : 164
            r"\s+AP initiated delete for idle timeout\s+:\s+(?P<apinit_idle_timeout>\d+)\s+"
            # AP initiated delete for client ACL mismatch                     : 0
            r"\s+AP initiated delete for client ACL mismatch\s+:\s+(?P<apinit_acl_mismatch>\d+)\s+"
            # AP initiated delete for AP auth stop                            : 0
            r"\s+AP initiated delete for AP auth stop\s+:\s+(?P<apinit_auth_stop>\d+)\s+"
            # AP initiated delete for association expired at AP               : 0
            r"\s+AP initiated delete for association expired at AP\s+:\s+(?P<apinit_association_expired>\d+)\s+"
            # AP initiated delete for 4-way handshake failed                  : 0
            r"\s+AP initiated delete for 4-way handshake failed\s+:\s+(?P<apinit_4way_fail>\d+)\s+"
            # AP initiated delete for DHCP timeout                            : 0
            r"\s+AP initiated delete for DHCP timeout\s+:\s+(?P<apinit_dhcp_timeout>\d+)\s+"
            # AP initiated delete for reassociation timeout                   : 0
            r"\s+AP initiated delete for reassociation timeout\s+:\s+(?P<apinit_reassocation_timeout>\d+)\s+"
            # AP initiated delete for SA query timeout                        : 0
            r"\s+AP initiated delete for SA query timeout\s+:\s+(?P<apinit_sa_timeout>\d+)\s+"
            # AP initiated delete for channel switch at AP                    : 0
            r"\s+AP initiated delete for channel switch at AP\s+:\s+(?P<apinit_channel_switch>\d+)\s+"
            # AP initiated delete for bad AID                                 : 0
            r"\s+AP initiated delete for bad AID\s+:\s+(?P<apinit_bad_aid>\d+)\s+"
            # AP initiated delete for request                                 : 0
            r"\s+AP initiated delete for request\s+:\s+(?P<apinit_request>\d+)\s+"
            # AP initiated delete for interface reset                         : 0
            r"\s+AP initiated delete for interface reset\s+:\s+(?P<apinit_interface_reset>\d+)\s+"
            # AP initiated delete for all on slot                             : 0
            r"\s+AP initiated delete for all on slot\s+:\s+(?P<apinit_all_slot>\d+)\s+"
            # AP initiated delete for reaper radio                            : 0
            r"\s+AP initiated delete for reaper radio\s+:\s+(?P<apinit_reaper_radio>\d+)\s+"
            # AP initiated delete for slot disable                            : 0
            r"\s+AP initiated delete for slot disable\s+:\s+(?P<apinit_slot_disable>\d+)\s+"
            # AP initiated delete for MIC failure                             : 0
            r"\s+AP initiated delete for MIC failure\s+:\s+(?P<apinit_mic_fail>\d+)\s+"
            # AP initiated delete for VLAN delete                             : 0
            r"\s+AP initiated delete for VLAN delete\s+:\s+(?P<apinit_vlan_delete>\d+)\s+"
            # AP initiated delete for channel change                          : 0
            r"\s+AP initiated delete for channel change\s+:\s+(?P<apinit_channel_change>\d+)\s+"
            # AP initiated delete for stop reassociation                      : 0
            r"\s+AP initiated delete for stop reassociation\s+:\s+(?P<apinit_stop_reassociation>\d+)\s+"
            # AP initiated delete for packet max retry                        : 0
            r"\s+AP initiated delete for packet max retry\s+:\s+(?P<apinit_max_retry>\d+)\s+"
            # AP initiated delete for transmission deauth                     : 0
            r"\s+AP initiated delete for transmission deauth\s+:\s+(?P<apinit_transmission_deauth>\d+)\s+"
            # AP initiated delete for sensor station timeout                  : 0
            r"\s+AP initiated delete for sensor station timeout\s+:\s+(?P<apinit_sensor_station_timeout>\d+)\s+"
            # AP initiated delete for age timeout                             : 0
            r"\s+AP initiated delete for age timeout\s+:\s+(?P<apinit_age_timeout>\d+)\s+"
            # AP initiated delete for transmission fail threshold             : 0
            r"\s+AP initiated delete for transmission fail threshold\s+:\s+(?P<apinit_transmission_fail_threshold>\d+)\s+"
            # AP initiated delete for uplink receive timeout                  : 0
            r"\s+AP initiated delete for uplink receive timeout\s+:\s+(?P<apinit_uplink_recieve_timeout>\d+)\s+"
            # AP initiated delete for sensor scan next radio                  : 0
            r"\s+AP initiated delete for sensor scan next radio\s+:\s+(?P<apinit_scan_next_radio>\d+)\s+"
            # AP initiated delete for sensor scan other BSSID                 : 0
            r"\s+AP initiated delete for sensor scan other BSSID\s+:\s+(?P<apinit_scan_other_bssid>\d+)\s+"
            # AAA server unavailable                                          : 0
            r"\s+AAA server unavailable\s+:\s+(?P<aaa_unavailable>\d+)\s+"
            # AAA server not ready                                            : 0
            r"\s+AAA server not ready\s+:\s+(?P<aaa_not_ready>\d+)\s+"
            # No dot1x method configuration                                   : 0
            r"\s+No dot1x method configuration\s+:\s+(?P<dot1x_no_config>\d+)\s+"
            # Client Abort                                                    : 0
            r"\s+Client Abort\s+:\s+(?P<client_abort>\d+)\s+"
            # Association connection timeout                                  : 0
            r"\s+Association connection timeout\s+:\s+(?P<connection_timeout_assocation>\d+)\s+"
            # MAC-AUTH connection timeout                                     : 0
            r"\s+MAC-AUTH connection timeout\s+:\s+(?P<connection_timeout_macauth>\d+)\s+"
            # L2-AUTH connection timeout                                      : 882
            r"\s+L2-AUTH connection timeout\s+:\s+(?P<connection_timeout_l2auth>\d+)\s+"
            # L3-AUTH connection timeout                                      : 0
            r"\s+L3-AUTH connection timeout\s+:\s+(?P<connection_timeout_l3auth>\d+)\s+"
            # Mobility connection timeout                                     : 0
            r"\s+Mobility connection timeout\s+:\s+(?P<connection_timeout_mobility>\d+)\s+"
            # static IP connection timeout                                    : 0
            r"\s+static IP connection timeout\s+:\s+(?P<connection_timeout_static_ip>\d+)\s+"
            # SM session creation timeout                                     : 0
            r"\s+SM session creation timeout\s+:\s+(?P<connection_timeout_sm_session_creation>\d+)\s+"
            # IP-LEARN connection timeout                                     : 25
            r"\s+IP-LEARN connection timeout\s+:\s+(?P<connection_timeout_iplearn>\d+)\s+"
            # NACK IFID exists                                                : 0
            r"\s+NACK IFID exists\s+:\s+(?P<nack_ifid_exists>\d+)\s+"
            # Radio Down                                                      : 0
            r"\s+Radio Down\s+:\s+(?P<radio_down>\d+)\s+"
            # EoGRE Reset                                                     : 0
            r"\s+EoGRE Reset\s+:\s+(?P<eogre_reset>\d+)\s+"
            # EoGRE Generic Join Failure                                      : 0
            r"\s+EoGRE Generic Join Failure\s+:\s+(?P<eogre_generic_join_fail>\d+)\s+"
            # EoGRE HA-Reconciliation                                         : 0
            r"\s+EoGRE HA-Reconciliation\s+:\s+(?P<eogre_ha_reconcile>\d+)\s+"
            # EoGRE Invalid VLAN                                              : 0
            r"\s+EoGRE Invalid VLAN\s+:\s+(?P<eogre_invalid_vlan>\d+)\s+"
            # EoGRE Invalid Domain                                            : 0
            r"\s+EoGRE Invalid Domain\s+:\s+(?P<eogre_invalid_domain>\d+)\s+"
            # EoGRE Empty Domain                                              : 0
            r"\s+EoGRE Empty Domain\s+:\s+(?P<eogre_empty_domain>\d+)\s+"
            # EoGRE Domain Shut                                               : 0
            r"\s+EoGRE Domain Shut\s+:\s+(?P<eogre_domain_shut>\d+)\s+"
            # EoGRE Invalid Gateway                                           : 0
            r"\s+EoGRE Invalid Gateway\s+:\s+(?P<eogre_invalid_gateway>\d+)\s+"
            # EoGRE All Gateways down                                         : 0
            r"\s+EoGRE All Gateways down\s+:\s+(?P<eogre_all_gateways_down>\d+)\s+"
            # EoGRE Flex - no active gateway                                  : 0
            r"\s+EoGRE Flex - no active gateway\s+:\s+(?P<eogre_flex_no_gateway>\d+)\s+"
            # EoGRE Rule Matching error                                       : 0
            r"\s+EoGRE Rule Matching error\s+:\s+(?P<eogre_rule_error>\d+)\s+"
            # EoGRE AAA Override error                                        : 0
            r"\s+EoGRE AAA Override error\s+:\s+(?P<eogre_aaa_override_error>\d+)\s+"
            # EoGRE client onboarding error                                   : 0
            r"\s+EoGRE client onboarding error\s+:\s+(?P<eogre_onboarding_error>\d+)\s+"
            # EoGRE Mobility Handoff error                                    : 0
            r"\s+EoGRE Mobility Handoff error\s+:\s+(?P<eogre_mobility_handoff_error>\d+)\s+"
            # IP Update timeout                                               : 0
            r"\s+IP Update timeout\s+:\s+(?P<ip_update_timeout>\d+)\s+"
            # L3 VLAN Override connection timeout                         : 0
            r"\s+L3 VLAN Override connection timeout\s+:\s+(?P<connection_timeout_l3vlan_override>\d+)\s+"
            # Mobility peer delete                                            : 0
            r"\s+Mobility peer delete\s+:\s+(?P<mobility_peer_delete>\d+)\s+"
            # NACK IFID mismatch                                              : 0
            r"\s+NACK IFID mismatch\s+:\s+(?P<nack_ifid_mismatch>\d+)\s+"
        )

        wlan_obj = {}

        if re.search(wlan_capture, output, re.MULTILINE):
            search = re.search(wlan_capture, output, re.MULTILINE)
            group = search.groupdict()

            new_group = {"wlan": group}
            wlan_obj.update(new_group)

        if re.search(client_stats_capture, output, re.MULTILINE):
            search = re.search(client_stats_capture, output, re.MULTILINE)
            group = search.groupdict()

            new_group = {"client_stats": group}
            wlan_obj.update(new_group)

        if re.search(client_delete_capture, output, re.MULTILINE):
            search = re.search(client_delete_capture, output, re.MULTILINE)
            group = search.groupdict()

            new_group = {"client_delete": group}

            key_list = [
                "anchor",
                "apinit",
                "client",
                "connection_timeout",
                "dot11",
                "dot11v",
                "eap",
                "eogre",
                "fqdn",
                "mac",
                "mobility",
                "policy",
                "qos",
                "wired",
            ]

            for key in key_list: 
                new_key_group = {key: {}}

                for item in new_group["client_delete"].copy():
                    # if the key from key_list is found in item
                    if re.search(f"^{key}_", item):
                        # replace the key and update with new_dict
                        new_key = re.sub(f"^{key}_", "", item)
                        new_dict = {new_key: new_group["client_delete"][item]}

                        new_key_group[key].update(new_dict)
                        new_group["client_delete"].pop(item)

                new_group["client_delete"].update(new_key_group)
            
            wlan_obj.update(new_group)

        return(wlan_obj)