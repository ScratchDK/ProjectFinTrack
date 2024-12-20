from unittest.mock import patch

from src.views import main


def test_main(returned_data: str) -> None:
    with patch("json.dumps") as mock_json_dumps:
        mock_json_dumps.return_value = returned_data
        assert main("28.12.2021 19:00:00") == returned_data
