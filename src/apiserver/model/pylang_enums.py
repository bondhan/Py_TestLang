import enum

class Status(enum.Enum):
    ACTIVE = 'ACTIVE'
    INACVITE = 'INACTIVE'

class SOF(enum.Enum):
    DEFAULT = 'DEFAULT'
    NOT_DEFAULT = 'NOT_DEFAULT'

class IdentityType(enum.Enum):
    KTP = 'KTP'
    SIM = 'SIM'
    PASPOR = 'PASPOR'

class OrganizationType(enum.Enum):
    BANK = 'BANK'
    OTHERS = 'OTHERS'

class DefaultFlag(enum.Enum):
    DEFAULT = 'DEFAULT'
    NOT_DEFAULT = 'NOT_DEFAULT'

class ReconFlag(enum.Enum):
    YES = 'YES'
    NO = 'NO'
