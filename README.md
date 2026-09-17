# Ansible Role: podman

![GitHub](https://img.shields.io/github/license/jomrr/ansible-role-podman)
![GitHub last commit](https://img.shields.io/github/last-commit/jomrr/ansible-role-podman)
![GitHub issues](https://img.shields.io/github/issues-raw/jomrr/ansible-role-podman)
[![dev](https://img.shields.io/github/actions/workflow/status/jomrr/ansible-role-podman/dev.yml?branch=dev&label=dev)](https://github.com/jomrr/ansible-role-podman/actions/workflows/dev.yml?query=branch%3Adev)
[![main](https://img.shields.io/github/actions/workflow/status/jomrr/ansible-role-podman/main.yml?branch=main&label=main)](https://github.com/jomrr/ansible-role-podman/actions/workflows/main.yml?query=branch%3Amain)

Install Podman and manage engine, storage, registry and rootless account
configuration.

## Purpose

Install Podman and optionally manage engine, storage, registry and image alias
configuration.
The role is idempotent: repeated runs with unchanged inputs preserve the managed
state.

## Scope

### Managed

- Distribution Podman packages and rootless UID mapping tools.
- System engine, storage and registry configuration when podman_configure is
  true.
- Explicit subordinate ID assignments and engine configuration for existing
  accounts, including service accounts below UID 1000.

### Not Managed

- Container workloads, registry authentication, user creation and storage
  migration.
- Backing filesystem provisioning and SELinux labeling of custom storage paths.

## Requirements

- Podman 3 or newer from the supported distribution packages; libpod.conf is no
  longer used.
- Selected accounts must exist. Subordinate ID ranges must not overlap
  allocations belonging to other accounts.
- Btrfs, ZFS and AUFS require a compatible backing filesystem and kernel
  support. Custom storage paths on SELinux hosts need appropriate container
  storage labels.

## Dependencies

```yaml
collections:
  - name: ansible.posix
  - name: community.general
    version: '>=12.0.0'
  - name: containers.podman
```

## Role Variables

### `podman_configure`

Type: `bool`. Required: `false`.

Manage system and selected rootless user configuration files.

Default:

```yaml
podman_configure: false
```

### `podman_conf_cgroup_manager`

Type: `str`. Required: `false`.

Cgroup manager for the system engine configuration.

Default:

```yaml
podman_conf_cgroup_manager: systemd
```

### `podman_conf_events_logger`

Type: `str`. Required: `false`.

Event logger for system and managed rootless engines.

Default:

```yaml
podman_conf_events_logger: file
```

### `podman_conf_namespace`

Type: `str`. Required: `false`.

Container namespace for system and managed rootless engines.

Default:

```yaml
podman_conf_namespace: ''
```

### `podman_user_cgroup_manager`

Type: `str`. Required: `false`.

Cgroup manager for managed non-root accounts.

Default:

```yaml
podman_user_cgroup_manager: cgroupfs
```

### `podman_storage_driver`

Type: `str`. Required: `false`.

Storage driver; its backing filesystem must already support the driver.

Default:

```yaml
podman_storage_driver: overlay
```

### `podman_storage_mountopt`

Type: `str`. Required: `false`.

Default overlay mount options; storage_options can override them.

Default:

```yaml
podman_storage_mountopt: nodev
```

### `podman_storage_graphroot`

Type: `str`. Required: `false`.

Directory for persistent rootful container storage.

Default:

```yaml
podman_storage_graphroot: /var/lib/containers/storage
```

### `podman_storage_runroot`

Type: `str`. Required: `false`.

Directory for temporary rootful container storage.

Default:

```yaml
podman_storage_runroot: /run/containers/storage
```

### `podman_storage_rootless_path`

Type: `str`. Required: `false`.

Rootless storage path with native environment variable expansion.

Default:

```yaml
podman_storage_rootless_path: $HOME/.local/share/containers/storage
```

### `podman_storage_options`

Type: `dict`. Required: `false`.

Native storage.options values and driver-specific subtables.

Default:

```yaml
podman_storage_options: {}
```

### `podman_search_registries`

Type: `list`. Required: `false`.

Ordered registries used to resolve unqualified image names.

Default:

```yaml
podman_search_registries:
  - docker.io
```

### `podman_insecure_registries`

Type: `list`. Required: `false`.

Legacy registry locations allowing HTTP or unverified TLS.

Default:

```yaml
podman_insecure_registries: []
```

### `podman_blocked_registries`

Type: `list`. Required: `false`.

Legacy registry locations blocked for image pulls.

Default:

```yaml
podman_blocked_registries: []
```

### `podman_registries`

Type: `list`. Required: `false`.

Native registry definitions; matching locations override legacy lists.

Default:

```yaml
podman_registries: []
```

### `podman_registry_aliases`

Type: `dict`. Required: `false`.

Short image names mapped to fully qualified names without tags or digests.

Default:

```yaml
podman_registry_aliases: {}
```

### `podman_short_name_mode`

Type: `str`. Required: `false`.

Policy for resolving image names without an explicit registry or alias.

Default:

```yaml
podman_short_name_mode: enforcing
```

### `podman_users`

Type: `dict`. Required: `false`.

Existing account names mapped to subordinate ID ranges in start:count form.

Default:

```yaml
podman_users: {}
```

### `podman_manual_mapping`

Type: `bool`. Required: `false`.

Manage the explicitly listed subordinate UID and GID assignments.

Default:

```yaml
podman_manual_mapping: true
```

## Managed Files

- `/etc/containers/containers.conf`
- `/etc/containers/storage.conf`
- `/etc/containers/storage.rootless.conf.d/00-ansible.conf`
- `/etc/containers/registries.conf`
- `/etc/containers/registries.conf.d/99-ansible.conf`
- `/etc/subuid and /etc/subgid: only explicitly selected account entries`
- `~/.config/containers/containers.conf for selected non-root accounts`

## Check Mode

Tasks support Ansible check mode. A fresh host still needs packages installed
before Podman functionality can be exercised.

## Service Behavior

Podman is daemonless and reads configuration on invocation. The role does not
restart container workloads.

## Security Notes

- TLS verification remains enabled unless a registry or mirror is explicitly
  marked insecure.
- Unrelated subordinate ID entries are preserved; no root or lxd range is added
  implicitly.

## Operational Notes

- podman_configure defaults to false and gates both system and rootless
  configuration files. Explicit mappings are controlled independently by
  podman_manual_mapping.
- podman_users defaults to an empty mapping. Disabling mapping management or
  removing an account from that mapping leaves existing assignments intact.
- podman_registries accepts native registries.conf keys, including mirror and
  mirror-by-digest-only. A custom location overrides the legacy insecure/blocked
  lists for that location.
- Registry settings are also written to 99-ansible.conf so distribution drop-ins
  sorted before it do not override configured search registries or aliases.
  Later drop-ins can override these settings.
- Native storage.options keys and nested driver tables are accepted in
  podman_storage_options. Values override the default overlay mountopt setting.
- Rootless storage paths use the legacy rootless_storage_path field for Podman
  3-5 and a rootless drop-in for Podman 6. Podman 6 may report a deprecation
  warning for the legacy field during rootful invocations.
- Changing drivers or storage paths does not migrate or reset existing container
  data. Changing subordinate IDs for active rootless engines may require podman
  system migrate after stopping affected workloads.
- Machine-generated short-name alias caches can override configured aliases.
  Existing per-user registries.conf and storage.conf files are left intact.
  Podman 6 system drop-ins can override values in these base files; user
  drop-ins sorted later can override the managed settings.
- Engine and storage candidates are parsed by Podman before installation.
  Registry files are serialized as TOML; registry behavior is verified through
  functional Molecule tests because no side-effect-free candidate validator has
  been established.

## Supported Platforms

| OS Family | Distribution | Version | Container Image |
| --------- | ------------ | ------- | --------------- |
| RedHat | AlmaLinux | latest | [jomrr/molecule-almalinux:latest](https://hub.docker.com/r/jomrr/molecule-almalinux) |
| Debian | Debian | latest | [jomrr/molecule-debian:latest](https://hub.docker.com/r/jomrr/molecule-debian) |
| RedHat | Fedora | latest | [jomrr/molecule-fedora:latest](https://hub.docker.com/r/jomrr/molecule-fedora) |
| Suse | OpenSuse Leap | latest | [jomrr/molecule-opensuse-leap:latest](https://hub.docker.com/r/jomrr/molecule-opensuse-leap) |
| Suse | OpenSuse Tumbleweed | latest | [jomrr/molecule-opensuse-tumbleweed:latest](https://hub.docker.com/r/jomrr/molecule-opensuse-tumbleweed) |
| Debian | Ubuntu | latest | [jomrr/molecule-ubuntu:latest](https://hub.docker.com/r/jomrr/molecule-ubuntu) |

## Example Playbook

### Storage, custom registry and image aliases

```yaml
---
- name: Configure Podman
  hosts: containers
  gather_facts: true
  roles:
    - role: jomrr.podman
      podman_configure: true
      podman_storage_driver: overlay
      podman_storage_options:
        overlay:
          mount_program: /usr/bin/fuse-overlayfs
      podman_registries:
        - prefix: images.example.org/team
          location: registry.example.org/team
          mirror:
            - location: mirror.example.org/team
      podman_registry_aliases:
        app: images.example.org/team/app
      podman_users:
        containers: "200000:65536"
```

## References

- [Podman configuration](https://docs.podman.io/en/stable/markdown/podman.1.html)
- [Storage configuration](https://github.com/containers/storage/blob/main/docs/containers-storage.conf.5.md)
- [Registries and aliases](https://github.com/containers/image/blob/main/docs/containers-registries.conf.5.md)

## Author

[Jonas Mauer](https://github.com/jomrr)

## License

This project is licensed under the MIT License.
See [LICENSE](LICENSE) for the full license text.

Copyright (c) 2019-2026 Jonas Mauer.
