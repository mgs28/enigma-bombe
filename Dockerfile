# Dockerfile

FROM python:3.11.2-slim-bullseye

RUN apt-get update && \
    apt-get upgrade --yes

RUN useradd --create-home realpython
USER realpython
WORKDIR /home/realpython

ENV VIRTUALENV=/home/realpython/venv
RUN python3 -m venv $VIRTUALENV
ENV PATH="$VIRTUALENV/bin:$PATH"

COPY --chown=realpython pyproject.toml constraints.txt ./
RUN python -m pip install --upgrade pip setuptools && \
    python -m pip install --no-cache-dir -c constraints.txt ".[dev]"

COPY --chown=realpython src/ src/
COPY --chown=realpython test/ test/

# unblock port 80 for the Flask app to run on
EXPOSE 80

#RUN python -m pip install . -c constraints.txt && \
#    python -m pytest test/unit/ && \
#    python -m flake8 src/ && \
#    python -m pylint src/ --disable=C0114,C0116,R1705 && \
#    python -m bandit -r src/ --quiet

RUN python -m pip install . -c constraints.txt && \
    python -m pytest test/unit/ && \
    python -m pylint src/ --disable=C0114,C0116,R1705 

#CMD ["python", "src/enigma_bombe/app.py"]
CMD ["flask", "--app", "enigma_bombe.app", "run", \
     "--host", "0.0.0.0", "--port", "80"]