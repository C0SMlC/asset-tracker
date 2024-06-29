from flask import Blueprint, request, jsonify, current_app
from app.models import Asset
from app.utils import get_google_sheet
from datetime import datetime, timezone
import pytz
import logging

main = Blueprint('main', __name__)

# Configure logging
logger = logging.getLogger(__name__)

@main.route('/scan', methods=['POST'])
def scan_barcode():
    logger.info("Received POST request to /scan")
    data = request.json
    asset_number = data.get('asset_number')
    if not asset_number:
        logger.warning("No asset number provided in request")
        return jsonify({'error': 'No asset number provided'}), 400
    
    assets_collection = current_app.db.assets
    asset_data = assets_collection.find_one({'asset_number': asset_number})
    if asset_data:
        logger.info(f"Asset found: {asset_number}")
        asset = Asset.from_dict(asset_data)
        utc_now = datetime.now(timezone.utc)
        ist_now = utc_now.astimezone(pytz.timezone('Asia/Kolkata'))
        asset.last_scanned_date = ist_now
        assets_collection.replace_one({'_id': asset._id}, asset.to_dict())
        logger.info(f"Updated last_scanned_date for asset: {asset_number}")
        
        sheet = get_google_sheet()
        cell = sheet.find(asset_number)
        if cell:
            row = cell.row
            sheet.update_cell(row, 5, ist_now.strftime('%Y-%m-%d %H:%M:%S'))
            message = f'Asset {asset_number} updated in Google Sheets'
            logger.info(message)
        else:
            sheet_data = [
                asset.asset_number, asset.description, asset.acquisition_date,
                'Yes', ist_now.strftime('%Y-%m-%d %H:%M:%S')
            ]
            sheet.append_row(sheet_data)
            message = f'Asset {asset_number} added to Google Sheets'
            logger.info(message)
        return jsonify({'message': message}), 200
    else:
        logger.warning(f"Asset not found: {asset_number}")
        return jsonify({'error': 'Asset not found'}), 404

@main.route('/asset/<asset_number>', methods=['GET'])
def get_asset(asset_number):
    logger.info(f"Received GET request for asset: {asset_number}")
    assets_collection = current_app.db.assets
    asset_data = assets_collection.find_one({'asset_number': asset_number})
    
    if asset_data:
        asset = Asset.from_dict(asset_data)
        logger.info(f"Asset found: {asset_number}")
        return jsonify(asset.to_dict()), 200
    else:
        logger.warning(f"Asset not found: {asset_number}")
        return jsonify({'error': 'Asset not found'}), 404

@main.route('/asset', methods=['POST'])
def create_asset():
    logger.info("Received POST request to create new asset")
    data = request.json
    new_asset = Asset(
        asset_number=data['asset_number'],
        description=data['description'],
        acquisition_date=data['acquisition_date']
    )
    
    assets_collection = current_app.db.assets
    try:
        result = assets_collection.insert_one(new_asset.to_dict())
        logger.info(f"Asset created successfully: {new_asset.asset_number}")
        return jsonify({'message': 'Asset created successfully', 'id': str(result.inserted_id)}), 201
    except Exception as e:
        logger.error(f"Error creating asset: {str(e)}")
        return jsonify({'error': str(e)}), 400

@main.before_app_request
def create_indexes():
    logger.info("Creating indexes for assets collection")
    Asset.create_asset_index(current_app.db.assets)