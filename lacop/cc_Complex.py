
class CAPcAMP:
    """
    cap camp complex class handles cap camp interactions and functions
    """

    def __init__(self, status):
        """
        :param status: a string of "active" or "Inactive"
        """
        if status == "Inactive":
            self.status = False
        else:
            self.status = True

    def get_status(self, glucose):
        """
        returns status of cap camp complex
        :params glucose: glucose level value
        """
        if glucose > 100:
            return False
        if glucose <= 100:
            return self.status
