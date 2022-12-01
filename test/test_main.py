"""
Test suite for the main module.
"""
import platform
from subprocess import call
from sys import executable

import pytest

from src.main import main  # test __all__


@pytest.fixture()
def data_for_ok_test():
    if platform.system().lower() == 'windows':
        return '-p C:\\ -i 187.188.112.16 -f test.bat'
    else:
        return '-p /home/flopezlira -i 187.188.112.16 -f test.sh'


@pytest.fixture()
def data_for_not_ok_test():
    if platform.system().lower() == 'windows':
        return '-p C:\\home2 -i 125.88.88.99 -f test2.bat'
    else:
        return '-p /home2/flopezlira -i 125.88.88.99 -f test2.bat'


def test_main_ok(data_for_ok_test):
    try:
        status = main(data_for_ok_test.split())
        assert status
    except SystemExit as ex:
        assert ex.code == 0


def test_main_not_ok(data_for_not_ok_test):
    try:
        status = main(data_for_not_ok_test.split())
        assert not status
    except SystemExit as ex:
        assert ex.code == 1


def test_main_none():
    """
        Test the main() function with no arguments.
    """
    with pytest.raises(SystemExit) as exinfo:
        main()  # displays a help message and exits gracefully
    assert exinfo.value.code == 2


def test_script():
    """
        Test command line execution.
    """
    # Call with the --help option as a basic sanity check.
    cmdl = f"{executable} -m main.py --help"
    assert 1 == call(cmdl.split())


# Make the script executable.
if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__]))
