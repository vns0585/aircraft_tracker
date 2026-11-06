from src.api_client import ApiClient
from unittest.mock import patch, Mock


def test_api_client_init() -> None:
    api_client = ApiClient()
    assert api_client.aeroplanes == []
    assert api_client._ApiClient__api_url_coordinates == 'https://nominatim.openstreetmap.org/search'
    assert api_client._ApiClient__api_url_aeroplanes == 'https://opensky-network.org/api/states/all?'


@patch("src.api_client.get")
def test_get_geo_coordinates_success(mock_get: Mock) -> None:
    api_client = ApiClient()
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = [{'boundingbox': ['1.0', '2.0', '3.0', '4.0']}]
    mock_get.return_value = mock_response
    result = api_client.get_geo_coordinates('Spain')
    assert result == ['1.0', '2.0', '3.0', '4.0']


@patch("src.api_client.get")
def test_get_geo_coordinates_wrong_response(mock_get: Mock) -> None:
    api_client = ApiClient()
    mock_response = Mock()
    mock_response.status_code = 502
    mock_response.json.return_value = [{}]
    mock_get.return_value = mock_response
    result = api_client.get_geo_coordinates('Spain')
    assert result == []
    mock_response.status_code = 200
    result = api_client.get_geo_coordinates('Spain')
    assert result == []
    mock_response.json.return_value = {}
    result = api_client.get_geo_coordinates('Spain')
    assert result == []


@patch("src.api_client.get")
def test_get_aeroplanes_success(mock_get: Mock) -> None:
    api_client = ApiClient()
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {'states': ['1', '2', '3', '4']}
    mock_get.return_value = mock_response
    result = api_client.get_aeroplanes([1, 2, 3, 4])
    assert result == ['1', '2', '3', '4']


@patch("src.api_client.get")
def test_get_aeroplanes_wrong_response(mock_get: Mock) -> None:
    api_client = ApiClient()
    mock_response = Mock()
    mock_response.status_code = 502
    mock_response.json.return_value = {'states': ['1', '2', '3', '4']}
    mock_get.return_value = mock_response
    result = api_client.get_aeroplanes([1, 2, 3, 4])
    assert result == []
    mock_response.status_code = 200
    mock_response.json.return_value = ['1', '2', '3', '4']
    result = api_client.get_aeroplanes([1, 2, 3, 4])
    assert result == []
    result = api_client.get_aeroplanes([1, 2, 3])
    assert result == []
