from Connection.ConectDB import connectAdmin


class Worker:
    def __init__(self, values) -> None:
        self.worker_id = str(values[0])
        self.worker_password = str(values[1])
        self.worker_name = str(values[2])
        self.worker_direction = str(values[3])
        self.worker_type = str(values[4])
        self.cursor = connectAdmin(self.worker_id,self.worker_password)