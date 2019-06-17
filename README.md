# ansible-role-podman

Ansible role for setting up podman.

## Requirements

Ansible 2.7 or higher is recommended.

## Variables

Variables for this

| variable | default value in defaults/main.yml | description |
| -------- | ---------------------------------- | ----------- |
| role_podman_enabled | false | determine whether role is enabled (true) or not (false) |

## Dependencies

None.

## Example Playbook

```yaml
---
# file: site.yml

- hosts: podman-servers
  roles:
    - role: ansible-role-podman
```

## License and Author

- Author:: Jonas Mauer (<jam@kabelmail.net>)
- Copyright:: 2019, Jonas Mauer

Licensed under MIT License;
See LICENSE file in repository.
