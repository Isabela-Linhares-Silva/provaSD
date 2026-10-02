FROM python:3.13-slim

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN pip install uv

RUN uv sync --frozen

COPY sistema-mensagens ./sistema-mensagens

CMD ["uv", "run", "python", "sistema-mensagens/server/server.py"]