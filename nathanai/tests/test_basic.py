from nathanai.agent import NathanAgent
from nathanai.providers import MockProvider


def test_mock_roundtrip():
    agent = NathanAgent(provider=MockProvider())
    reply = agent.chat("Hola")
    assert reply.startswith("[mock:")
    assert "Hola" in reply
