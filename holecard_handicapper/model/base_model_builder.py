class BaseModelBuilder:
  """
  Concrete class name must be ModelBuilder
  """

  def build(self):
    """
    Concrete class should override this method and return custom model
    """
    raise NotImplementedError("build method is not implemented!!")

