# tests/test_csv_reader.py
import pytest
from src.modules.data_processing.csv_reader import read_csv

def test_read_csv_success(tmp_path):
    test_file = tmp_path / "test.csv"
    test_file.write_text("a,b,c\n1,2,3")
    data = read_csv(str(test_file))
    assert len(data) == 2
    assert data[0].startswith("a")
