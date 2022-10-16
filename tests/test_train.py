from src import train


def test_get_model():
    model_pipeline = train.get_model()

    assert model_pipeline is not None
