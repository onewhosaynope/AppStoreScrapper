from threading import Timer


class RepeatedTimer(object):
    def __init__(self, interval, function, *args, **kwargs):
        self._timer     = None
        self.interval   = interval
        self.function   = function
        self.args       = args
        self.kwargs     = kwargs
        self.is_running = False
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False


def check(familyname):
    suffixes = ['ov', 'ova', 'aya', 'ev', 'eva', 
    'in', 'ina', 'sky', 'skaya', 'ykh', 'qızı',
    'yan', 'ian',
    'vych', 'chuk', 'enko', 'ko', 'ka', 'shyn', 'uk'] 
    return familyname.endswith(tuple(suffixes))


def check_custom(familyname, suffix): 
    return familyname.endswith(suffix)


def fix_price(price):
    if price.get('amount') == '0.00000':
        cost = "FREE"
    else:
        cost = str(price.get('amount')[:-3] + price.get('currency'))
    return cost


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'