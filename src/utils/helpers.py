from time import sleep


def wait_for(cond, timeout, delay):
    itr = int(timeout/delay)
    for i in range(1, itr):
        if cond():
            return True
        else:
            sleep(delay)

    return False