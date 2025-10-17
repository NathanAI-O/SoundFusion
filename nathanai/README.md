# NathanAI

NathanAI es un agente de línea de comandos minimalista y extensible.

## Instalación (editable)

```bash
pip install -e ./nathanai
```

## Uso rápido

```bash
nathanai chat --model mock --system "Eres NathanAI, un asistente útil" --message "Hola"
```

## Configuración opcional

Crea un archivo `.env` con claves como `OPENAI_API_KEY` si vas a usar el proveedor OpenAI.

## Desarrollo

- Ejecuta pruebas: `pytest -q`
- Formato sugerido: `ruff`, `black` (no incluidos por defecto)
