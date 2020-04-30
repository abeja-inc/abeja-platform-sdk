from abeja.training import Client


def test_init(organization_id):
    client = Client(organization_id=organization_id)
    assert client.organization_id == organization_id
