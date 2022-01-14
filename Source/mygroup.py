from pygame.sprite import Group


class ContainerGroup(Group):

    def __init__(self, *sprites):
        super().__init__(self, *sprites)
        self._sprites = []

    def store_permanent(self):
        for sp in self:
            self._sprites.append(sp)

    def iter_store(self):
        for sp in self._sprites:
            yield sp
