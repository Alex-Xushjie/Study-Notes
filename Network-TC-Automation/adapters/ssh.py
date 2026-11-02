class SSHAdapter:
    simulated = False
    def __init__(self, username, password, timeout=30):
        self.username, self.password, self.timeout = username, password, timeout
    def execute(self, device, command):
        self.prompt = self.hostname = ""
        from netmiko import ConnectHandler
        try:
            with ConnectHandler(host=device.host, port=device.port, device_type=device.platform,
                                username=device.username or self.username, password=device.password or self.password,
                                ssh_strict=True, system_host_keys=True, conn_timeout=self.timeout,
                                auth_timeout=self.timeout, banner_timeout=self.timeout) as conn:
                self.prompt = conn.find_prompt().strip()
                self.hostname = self.prompt.strip('<>[]# ').strip()
                output = conn.send_command(command, read_timeout=self.timeout,
                                           strip_prompt=False, strip_command=False)
                # This leading prompt was actually read from the same SSH session.
                return self.prompt + output if output.startswith(command) else self.prompt + '\n' + output
        except Exception as exc:
            # Do not persist connection arguments or credential-bearing exceptions.
            raise RuntimeError(f'SSH {type(exc).__name__}: connection/command failed; check host key, reachability, credentials and timeout') from None

    def configure(self,device,commands):
        """Explicit workflow-only configuration; never used by ordinary query tasks."""
        self.prompt=self.hostname=''
        from netmiko import ConnectHandler
        try:
            with ConnectHandler(host=device.host,port=device.port,device_type=device.platform,
                                username=device.username or self.username,password=device.password or self.password,
                                ssh_strict=True,system_host_keys=True,conn_timeout=self.timeout,
                                auth_timeout=self.timeout,banner_timeout=self.timeout) as conn:
                self.prompt=conn.find_prompt().strip();self.hostname=self.prompt.strip('<>[]# ')
                output=conn.send_config_set(commands,read_timeout=self.timeout,strip_prompt=False,strip_command=False)
                import re
                if re.search(r'(?im)^\s*(%\s*(Invalid|Incomplete|Ambiguous|Error)|Error:|Unrecognized command)',output):
                    raise RuntimeError('Configuration rejected')
                return output
        except Exception as exc:
            raise RuntimeError(f'SSH {type(exc).__name__}: configuration failed; check device and restore state') from None
