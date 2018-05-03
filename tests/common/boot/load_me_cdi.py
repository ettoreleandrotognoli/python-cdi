from pycdi import Producer


@Producer(str, _context='load_me')
def producer():
    return __name__
