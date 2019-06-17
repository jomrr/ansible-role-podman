import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_podman(host):
    cmd = host.run("podman run hello-world")

    assert cmd.rc == 0
    assert 'Hello from Docker!' in cmd.stdout
