import docker
import shutil
import tempfile
import os
from pathlib import Path
import uuid

def build_and_push_image(
    base_image: str,
    locustfile_contents: str,
    requirements: list,
    registry_url: str,
    tag_prefix: str = "loadtest"
):
    # Create temp build context
    build_dir = Path(tempfile.mkdtemp())
    try:
        # Write Dockerfile
        (build_dir / "Dockerfile").write_text(f"""
FROM {base_image}
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY locustfile.py .
CMD ["locust", "-f", "locustfile.py", "--headless", "-u", "100", "-r", "10", "--run-time", "1m"]
""")
        # Write requirements.txt
        (build_dir / "requirements.txt").write_text("\n".join(requirements))
        # Write locustfile.py
        (build_dir / "locustfile.py").write_text(locustfile_contents)
        
        # Image name and tag
        test_id = str(uuid.uuid4())[:8]
        image_name = f"{registry_url}/{tag_prefix}:{test_id}"
        
        # Build image
        client = docker.from_env()
        image, logs = client.images.build(path=str(build_dir), tag=image_name)
        for chunk in logs:
            print(chunk.get('stream', ''), end='')
        
        # Push image
        for line in client.images.push(image_name, stream=True, decode=True):
            print(line)
        
        return image_name
    finally:
        shutil.rmtree(build_dir)