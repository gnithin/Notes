# Celery

Understanding Celery.

## Introduction 
Notes from https://docs.celeryproject.org/en/stable/getting-started/introduction.html#introduction-to-celery

- [QUESTION] Why is Celery called a task queue? It's a worker. It uses redis or rabbitMQ as it's queue.

- A task is an object which specifies what to do. Think of it as a JSON message.
- To initiate a task the client adds a message to the queue, the broker then delivers that message to a worker.

- Celery requires a message transport to send and receive messages
	- Again I am confused


