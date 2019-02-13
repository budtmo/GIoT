"""
Database model device.
"""

from src.models import db


class Device(db.Model):
    """
    Device class
    """

    class Category(object):
        SIMULATOR = 'simulator'
        HARDWARE = 'hardware'

    class Status(object):
        INACTIVE = 'inactive'
        AVAILABLE = 'available'
        USED = 'used'

    __tablename__ = 'device'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    category = db.Column(db.Enum(Category.SIMULATOR, Category.HARDWARE, name='category'), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    ip = db.Column(db.String(25), nullable=False)
    port = db.Column(db.String(10), nullable=False)
    status = db.Column(db.Enum(Status.INACTIVE, Status.AVAILABLE, Status.USED, name='status'), nullable=False)

    def __init__(self, name: str, category: str, type: str, ip: str, port: str, status: str):
        """
        Constructor
        :param name: Device name
        :param category: Device category
        :param type: Device Type
        :param ip: Ip address of the device
        :param port: Port number of the device
        :param status: Device status
        """
        self.name = name
        self.category = category
        self.type = type
        self.ip = ip
        self.port = port
        self.status = status

    def update(self, id: int = None, name: str = None, category: str = None, type: str = None, ip: str = None,
               port: str = None,
               status: str = None):
        if name:
            self.name = name
        if category:
            self.category = category
        if type:
            self.type = type
        if ip:
            self.ip = ip
        if port:
            self.port = port
        if status:
            self.status = status

    def to_dict(self) -> dict:
        """
        Convert device object to dict
        :return: device
        """
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'type': self.type,
            'ip': self.ip,
            'port': self.port,
            'status': self.status
        }

    def __repr__(self):
        """
        Convert device object to string
        :return: device
        """
        return '<Device(id={id}, name={name}, category={category}, type={type}, ip={ip}, port={port}, status={status})'. \
            format(id=self.id, name=self.name, category=self.category, type=self.type, ip=self.ip, port=self.port,
                   status=self.status)
