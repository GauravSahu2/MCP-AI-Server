import pytest
from fastapi.testclient import TestClient
import sys
import os
import importlib.util

def load_app_from_path(module_name, path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module.app

# Paths to the FastAPI apps
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
mcp_path = os.path.join(base_dir, "apps", "model-control-plane", "main.py")
serving_path = os.path.join(base_dir, "apps", "model-serving-api", "main.py")

mcp_app = load_app_from_path("mcp_main", mcp_path)
serving_app = load_app_from_path("serving_main", serving_path)

@pytest.fixture
def mcp_client():
    return TestClient(mcp_app)

@pytest.fixture
def serving_client():
    return TestClient(serving_app)
