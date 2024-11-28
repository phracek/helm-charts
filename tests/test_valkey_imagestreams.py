import os

import pytest
from pathlib import Path

from container_ci_suite.helm import HelmChartsAPI

test_dir = Path(os.path.abspath(os.path.dirname(__file__)))

@pytest.fixture(scope="module")
def helm_api(request):
    helm_api = HelmChartsAPI(path=test_dir / "../charts/centos", package_name="valkey-imagestreams", tarball_dir=test_dir)
    print(request)
    # app_name = os.path.basename(request.param)
    yield helm_api
    pass
    helm_api.delete_project()


class TestHelmCentOSValkeyImageStreams:

    @pytest.mark.parametrize(
        "version,registry,expected",
        [
            ("7-el10", "quay.io/sclorg/valkey-7-c10s:latest", True),
        ],
    )
    def test_package_imagestream(self, helm_api, version, registry, expected):
        assert helm_api.helm_package()
        assert helm_api.helm_installation()
        assert helm_api.check_imagestreams(version=version, registry=registry) == expected
