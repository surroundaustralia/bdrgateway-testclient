from client.synthesizer import Synthesizer


def test_basic():
    synth = Synthesizer(1)
    g = synth.to_graph()
    print(g.serialize())
