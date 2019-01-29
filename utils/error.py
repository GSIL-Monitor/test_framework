# coding = utf-8


class Sqlerror(IOError):
    pass


try:
    raise Sqlerror("Bad hostname")
except Sqlerror as e:
    print(e)