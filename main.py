import sys
from system.start import run as porch_order

from loader.help import HELP_CHARGE

if __name__ == '__main__':
    print("use help to see the instructions for custome charge")
    print("use customfile flag for load data from loader/custome.py")
    base = sys.argv[1]
    kwargs = {}

    if base == 'default':
        print('Running bot "%s" with default arguments "%s"' % (base, kwargs))
    elif base == 'customfile':
          kwargs = {'fromfile':True}
          print('Running bot "%s" with custome file arguments as "%s"' % (base, True))
    elif base == 'customcharge':
        print('Running bot "%s" with custome charge arguments "%s"' % (base, kwargs))
        
        for kwarg in sys.argv[2:]:
            try:
                k, v = kwarg.split('=')
                kwargs[k] = v 
            except ValueError:
                continue
        kwargs['customcharge'] = True

    elif base == 'help':
        print(HELP_CHARGE)
    else:
        raise NotImplementedError(
            "Invalid System. \"%s\" doesn't exists." % base
        )
    
    run = porch_order
    run(**kwargs)