# LoadTest Framework

A flexible, extensible Python-based framework for orchestrating multi-protocol load tests—locally, in containers, or on Kubernetes/OpenShift. Supports dynamic user-provided data, pluggable message producers (Kafka, RabbitMQ, etc.), and API-driven test scheduling.

---

## 🚀 Features

- **Run Anywhere:** Local, Docker, Kubernetes, or OpenShift Jobs.
- **Pluggable Runners:** Local, Docker, K8s, and more via simple registry.
- **Protocol Agnostic:** Supports HTTP, Kafka, RabbitMQ, MQ, gRPC, etc.
- **Dynamic Data:** Users supply data per test via API (single message, list, file, etc.).
- **Producer Abstraction:** Easily add new message brokers by subclassing.
- **API-Driven:** Schedule and monitor tests remotely with a FastAPI-powered service.
- **Autocleanup:** Automatic cleanup of test resources (K8s Jobs, Docker containers, etc.).
- **Extensible:** Add new runners, producers, or data handlers with minimal code.

---

## 🗂️ Project Structure

```
loadtest_framework/
├── api/                 # FastAPI app for remote test orchestration
├── config/              # Config loading utilities
├── connections/         # Pluggable message producers/connectors
├── data/                # Data handler abstractions (list, single, etc.)
├── runner/              # Pluggable runners (local, docker, k8s, etc.)
├── users/               # Locust User classes (per protocol or generic)
├── shapes/              # Locust custom shape classes
├── locustfile.py        # Entrypoint for Locust CLI
├── main.py              # CLI entrypoint for local runs
├── requirements.txt
├── Dockerfile
└── README.md
```

---

## 🏁 Quick Start

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. (Optional) Build Docker image

```bash
docker build -t my-loadtest .
```

### 3. Run a test locally

```bash
python main.py --config=config/example_kafka.yaml --runner=local
```

### 4. Launch API server

```bash
uvicorn api.main:app --reload
```

### 5. Start a test via API

```bash
curl -X POST http://localhost:8000/run \
     -H 'Content-Type: application/json' \
     -d @example_api_request.json
```

Check status:
```bash
curl http://localhost:8000/status/<test_id>
```

---

## 🧩 Extending the Framework

### Add a New Runner

1. Create `runner/my_runner.py`:
    - Subclass `BaseRunner`
    - Register with `@RunnerRegistry.register("mytype")`
2. Update documentation.

### Add a Message Producer

1. Create `connections/my_producer.py`:
    - Subclass `BaseProducer`
    - Register in `connections/factory.py`

### Add a Data Handler

1. Create `data/my_handler.py`:
    - Subclass `BaseDataHandler`
    - Register in `data/factory.py`

---

## ⚙️ Example API Request

```json
{
  "test_type": "kafka",
  "runner_type": "local",
  "config": {
    "msg_type": "kafka",
    "bootstrap_servers": "localhost:9092",
    "topic": "my-topic"
  },
  "data": [
    "message 1",
    "message 2",
    "message 3"
  ]
}
```

---

## 🧪 Testing Protocols

- **HTTP:** Use `users/http_user.py`
- **Kafka:** Use `users/kafka_user.py`
- **RabbitMQ:** Use `users/mq_user.py`
- **Generic Message:** Use `users/generic_msg_user.py` with any supported producer

---

## 📖 Advanced Usage

- **Custom Load Shapes:** Implement in `shapes/custom_shape.py`
- **Distributed Testing:** Use K8s runner for massive tests
- **Autocleanup:** Runners clean up jobs/containers after test completion
- **Custom Data Sources:** Extend `data/` for CSV, random, or API-driven data

---

## 🛠️ Contributing

- PRs welcome! Add new runners, producers, data handlers, or user classes.
- Please document new features and update this README.

---

## 📄 License

MIT License
