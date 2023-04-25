import os

import pytest
from pathlib import Path

from container_ci_suite.helm import HelmChartsAPI

test_dir = Path(os.path.abspath(os.path.dirname(__file__)))


class TestHelmRedisDBPersistent:

    def setup_method(self):
        package_name = "redis-persistent"
        path = test_dir / "../charts/redhat"
        self.hc_api = HelmChartsAPI(path=path, package_name=package_name, namespace="redis-helm", tarball_dir=test_dir, delete_prj=False)

    def teardown_method(self):
        self.hc_api.delete_project()

    def test_package_persistent(self):
        self.hc_api.set_version("0.0.1")
        self.hc_api.package_name = "redis-imagestreams"
        self.hc_api.helm_package()
        assert self.hc_api.helm_installation()
        self.hc_api.set_version("0.0.1")
        self.hc_api.package_name = "redis-persistent"
        self.hc_api.helm_package()
        assert self.hc_api.helm_installation(values={".redis_version": "8-el8", ".namespace": self.hc_api.namespace})
        assert self.hc_api.is_pod_running()
        assert self.hc_api.test_helm_chart(expected_str=["PONG"])
