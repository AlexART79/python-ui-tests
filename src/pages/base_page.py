class BasePage(object):
    def __init__(self, drv):
        object.__init__(self)
        self.driver = drv

    def go_to(self, url):
        self.driver.get(url)

    def back(self):
        self.driver.back()

    def forward(self):
        self.driver.forward()

    def refresh(self):
        self.driver.refresh()

    @property
    def title(self):
        return self.driver.title

