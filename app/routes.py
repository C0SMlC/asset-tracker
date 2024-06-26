from flask import Blueprint, request, jsonify, current_app
from app.models import Asset
from app.utils import get_google_sheet

main = Blueprint('main', __name__)

@main.route('/scan', methods=['POST'])
def scan_barcode():
    data = request.json
    asset_number = data.get('asset_number')
    
    if not asset_number:
        return jsonify({'error': 'No asset number provided'}), 400
    
    assets_collection = current_app.db.assets
    asset_data = assets_collection.find_one({'asset_number': asset_number})
    
    if asset_data:
        asset = Asset.from_dict(asset_data)
        asset.mark_as_scanned()
        
        assets_collection.replace_one({'_id': asset._id}, asset.to_dict())
        
        sheet = get_google_sheet()
        sheet_data = [asset.asset_number, asset.description, asset.acquisition_date, 'Yes', asset.last_scanned_date]
        sheet.append_row(sheet_data)
        
        return jsonify({'message': f'Asset {asset_number} marked as scanned and updated in Google Sheets'}), 200
    else:
        return jsonify({'error': 'Asset not found'}), 404

@main.route('/asset/<asset_number>', methods=['GET'])
def get_asset(asset_number):
    assets_collection = current_app.db.assets
    asset_data = assets_collection.find_one({'asset_number': asset_number})
    
    if asset_data:
        asset = Asset.from_dict(asset_data)
        return jsonify(asset.to_dict()), 200
    else:
        return jsonify({'error': 'Asset not found'}), 404

@main.route('/asset', methods=['POST'])
def create_asset():
    data = request.json
    new_asset = Asset(
        asset_number=data['asset_number'],
        description=data['description'],
        acquisition_date=data['acquisition_date']
    )
    
    assets_collection = current_app.db.assets
    try:
        result = assets_collection.insert_one(new_asset.to_dict())
        return jsonify({'message': 'Asset created successfully', 'id': str(result.inserted_id)}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@main.before_app_request
def create_indexes():
  Asset.create_asset_index(current_app.db.assets)
