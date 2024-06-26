from datetime import datetime
from bson import ObjectId

class Asset:
    def __init__(self, asset_number, description, acquisition_date, scanned=False, last_scanned_date=None, _id=None):
        self._id = ObjectId(_id) if _id else ObjectId()
        self.asset_number = asset_number
        self.description = description
        self.acquisition_date = acquisition_date
        self.scanned = scanned
        self.last_scanned_date = last_scanned_date

    @classmethod
    def from_dict(cls, data):
        return cls(
            asset_number=data['asset_number'],
            description=data['description'],
            acquisition_date=data['acquisition_date'],
            scanned=data.get('scanned', False),
            last_scanned_date=data.get('last_scanned_date'),
            _id=data.get('_id')
        )

    def to_dict(self):
        return {
            '_id': str(self._id),
            'asset_number': self.asset_number,
            'description': self.description,
            'acquisition_date': self.acquisition_date,
            'scanned': self.scanned,
            'last_scanned_date': self.last_scanned_date
        }

    def mark_as_scanned(self):
        self.scanned = True
        self.last_scanned_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    @staticmethod
    def create_asset_index(collection):
        collection.create_index("asset_number", unique=True)