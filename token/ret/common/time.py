from boa.interop.Neo.Blockchain import GetHeight, GetHeader
from boa.interop.Neo.Header import GetTimestamp, GetHash, GetNextConsensus # All these references are needed


def get_now():
    height = GetHeight()
    current_block = GetHeader(height)
    timestamp = current_block.Timestamp
    return timestamp