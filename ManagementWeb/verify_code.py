from apscheduler.schedulers.background import BackgroundScheduler
import random
import string
import datetime

sh = BackgroundScheduler()

class verify_code_m:
    v_code = []

    def __init__(self):
        self.new_code()
        print('verify_init')

    def new_code(self):
        new_code_m = random.sample(string.ascii_letters + string.digits, random.randint(10, 15))
        new_code_m = "".join(new_code_m)
        print(new_code_m)
        sh.add_job(func=self.del_code, args=(new_code_m,), next_run_time=datetime.datetime.now()
                   + datetime.timedelta(minutes=1), id=new_code_m)
        self.v_code.append(new_code_m)
        return new_code_m

    def del_code(self, code):
        self.v_code.remove(code)

    def is_not_code(self, code):
        if code in self.v_code:
            sh.remove_job(code)
            self.del_code(code)
            return False
        else:
            return True

    def refresh_code(self, code):
        if code in self.v_code:
            sh.remove_job(code)
            self.del_code(code)
            return self.new_code()
        else:
            return 'null'
