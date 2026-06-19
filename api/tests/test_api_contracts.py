import subprocess
import sys
import unittest

from pydantic import ValidationError

from api.main import app, home
from api.response_utils import list_response, success_response
from api.schemas import AssetCreate, AssetRelationshipCreate, ProjectCreate


class ApiContractTests(unittest.TestCase):
    def test_package_import_registers_expected_routes(self):
        route_paths = {route.path for route in app.routes}

        self.assertIn("/", route_paths)
        self.assertIn("/health", route_paths)
        self.assertIn("/projects", route_paths)
        self.assertIn("/assets", route_paths)
        self.assertIn("/relationships", route_paths)
        self.assertIn("/assets/{asset_id}/relationships", route_paths)
        self.assertIn("/assets/{asset_id}/impact", route_paths)
        self.assertIn("/search", route_paths)

    def test_openapi_schema_is_generated(self):
        schema = app.openapi()

        self.assertEqual(schema["info"]["title"], "Engineering OS API")
        self.assertIn("/search", schema["paths"])

    def test_legacy_main_import_still_works(self):
        result = subprocess.run(
            [
                sys.executable,
                "-c",
                (
                    "import sys; "
                    "sys.path.insert(0, 'api'); "
                    "import main; "
                    "print(main.app.title)"
                ),
            ],
            capture_output=True,
            check=True,
            text=True,
        )

        self.assertIn("Engineering OS API", result.stdout)

    def test_home_response_contract(self):
        self.assertEqual(
            home(),
            success_response(
                message="Engineering OS API is running",
                data={
                    "platform": "Engineering OS",
                    "status": "running",
                    "version": "1.0.0",
                },
            ),
        )

    def test_list_response_contract(self):
        self.assertEqual(
            list_response("Items retrieved", ["a", "b"]),
            {
                "success": True,
                "message": "Items retrieved",
                "count": 2,
                "data": ["a", "b"],
            },
        )

    def test_schema_status_values_are_normalized(self):
        project = ProjectCreate(
            project_id="PRJ-0002",
            project_name="New Project",
            status="active",
            priority="high",
        )

        self.assertEqual(project.status, "ACTIVE")
        self.assertEqual(project.priority, "HIGH")

        relationship = AssetRelationshipCreate(
            source_asset_id="ASSET-0001",
            source_asset_type="asset",
            target_asset_id="WF-0001",
            target_asset_type="workflow",
            relationship_type="depends_on",
        )

        self.assertEqual(relationship.source_asset_type, "ASSET")
        self.assertEqual(relationship.target_asset_type, "WORKFLOW")
        self.assertEqual(relationship.relationship_type, "DEPENDS_ON")

    def test_invalid_schema_status_is_rejected(self):
        with self.assertRaises(ValidationError):
            AssetCreate(
                asset_id="ASSET-0001",
                asset_name="Bad Asset",
                asset_type="Service",
                status="unknown",
            )


if __name__ == "__main__":
    unittest.main()
