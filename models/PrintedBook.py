class PrintedBook:
    def __init__(self, status, address, changed=False):
        self.status = status
        self.address = address
        self.changed = changed
        
    def to_dict(self):
        return {
            'status': self.status,
            'address': self.address,
            'changed': self.changed
        }
