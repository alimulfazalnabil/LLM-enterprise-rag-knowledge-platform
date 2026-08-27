from enum import StrEnum

class IngestionState(StrEnum):
    PENDING = 'PENDING'
    PROCESSING = 'PROCESSING'
    COMPLETED = 'COMPLETED'
    FAILED = 'FAILED'

if __name__ == '__main__':
    print('Worker scaffold started')
