from apscheduler.schedulers.background import BackgroundScheduler
import random
import string
import datetime

sh = BackgroundScheduler()


class verify_code_m:
    v_code = {}
    jobs = []

    def __init__(self):
        print('verify_init')

    def new_code(self, openid):
        new_code_m = random.sample(string.ascii_letters + string.digits, random.randint(10, 15))
        new_code_m = "".join(new_code_m)
        print(new_code_m)
        if openid in self.jobs:
            sh.remove_job(openid)
        sh.add_job(func=self.del_code, args=(openid,), next_run_time=datetime.datetime.now()
                                                                     + datetime.timedelta(minutes=30), id=openid)
        self.jobs.append(openid)
        self.v_code[openid] = new_code_m
        return new_code_m

    def del_code(self, openid):
        self.v_code[openid] = None
        self.jobs.remove(openid)

    def is_code(self, openid, code):
        if openid in self.jobs:
            if self.v_code[openid] == code:
                sh.remove_job(openid)
                sh.add_job(func=self.del_code, args=(openid,), next_run_time=datetime.datetime.now()
                                                                             + datetime.timedelta(minutes=30), id=openid)
                return True
        print("true is ", self.v_code[openid], "\t\tfalse is ", code)
        return False
