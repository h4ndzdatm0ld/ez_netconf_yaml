EZ NETCONF

This is an updated Nornir Runbook which is taking advantage of Dimitry F. YAML conversion to compile NETCONF XML rpc calls. There is an updated function here which inspects the rpc-reply and sends a netconf_commit rpc call. Committing is necessary when making NETCONF changes to target candidate configurations, such as on Nokia SROS and IOSXR devices.

Thanks to @IPvZero for sharing this and thanks to Dimitry for his 'magic sauce'
