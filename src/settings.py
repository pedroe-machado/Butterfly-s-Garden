class Settings:
    def __init__(self):
        # Screen settings
        self.screen_width = 608
        self.screen_height = 416
        self.bg_color = (230, 230, 230)  # Light gray

        # Frame rate
        self.fps = 60

        # Other settings can be added here as needed
    
    @property
    def WIDTH(self):
        return self.screen_width
    
    @property
    def HEIGHT(self):
        return self.screen_height