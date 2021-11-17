from ...db.db import db


class Share:
    @staticmethod
    def get_all():
        """
        Get all shares from the database
        TODO: paginate
        """
        cursor = db['shares'].find({})
        shares = [document for document in cursor]
        return shares
