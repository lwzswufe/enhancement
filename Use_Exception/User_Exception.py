# author='lwz'
# coding:utf-8


class NoCodeError(KeyError):
    def __init__(self, err):
        if isinstance(err, str):
            str_ = err
        else:
            str_ = str(err.__class__) + err.__str__()
        self.err_msg = str_

    def __repr__(self):
        return self.err_msg

    def __str__(self):
        return self.err_msg


def task():
    d = {"000001": "平安银行", "600000": "浦发银行"}
    try:
        d["300001"]
    except KeyError as err:
        print("KeyError: ", err)
        msg = "No Code Named :{}".format(err.__str__())
        raise NoCodeError(msg)


def main():
    try:
        task()
    except NoCodeError as err:
        if isinstance(err, str):
            print("err is str")
        print("NoCodeError:", err)

if __name__ == "__main__":
    main()
