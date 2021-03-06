# import
from mongo import get_db, post_db, update_db
from flask import request
import json
from config import USER_COLLECTION_NAME, SSS_COLLECTION_NAME

class SSS():
    """
    Provides functions to store data generated by SSS-maker.

    Parameters: Provide seg1, seg2 and seg3 in dictionary form.
    """

    def __init__(self,
                 seg1=None,
                 seg2=None,
                 seg3=None):
        if seg1:
            self.seg1 = seg1
        else:
            raise("seg1 not found")
        
        if seg2:
            self.seg2 = seg2
        else:
            raise("seg2 not found")
        
        if seg3:
            self.seg3 = seg3
        else:
            raise("seg3 not found")
        
        self.json_obj = {
            "metadata": self.seg1,
            "pgxform": self.seg2,
            "ssscrite": self.seg3
        }
        # `filter_obj` is used for querying the database on bases of `username`, `sssname`, `renurl`
        self.filter_obj = {"metadata.renarratorid": self.seg1['renarratorid'],
            "metadata.sssname": self.seg1['sssname'],
            "metadata.renurl": self.seg1['renurl']
        }

    @classmethod
    def fromJSON(cls, json_obj):
        """
        intialize class with JSON Object

        json_obj: JSON object containing 3 segments to given by user
        output: intialize class with JSON object values.
        """
        return cls(seg1=json_obj['metadata'],
                   seg2=json_obj['pgxform'],
                   seg3=json_obj['ssscrite'])

    # Wrapper for post_db function.
    def post(self):
        """
        post class.json_obj to sss_info database
        """
        return post_db(self.json_obj, SSS_COLLECTION_NAME)

    def ifExists(self):
        """
        Check if given SSS-name, author username and ren-url pair exist in collection or not.
        If yes, then return True, else return False
        """
        if(get_db(SSS_COLLECTION_NAME, self.filter_obj).count() > 0):
            return True
        else:
            return False

    @staticmethod
    def get(json_obj):
        """
        wrapper for get_db function to retreive resuts from sss_info collection.
        input: json object containing list of conditions to specify projection.
        output: return list of matching documents else False if no documents found.
        """
        print(json_obj)
        print(SSS_COLLECTION_NAME)
        results = get_db(SSS_COLLECTION_NAME, json_obj)
        print(results.count())
        if(results.count() > 0):
            return results
        return False

    def update(self, upsert=False, multi=False):
        """
        Check if SSS with same username, sss-name and ren-url already exist. If yes then
        that document is replaced with new values.

        upsert: if True, a new document will be created if not found in collection and return Id.
                if False, will return 'updated'.

        multi: if True, will update multiple documents matching to the query.
        """
        return update_db(collection_name=SSS_COLLECTION_NAME,
                            queryFilter=self.filter_obj, update=self.json_obj) 
