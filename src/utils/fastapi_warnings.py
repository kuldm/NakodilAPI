import warnings
from fastapi.exceptions import FastAPIDeprecationWarning

warnings.filterwarnings(
    "ignore",
    message="`example` has been deprecated.*",
    category=FastAPIDeprecationWarning,
)