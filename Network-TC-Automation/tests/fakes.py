class MockAdapter:
    simulated = True
    def execute(self, device, command):
        return f'[SIMULATED] {device.id}\n> {command}\nVersion demo 1.0\nInterface UP\n'
