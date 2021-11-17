from ...db.db import db


class Share:
    required_fields = ['title', 'teaser', 'content', 'link']
    optional_fields = ['img_url']

    @staticmethod
    def get_all():
        """
        Get all shares from the database
        TODO: paginate
        """
        cursor = db['shares'].find({})
        shares = [document for document in cursor]
        return shares

    @staticmethod
    def insert(share_object: dict):
        """
        Add the given object
        """
        # blindly trusting that whoever called this function already validated the share object
        db['shares'].insert_one(share_object)
