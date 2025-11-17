#https://stackoverflow.com/questions/372042/difference-between-abstract-class-and-interface-in-python
class AbstractService:
    def validate_input(self):
        raise NotImplementedError("Should have implemented this")
