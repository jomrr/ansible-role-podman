# ansible-role-podman

[![Build Status](https://travis-ci.org/jam82/ansible-role-podman.svg?branch=master)](https://travis-ci.org/jam82/ansible-role-podman)

Ansible role for setting up [podman](https://podman.io).

## Supported Platforms

* Archlinux
* CentOS 7
* Ubuntu 18.04

## Requirements

Ansible 2.7 or higher is required for defaults/main/*.yml to work correctly.

## Variables

Variables for this role:

| variable | defaults/main/*.yml | type | description |
| -------- | ------------------- | ---- | ----------- |
| role_podman_enabled | False | boolean | determine whether role is enabled (true) or not (false) |
| podman_users | { root: '100000:65535' } | dictionary | podman users that get uid mapping configured |
| podman_manual_mapping | True | boolean | ansible managed /etc/subuid and /etc/subgid entries |
| podman_search_registries | - 'docker.io' | items | list of registries that podman is pulling images from |
| podman_insecure_registries | [] | items | non TLS registries for podman, i.e. localhost:5000 |
| podman_blocked_registries | [] | items | blocked container registries |
| podman_conf_cgroup_manager | 'systemd' | string | /etc/container/libpod.conf: cgroup_manager |
| podman_conf_events_logger | 'journald' | string | /etc/container/libpod.conf: events_logger |
| podman_conf_namespace | '' | string | /etc/container/libpod.conf: namespace (=default namespace) |
| podman_storage_driver | 'overlay' | string | storage driver |
| podman_storage_mountopt | 'nodev' | string | storage driver mount options |

## Dependencies

None.

## Example Playbook

For a basic setup with default values run:

```yaml
---
# play: example-site
# file: site.yml

- hosts: podman-servers
  vars:
    role_podman_enabled: True
    podman_users:
      root: '100000:65535'
      <user1>: '165536:65535'
      ...
    podman_registries:
      - 'registry.access.redhat.com'
      - 'docker.io'
      - 'registry.fedoraproject.org'
      - 'quay.io'
      - 'registry.centos.org'
  roles:
    - role: ansible-role-podman
```

## License and Author

- Author:: Jonas Mauer (<jam@kabelmail.net>)
- Copyright:: 2019, Jonas Mauer

Licensed under MIT License;
See LICENSE file in repository.

## References

- [libpod Installation Instructions](https://github.com/containers/libpod/blob/master/install.md)
- [podman manpage](https://github.com/containers/libpod/blob/master/docs/podman.1.md)
- [ArchWiki - Linux Containers](https://wiki.archlinux.org/index.php/Linux_Containers)
- [vbatts: centos7 - non-root podman](https://asciinema.org/a/221441)
- [A preview of running containers without root in RHEL 7.6](https://www.redhat.com/en/blog/preview-running-containers-without-root-rhel-76)
