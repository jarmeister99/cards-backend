import pymongo

from ...db.db import db


class Share:
    required_fields = ['title', 'teaser', 'content', 'link']
    optional_fields = ['img_url', 'tags']

    @staticmethod
    def get_all():
        """
        Get all shares from the database
        TODO: paginate
        """
        cursor = db['shares'].find({}).sort("_id", pymongo.DESCENDING)
        shares = [document for document in cursor]
        for share in shares:
            if not share.get('img_url'):
                # hardcoded img_urls
                # TODO: replace with regex
                if 'youtube' in share.get('link'):
                    share['img_url'] = 'https://share.jaredfoster.dev/images/youtube.png'
        return shares

    @staticmethod
    def insert(share_object: dict):
        """
        Add the given object
        """
        # blindly trusting that whoever called this function already validated the share object
        db['shares'].insert_one(share_object)

    @staticmethod
    def delete(share_id: str):
        print(share_id)
