class ConsoleColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_fail(item):
    print(ConsoleColors.FAIL + str(item) + ConsoleColors.ENDC)


def print_warn(item):
    print(ConsoleColors.WARNING + str(item) + ConsoleColors.ENDC)


def print_ok(item):
    print(ConsoleColors.BOLD + str(item) + ConsoleColors.ENDC)
