class UpdateHandler:
    def __init__(self):
        self.updatable_objects = []

    def add_object(self, obj):
        self.updatable_objects.append(obj)

    def update_all(self):
        for obj in self.updatable_objects:
            obj.update()


updateHandler = UpdateHandler()
