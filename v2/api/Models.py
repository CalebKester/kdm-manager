#!/usr/bin/python2.7

from bson.objectid import ObjectId
from copy import copy

from flask import Response

import utils

#
#   Base classes for game assets are here. Also, special exceptions for those
#       classes live here as well.
#


class AssetInitError(Exception):
    """ Handler for asset-based errors. """

    def __init__(self, message="An error occurred while initializing this asset!"):
        self.logger = utils.get_logger()
        self.logger.exception(message)
        Exception.__init__(self, message)

class AssetLoadError(Exception):
    """ Handler for asset-based errors. """

    def __init__(self, message="Asset could not be retrieved from mdb!"):
        self.logger = utils.get_logger()
        self.logger.exception(message)
        Exception.__init__(self, message)


class AssetCollection():
    """ The base class for game asset objects, i.e. working with the dict assets
    in the assets/ folder.

    Each model in the models/ folder should have a method that subclasses this
    base class.

    All asset objects that use this as their base class MUST define their own
    self.assets dict (preferably in their __init__() method). """

    def __init__(self):
        """ sets misc attributes of the collection's assets dict. """
        self.logger = utils.get_logger()
        for a in self.assets.keys():
            self.assets[a]["handle"] = a
            if hasattr(self, "type"):
                self.assets[a]["type"] = self.type

    def get_handles(self):
        """ Dumps all asset handles, i.e. the list of self.assets keys. """
        return self.assets.keys()

    def get_names(self):
        """ Dumps all asset 'name' attributes, i.e. a list of name values. """
        return [self.assets[k]["name"] for k in self.assets.keys()]

    def get_asset(self, handle):
        """ Return an asset dict based on a handle. Return None if the handle
        cannot be retrieved. """
        try:
            asset = self.assets[handle]
            if not "handle" in asset.keys():
                asset["handle"] = handle
            return asset
        except:
            return None

    def get_asset_from_name(self, name, case_sensitive=False):
        """ Tries to return an asset dict by looking up "name" attributes within
        the self.assets. dict. Returns None if it fails.

        By default, the mactching here is NOT case-sensitive: everything is
        forced to upper() to allow for more permissive matching/laziness. """

        name = name.strip()
        if not case_sensitive:
            name = name.upper()

        name_lookup = {}
        for a in self.assets.keys():
            if "name" in self.assets[a]:
                if case_sensitive:
                    name_lookup[self.assets[a]["name"]] = a
                elif not case_sensitive:
                    asset_name_upper = self.assets[a]["name"].upper()
                    name_lookup[asset_name_upper] = a

        if name in name_lookup.keys():
            return self.get_asset(name_lookup[name])
        else:
            return None


