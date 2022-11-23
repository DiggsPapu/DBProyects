class InstructorContract:
    def __init__(self,values) -> None:
        self.contract_code = str(values[0])
        self.worker_id = str(values[1])
        self.weight = str(values[2])
        self.height = str(values[3])
    def saveContract(self,cursor):
        cursor.execute('''update instructorcontract set contractinstructorcode = {}, workerid = '{}', weight= {},height= {} '''.format(self.contract_code,self.worker_id,self.weight,self.height))
        cursor.close()