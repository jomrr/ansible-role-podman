# ansible-role-podman

Ansible role for setting up podman.

## Supported Platforms

* Archlinux
* CentOS 7
* Ubuntu 18.04

## Requirements

Ansible 2.7 or higher is recommended.

## Variables

Variables for this role:

| variable | defaults/main.yml | description |
| -------- | ---------------------------------- | ----------- |
| role_podman_enabled | false | determine whether role is enabled (true) or not (false) |
| podman_users | [] | non-root users that can use podman |
| podman_registries | - 'docker.io' | list of registries that podman is pulling images from |
| podman_insecure_registries | [] | non TLS registries for podman, i.e. localhost:5000 |
| podman_blocked_registries | [] | blocked container registries |
| podman_storage_driver | 'overlay' | storage driver |
| podman_storage_mountopt | 'nodev' | storage driver mount options |

## Dependencies

None.

## Example Playbook

```yaml
---
# role: ansible-role-podman
# file: site.yml

- hosts: podman-servers
  vars:
    role_podman_enabled: True
    podman_users:
      - <your-username>
    podman_registries:
      - 'docker.io'
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
