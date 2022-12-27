import os
from unittest import mock

import pytest

from ..testings import EXAMPLE_SUBSCRIPTION_URL


@pytest.fixture()
def env_v2ray_subscription():
    with mock.patch.dict(os.environ, {'V2RAY_SUBSCRIPTION': EXAMPLE_SUBSCRIPTION_URL}):
        yield
