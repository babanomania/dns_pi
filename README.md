# The PiHole Ansible Playbook for RaspberryPI

This is an ansible-playbook to setup an raspberry-pi with an pihole running with automatic backup

### Server hardening

- Change the password of the pi user
- Ensure Root cannot login via ssh
- Disable password based login
- Install & enable ufw and fail2ban
- Set default and ssh firewall rules

### Pihole

- Setup pihole via docker containers

### Backups

- Weekly backups of the pihole teleporter data
- Weekly syncing of backups to dropbox
- Ability to restore backups from dropbox
- Telegram updates on backup and sync job completion

## Prerequisites

The following software packages have to be installed on your local machine and the Raspberry Pi.

### On Local System

- [Python 3](https://www.python.org/downloads/)
- [Ansible](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html)
- [Setup SSH key](https://www.makeuseof.com/ssh-keygen-mac/)

### On RaspberryPi

- [Raspberry Pi OS](https://www.raspberrypi.com/software/)
- [Python 3](https://www.python.org/downloads/)
- [Password-less SSH from local system](https://www.tecmint.com/ssh-passwordless-login-using-ssh-keygen-in-5-easy-steps/)

## Steps

1. [Install Ansible](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html). The easiest way (especially on Pi or a Debian system) is via Pip:

```bash
sudo apt-get install -y python3-pip
```

2. Generate an SSH key-pair using ssh-keygen

```bash
ssh-keygen -t rsa
```

3. Setup password-less SSH to your pi

```bash
ssh-copy-id pi@192.168.29.252
```

4. Clone this repository, then enter the repository directory.

```bash
git clone https://github.com/babanomania/vault_pi.git
cd vault_pi
```

5. Install requirements

```bash
ansible-galaxy collection install -r requirements.yml
```

> if you see `ansible-galaxy: command not found`, restart your SSH session or reboot the Pi and try again

6. Make copies of the following files and customize them to your liking:

- `example.inventory.ini` to `inventory.ini` (replace IP address with your Pi's IP, or comment that line and uncomment the `connection=local` line if you're running it on the Pi you're setting up).
- `example.config.yml` to `config.yml`

7. Run the playbook: `ansible-playbook main.yml`

> **If running locally on the Pi**: You may encounter an error like "Error while fetching server API version". If you do, please either reboot or log out and log back in, then run the playbook again.
