class ModelInterface:
    def get_response(self, messages):
        raise NotImplementedError("This method should be implemented by subclasses")
