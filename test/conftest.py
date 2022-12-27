import pytest
import responses

from v2raycli.outbounds import NamedServer
from v2raycli.subscription import parse_subscription
from .testings import EXAMPLE_SUBSCRIPTION_LINES


@pytest.fixture(autouse=True)
def global_mocks():
    responses._add_from_file('responses.toml')
    yield
    responses.reset()


@pytest.fixture()
def subline_1() -> str:
    return EXAMPLE_SUBSCRIPTION_LINES[0]


@pytest.fixture()
def site_1(subline_1) -> NamedServer:
    return parse_subscription(subline_1)


@pytest.fixture()
def subline_2() -> str:
    return EXAMPLE_SUBSCRIPTION_LINES[1]


@pytest.fixture()
def site_2(subline_2) -> NamedServer:
    return parse_subscription(subline_2)


@pytest.fixture()
def subline_3() -> str:
    return EXAMPLE_SUBSCRIPTION_LINES[2]


@pytest.fixture()
def site_3(subline_3) -> NamedServer:
    return parse_subscription(subline_3)


@pytest.fixture()
def subline_4() -> str:
    return EXAMPLE_SUBSCRIPTION_LINES[3]


@pytest.fixture()
def site_4(subline_4) -> NamedServer:
    return parse_subscription(subline_4)


@pytest.fixture()
def subline_5() -> str:
    return EXAMPLE_SUBSCRIPTION_LINES[4]


@pytest.fixture()
def site_5(subline_5) -> NamedServer:
    return parse_subscription(subline_5)


@pytest.fixture()
def subline_6() -> str:
    return EXAMPLE_SUBSCRIPTION_LINES[5]


@pytest.fixture()
def site_6(subline_6) -> NamedServer:
    return parse_subscription(subline_6)
