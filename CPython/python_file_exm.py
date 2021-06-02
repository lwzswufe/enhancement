# author='lwz'

def python_function_exm(a):
    print("python get:{}".format(a))
    return a + 100


class String(object):
    def __init__(self):
        self.string = "py"
        # print("initial: {}".format(s))
    
    def __add__(self, s=""):
        if isinstance(s, String):
            self.string += s.string
        elif isinstance(s, str):
            self.string += s
        else:
            raise TypeError("error type {}".format(type(s)))
    
    def __str__(self):
        return self.string
    
    def print(self, s=''):
        return self.string + s


if __name__ == "__main__":
    print("run {}".format(__file__))
    s = String()
