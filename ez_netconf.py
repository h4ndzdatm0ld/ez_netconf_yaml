"""
This script is a slight modification of original work
created by Dmitry Figol - https://github.com/dmfigol/nornir-apps
"""

from nornir import InitNornir
from nornir_scrapli.tasks import netconf_edit_config, netconf_commit
from nornir_utils.plugins.functions import print_result
from nornir.core.task import Result
from lxml import etree
from ruamel.yaml import YAML
from dimitry_netconf import nojinja
import xmltodict
import json


def rpc_check_commit(task):
    """Validate if 'OK' from rpc-reply.
    This value is stored into a dict from edit_nc_config_from_yaml."""

    rpcreply = task.host["rpc-reply"]

    data = xmltodict.parse(rpcreply)
    reply = json.loads(json.dumps(data))

    if "ok" in reply["rpc-reply"]:
        commit = netconf_commit(task)
        return commit
    else:
        return f"Nothing to commit: {rpcreply}"


def edit_nc_config_from_yaml(task):
    with open(f"host_vars/{task.host}.yml") as f:
        yaml = YAML(typ="safe")
        data = yaml.load(f)
        xml = nojinja.dict_to_xml(data, root="config")
        xml_str = etree.tostring(xml).decode("utf-8")
        result = task.run(
            task=netconf_edit_config, target=task.host["target"], config=xml_str
        )
        # Capture the rpc-reply from the netconf server
        task.host["rpc-reply"] = result.result

        return Result(host=task.host, result=result.result)


def main():
    nr = InitNornir(config_file="config.yml")

    results = nr.run(task=edit_nc_config_from_yaml)
    commit = nr.run(task=rpc_check_commit)

    print_result(results)
    print_result(commit)


if __name__ == "__main__":
    main()
