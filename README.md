# Install Notes

First, we're going to use conda which is the same environment management tool pytorch uses. It's really for us a wrapper on a specific python version and allows us to use pip installs without affecting any other projects. 

$ conda activate enigma-bombe

Then make sure to install all the items listed in pyproject.toml. The ".[dev]" argument installs all options in the [project.optional-dependencies] section. 

$ pip install --editable ".[dev]" 

You can then run two options: run the command line versions or the dockerized API version

## Comannd Line Version

First, run the unit tests to make sure the system works

$ python -m pytest -v test/unit

Then you can run the code quality tools 

like linting

$ python -m pylint src/ --disable=C0114,C0116,R1705

like black to autofix some linting issues

$ python -m black src/ --check 

$ python -m black src/

## Install pytorch tasks

After spacy is installed, download the english model to tokenize 

python -m spacy download en_core_web_sm

## Dockerized API version
You can then dockerize the enigma-bombe webapp with 

docker build -t enigma-bombe . 

In docker desktop (MacOS), you'll need to start images with 'Optional Settings' and specify the port that you wish to access for the engima-bombe web app

$ flask --app src/enigma_bombe/app.py run


# Resources

Here's the [paper](https://web.archive.org/web/20060720040135/http://members.fortunecity.com/jpeschel/gillog1.htm) that we will base our attack of enigma cipher text on using the  [Index of Coincidence](https://en.wikipedia.org/wiki/Index_of_coincidence)


A [great RealPython resource](https://realpython.com/docker-continuous-integration/) to start using redis, python and docker together is on RealPython. I modified this a fair bit to get the behavior I wanted for a dockerized API. 


