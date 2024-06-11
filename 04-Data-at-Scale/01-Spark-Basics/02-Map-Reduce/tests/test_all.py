import os
import pathlib

from lwmr import impl_python, impl_mapreduce

TXT = "I love apples, bananas and apples"


def test_txt_file_exists():
    parent_dir = pathlib.Path(os.path.realpath(__file__)).parent.parent
    txt_fp = os.path.join(parent_dir, "data", "The_Data_Engineering_Cookbook.txt")
    assert os.path.isfile(
        txt_fp
    ), "Please download the file https://wagon-public-datasets.s3.amazonaws.com/data-engineering/W3D3-processing/The_Data_Engineering_Cookbook.txt under ./data/"


def test_python_impl():
    cnt = impl_python.count_words(TXT)
    print(cnt)
    assert cnt.get("apples") == 2, "'apples' is expected to be found 2 times"
    assert cnt.get("i") == 1, "'i' is expected to be found 1 time"


def get_test_file_path():
    parent_dir = pathlib.Path(os.path.realpath(__file__)).parent
    path_test_file = os.path.join(parent_dir, "sample.txt")
    return path_test_file


def test_mapreduce_impl():
    cnt = impl_mapreduce.count_words_mapreduce([get_test_file_path()])
    assert cnt.get("apples") == 2, "'Apples' is expected to be found 2 times"
    assert cnt.get("i") == 1, "'I' is expected to be found 1 time"
