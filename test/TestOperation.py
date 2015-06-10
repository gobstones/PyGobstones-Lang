class TestOperation(object):
  def __init__(self, nretvals, code, replace={}):
    self.nretvals = nretvals
    for k, v in replace.items():
      code = code.replace('@' + k, str(v))
    self.code = code