class GameAsset():
    """ The base class for initializing individual game asset objects. All of
    the specific models in the models/ folder will sub-class this model for
    their generally available methods, etc.

    """

    def __init__(self, handle=None, name=None):

        # initialize basic vars
        self.logger = utils.get_logger()
        self.name = name
        self.handle = handle


    def initialize(self):
        """ Call this method to initialize the object. """

        if self.handle is not None:
            self.initialize_from_handle()
        elif self.name is not None:
            self.initialize_from_name()
        elif handle is None and name is None:
            raise AssetInitError("Asset objects must be initialized with 'handle' or 'name' kwargs.")
        else:
            raise AssetInitError()


    def initialize_asset(self, asset_dict):
        """ Pass this a valid asset dictionary to set the object's attributes
        with a bunch of exec calls. """

        if type(asset_dict) != dict:
            raise AssetInitError("Asset objects may not be initialized with a '%s' type object!" % type(asset_dict))

        for k, v in asset_dict.iteritems():
            if type(v) == str:
                exec """self.%s = "%s" """ % (k,v)
            else:
                exec "self.%s = %s" % (k,v)


    def initialize_from_handle(self):
        """ If we've got a not-None handle, we can initiailze the asset object
        by checking self.assets to see if our handle is a valid key.
        If we can't find a valid key, throw an exception. """

        # sanity warning
        if " " in self.handle:
            self.logger.warn("Asset handle '%s' contains whitespaces. Handles should use underscores." % self.handle)

        asset_dict = self.assets.get_asset(self.handle)
        self.initialize_asset(asset_dict)

        if self.name is None:
            raise AssetInitError("Asset handle '%s' could not be retrieved!" % self.handle)


    def initialize_from_name(self):
        """ If we've got a not-None name, we can initiailze the asset object
        by checking self.assets to see if we can find an asset whose "name"
        value matches our self.name. """

        # sanity warning
        if "_" in self.name:
            self.logger.warn("Asset name '%s' contains underscores. Names should use whitespaces." % self.name)

        lookup_dict = {}
        for asset_handle in self.assets.get_handles():
            asset_dict = self.assets.get_asset(asset_handle)
            lookup_dict[asset_dict["name"]] = asset_handle

        if self.name in lookup_dict.keys():
            self.handle = lookup_dict[self.name]
            self.initialize_from_handle()

        if self.handle is None:
            raise AssetInitError("Asset handle '%s' could not be retrieved!" % self.handle)


    #
    # look-up and manipulation methods below
    #

    def get(self, attrib):
        """ Wrapper method for trying to retrieve asset object attributes.
        Returns a None type value if the requested attrib doesn't exist. """

        try:
            return getattr(self, attrib)
        except:
            return None


class UserAsset():
    """ The base class for initializing individual user assets, such as
    survivors, sessions, settlements, etc. """


    def __repr__(self):
        exec 'repr_name = self.%s["name"]' % (self.collection[:-1])
        return "%s object '%s' [%s]" % (self.collection, repr_name, self._id)


    def __init__(self, collection=None, _id=None):

        # initialize basic vars
        self.logger = utils.get_logger(log_name="server")

        if collection is not None:
            self.collection = collection
        elif hasattr(self,"collection"):
            pass
        else:
            err_msg = "User assets may not be initialized without specifying a collection!"
            self.logger.error(err_msg)
            raise AssetInitError(err_msg)

        # use attribs to determine whether the object has been loaded
        self.loaded = False
        if _id is None:
            self.new()
        else:
            try:
                self._id = ObjectId(_id)
                self.load()
                self.loaded = True
            except Exception as e:
                self.logger.error("Could not load _id '%s' from %s!" % (_id, self.collection))
                self.logger.exception(e)


    def save(self):
        """ Saves the user asset back to either the 'survivors' or 'settlements'
        collection in mdb, depending on self.collection. """

        if self.collection == "settlements":
            utils.mdb.settlements.save(self.settlement)
        elif self.collection == "survivors":
            utils.mdb.survivors.save(self.survivor)
        else:
            raise AssetLoadError("Invalid MDB collection for this asset!")
        self.logger.info("Saved %s to mdb.%s successfully!" % (self, self.collection))


    def load(self):
        """ Retrieves an mdb doc using self.collection and makes the document an
        attribute of the object. """

        mdb_doc = utils.mdb[self.collection].find_one({"_id": self._id})
        if mdb_doc is None:
            raise AssetLoadError()

        if self.collection == "settlements":
            self.settlement = mdb_doc
        elif self.collection == "survivors":
            self.survivor = mdb_doc
        else:
            raise AssetLoadError("Invalid MDB collection for this asset!")


    def get_serialize_meta(self):
        """ Sets the 'meta' dictionary for the object when it is serialized. """

        output = copy(utils.api_meta)
        try:
            output["meta"]["object"]["version"] = self.object_version
        except Exception as e:
            self.logger.error("Could not create 'meta' dictionary when serializing object!")
            self.logger.exception(e)
            self.logger.warn(utils.api_meta)
            self.logger.warn(output["meta"])
        return output


    def http_response(self):
        """ Generates an HTTP request response: tries to serialize the object instance but,
        if it can't, returns a 500 or 404 as appropriate. """

        if self.loaded:
            return Response(response=self.serialize(), status=200, mimetype="application/json")
        else:
            return utils.http_404
