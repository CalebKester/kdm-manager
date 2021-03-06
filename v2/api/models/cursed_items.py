#!/usr/bin/python2.7


from assets import cursed_items
import Models
import utils


class Assets(Models.AssetCollection):

    def __init__(self, *args, **kwargs):
        self.assets = cursed_items.items
        self.type = "cursed_item"
        Models.AssetCollection.__init__(self,  *args, **kwargs)
