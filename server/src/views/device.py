"""
Device endpoints.
"""

import logging

from connexion import NoContent

from flask import abort

from sqlalchemy.exc import DataError

from src import get_number_of_pages
from src.models import db
from src.models.device import Device
from src.msg import warning

logger = logging.getLogger('views.device')


def get_all(page_number: int, page_size: int, category: str=None, type: str=None, version: str=None,
            status: str=None) -> dict:
    """
    Get all devices based on given parameters
    :param page_number: selected page number
    :param page_size: size of page
    :param category: Category of device
    :param type: Type of device
    :param version: Version of device
    :param status: status of device
    :return: devices
    """
    logger.info('Page number: {num}, page size: {size}'.format(num=page_number, size=page_size))
    if not page_number or not page_size:
        logger.warning(warning.NO_PAGE_INFO)
        abort(404, {'message': warning.NO_PAGE_INFO})

    device_query = Device.query

    if category:
        device_query = device_query.filter(Device.category == category)

    if type:
        device_query = device_query.filter(Device.type == type)

    if version:
        device_query = device_query.filter(Device.version == version)

    if status:
        device_query = device_query.filter(Device.status == status)

    num_items = device_query.count()
    logger.info('Number of items: {item}'.format(item=num_items))
    total_pages = 0
    if num_items > 0:
        total_pages = get_number_of_pages(num_items, page_size)
        logger.info('Total pages: {total}'.format(total=total_pages))
    else:
        logger.warning(warning.NO_DATA)
        abort(404, {'message': warning.NO_DATA})

    if page_number > total_pages:
        logger.warning(warning.INVALID_PAGE)
        abort(404, {'message': warning.INVALID_PAGE})

    devices = device_query.order_by(Device.id.asc()).paginate(page=page_number, per_page=page_size,
                                                              error_out=True)
    logger.info('Devices: {devices}'.format(devices=devices.items))
    return {
        'page': page_number,
        'total_pages': total_pages,
        'devices': [d.to_dict() for d in devices.items]
    }


def register(device: dict) -> dict:
    """
    Register a new device
    """
    logger.info('New registered device: {d}'.format(d=device))
    # Check if the name already exists
    if Device.query.filter(Device.name == device.get('name')).first():
        logger.warning(warning.ALREADY_EXISTS)
        abort(400, {'message': warning.ALREADY_EXISTS})
    else:
        try:
            # ID will be automatically generated
            device.pop('id', None)
            db.session.add(Device(**device))
            db.session.commit()
            logger.info('Device is successfully registered!')
        except DataError:
            abort(400, {'message': warning.INVALID_DATA_TYPE})
    return NoContent, 200


def get_available_device(category: str=None, type: str=None, version: str=None) -> dict:
    device_query = Device.query

    if category:
        device_query = device_query.filter(Device.category == category)

    if type:
        device_query = device_query.filter(Device.type == type)

    if version:
        device_query = device_query.filter(Device.version == version)

    return device_query.filter(Device.status == "available").first_or_404().to_dict()


def get(device_id: int):
    """
    Get detail information of selected device
    :param device_id: device-ID
    :return: device
    """
    return Device.query.filter(Device.id == device_id).first_or_404().to_dict()


def update(device_id: int, device: dict) -> dict:
    """
    Update information of selected device
    :param device_id: device-ID
    :param device: new information
    """
    try:
        logger.info('Device with id \"{id}\" want to be updated'.format(id=device_id))
        selected_device = Device.query.filter(Device.id == device_id).first_or_404()
        selected_device.update(**device)
        db.session.commit()
        logger.info('Updated!')
        return NoContent, 201
    except DataError:
        abort(400, {'message': warning.INVALID_DATA_TYPE})


def delete(device_id: int):
    """
    Delete device from the list
    :param device_id: device-ID
    """
    d = Device.query.filter(Device.id == device_id).first_or_404()
    db.session.delete(d)
    db.session.commit()
    logger.info('Device with id \"{id}\" is successfully deleted!'.format(id=device_id))
    return NoContent, 204
