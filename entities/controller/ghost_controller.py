class GhostController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def update(self, scaled_delta_time: float) -> None:
        self.model.update_physics()
        self.view.update_animation(scaled_delta_time)
