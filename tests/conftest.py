import pytest
import responses

from tests.mock_api import MockCrewbook, load_fixtures


@pytest.fixture
def crewbook():
    """Start the fake API with a dataset: `api = crewbook(dataset)`; defaults to fixtures/*.json."""
    with responses.RequestsMock(assert_all_requests_are_fired=False) as rsps:
        def start(dataset=None):
            api = MockCrewbook(dataset if dataset is not None else load_fixtures())
            api.install(rsps)
            return api
        yield start
