import os

BATCH_SIZE_FOR_TRANSFERRING = int(os.getenv("BATCH_SIZE_FOR_TRANSFERRING", "500"))
TRANSFER_DATA_TO_ELASTIC = True if os.getenv("TRANSFER_DATA_TO_ELASTIC", "false").lower() == "true" else False
CREATE_ELASTIC_INDEX = True if os.getenv("CREATE_ELASTIC_INDEX", "false").lower() == "true" else False
