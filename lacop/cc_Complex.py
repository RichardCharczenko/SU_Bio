
class CAPcAMP:

    def __init__(self, status):
        if status == "Inactive":
            self.status = False
        else:
            self.status = True

    def get_status(self, glucose):
        if glucose > 100:
            return False
        if glucose <= 100:
            return self.status
