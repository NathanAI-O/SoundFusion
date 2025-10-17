from __future__ import annotations

import json
from typing import Optional

import click
from dotenv import load_dotenv

from .agent import NathanAgent
from .tools import echo_tool_factory
from .providers import MockProvider, OpenAIProvider


@click.group()
def main() -> None:
    """NathanAI - agente de línea de comandos"""


@main.command()
@click.option("--model", required=False, default="mock", help="Nombre del modelo (mock u openai)")
@click.option("--system", required=False, default=None, help="Prompt del sistema")
@click.option("--message", required=True, help="Mensaje del usuario")
@click.option("--provider", required=False, default=None, help="Forzar proveedor: mock|openai")
@click.option("--kwargs", required=False, default=None, help="JSON con kwargs del proveedor")
def chat(model: str, system: Optional[str], message: str, provider: Optional[str], kwargs: Optional[str]) -> None:
    """Envía un mensaje y recibe respuesta."""
    load_dotenv()

    provider_name = (provider or ("openai" if model != "mock" else "mock")).lower()
    if provider_name == "openai":
        backend = OpenAIProvider()
    else:
        backend = MockProvider()

    agent = NathanAgent(provider=backend, model=model, system_prompt=system)
    # Add a simple echo tool as example
    agent.tools.append(echo_tool_factory(prefix="echo:"))

    extra_kwargs = json.loads(kwargs) if kwargs else {}
    response = agent.chat(message, **extra_kwargs)
    click.echo(response)
