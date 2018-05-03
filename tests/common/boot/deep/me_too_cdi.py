from pycdi import Producer


@Producer(str, _context='me_too')
def producer():
    return __name__
