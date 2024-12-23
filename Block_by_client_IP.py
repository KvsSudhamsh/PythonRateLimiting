from iblockId import IBlockId
from flask import request

class BlockByIP(IBlockId):
    def blockId(self):
        if request.headers.get('X-Forwarded-For'):
            return request.headers.get('X-Forwarded-For').split(',')[0]
        return request.remote_addr