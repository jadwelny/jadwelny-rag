# mini-rag

This is a minimal implementation of the RAG model for question answering.

## Requirements

- Python 3.8 or later

#### Install Python using MiniConda

1) Download and install MiniConda from [here](https://docs.anaconda.com/free/miniconda/#quick-command-line-install)
2) Create a new environment using the following command:

```bash
conda create -n mini-rag python=3.8
```

3) Activate the environment:

```bash
conda activate mini-rag
```

### (Optional) Setup you command line interface for better readability

```bash
export PS1="\[\033[01;32m\]\u@\h:\w\n\[\033[00m\]\$ "
```

## Installation

### Install the required packages

```bash
pip install -r requirements.txt
```

### Setup the environment variables

```bash
cp .env.example .env
```

Set your environment variables in the `.env` file. Like `OPENAI_API_KEY` value.

## Run the FastAPI server

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 5000
```

## Reset docker on devs

### stop all the running containers

```bash
sudo docker stop $(sudo docker ps -aq)
```

### remove all the running containers

```bash
sudo docker rm $(sudo docker ps -aq)
```

### remove all the images I downloaded from dockerhub

```bash
sudo docker rmi $(sudo docker images -q)
```

### remove all the volumes

```bash
sudo docker volume rm $(sudo docker volume ls -q)
```

### remove what left

```bash
sudo docker system prune --all
```

### reset all

```bash
sudo docker stop $(sudo docker ps -aq); sudo docker rm $(sudo docker ps -aq); sudo docker rmi $(sudo docker images -q); sudo docker volume rm $(sudo docker volume ls -q); sudo docker system prune --all
```