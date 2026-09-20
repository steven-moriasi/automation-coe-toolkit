FROM python:3.14.7-slim-bookworm@sha256:9ab8d9c8514b44f90cf0029dd42fdd7e9e211e639c8b995304cc04568dee900f AS build

ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV PIP_NO_CACHE_DIR=1

WORKDIR /build

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:${PATH}"

COPY pyproject.toml README.md ./
COPY src ./src

RUN pip install --upgrade pip==26.2.1 \
    && pip install .

FROM python:3.14.7-slim-bookworm@sha256:9ab8d9c8514b44f90cf0029dd42fdd7e9e211e639c8b995304cc04568dee900f AS runtime

ENV PATH="/opt/venv/bin:${PATH}"
ENV PYTHONUNBUFFERED=1

RUN groupadd --system --gid 1001 coe \
    && useradd --system --uid 1001 --gid coe coe

WORKDIR /app

COPY --from=build /opt/venv /opt/venv
COPY examples ./examples

USER coe

ENTRYPOINT ["coe-toolkit"]
CMD ["evaluate", "examples/sample-intake.json"]
