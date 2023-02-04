from .order import PorchOrder

#Call de code by run this function
def run(*args, **kwargs):
    #Pass all args or kwargs you send in commad line, in this case only kwargs
    selenium = PorchOrder(**kwargs)
    selenium()
