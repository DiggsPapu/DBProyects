class UserContract:
    def __init__(self,values) -> None:
        self.contract_code = str(values[0])
        self.user_id = str(values[1])
        self.subscription_type = str(values[2])
        self.last_date = str(values[3])
        self.smart_watch_return = str(values[4])
        self.active_contract = str(values[5])
        self.payment_method = str(values[6])
        self.card_number = str(values[7])
        self.initdate = str(values[8])
    def saveContract(self,cursor):
        cursor.execute('''update usercontract set contractcode = {}, userid = '{}', subscriptionType = '{}', lastDate = '{}', smartwatchreturn = {}, activeContract = {}, paymentmethod = '{}', cardnumber = '{}', initdate = '{}' '''.format(self.contract_code, self.user_id, self.subscription_type, self.last_date, self.smart_watch_return, self.active_contract, self.payment_method, self.card_number, self.initdate))
        cursor.close()