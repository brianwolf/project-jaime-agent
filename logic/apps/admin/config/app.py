from uuid import UUID, uuid4

_ID_AGENT: UUID = None


def setup_id_agent() -> UUID:

    global _ID_AGENT
    _ID_AGENT = str(uuid4()).split('-')[4]

    return _ID_AGENT


def get_id_agent() -> UUID:
    return _ID_AGENT
