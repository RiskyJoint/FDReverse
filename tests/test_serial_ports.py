from communication.serial_handler import list_available_ports


def test_list_available_ports():
    ports = list_available_ports()
    assert isinstance(ports, list)
