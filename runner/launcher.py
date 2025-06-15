import uuid
from runner.factory import get_runner
from users.http_user import HTTPUser
from users.kafka_user import KafkaUser
from users.mq_user import MQUser
from shapes.custom_shape import CustomShape
from runner.openshift_runner import OpenshiftRunner
from utils.image_builder import build_and_push_image
from runner.base import BaseRunner
USER_CLASS_MAP = {
    "http": HTTPUser,
    "kafka": KafkaUser,
    "mq": MQUser,
}

def launch_test(test_type, config, runner_type="local", data=None, test_id=None, status_store=None):
    # Optionally receive a test_id and a dict to store status/progress
    if not test_id:
        test_id = str(uuid.uuid4())
    user_class = USER_CLASS_MAP[test_type]
    user_class.config = config
    shape = CustomShape(config.get("shape", {}))
    runner : BaseRunner = get_runner(runner_type, user_class, shape, config)
    runner.prepare()

    # Optional: store status if a store is provided
    if status_store is not None:
        status_store[test_id] = {"status": "running"}

    try:
        runner.run()
        if status_store is not None:
            status_store[test_id]["status"] = "finished"
    except Exception as e:
        if status_store is not None:
            status_store[test_id]["status"] = "error"
            status_store[test_id]["error"] = str(e)
        raise
    finally:
        if hasattr(runner, "cleanup"):
            runner.cleanup()
    return test_id