import requests
import time

class GNS3Project:
    """A simple class to manage a GNS3 project."""

    def __init__(self, project_name, server_url="http://localhost:3080"):
        """
        Set up the GNS3 project with a server URL and project name.
        """
        self.server_url = server_url
        self.project_name = project_name
        self.project_id = self._find_project_id()

    def _find_project_id(self):
        """Find the project ID based on the project name."""
        try:
            response = requests.get(f"{self.server_url}/v2/projects", timeout=5)
            response.raise_for_status()
            projects = response.json()
            for project in projects:
                if project['name'] == self.project_name:
                    return project['project_id']
            raise ValueError(f"Project '{self.project_name}' not found")
        except requests.RequestException as e:
            raise Exception(f"Failed to fetch projects: {e}")

    def start(self):
        """Start the project by opening it and starting all nodes."""
        try:
            open_response = requests.post(f"{self.server_url}/v2/projects/{self.project_id}/open")
            open_response.raise_for_status()
            start_response = requests.post(f"{self.server_url}/v2/projects/{self.project_id}/nodes/start")
            start_response.raise_for_status()
            print(f"Started project '{self.project_name}'")
            time.sleep(15)
        except requests.RequestException as e:
            raise Exception(f"Failed to start project: {e}")

    def stop(self, close=False):
        """Stop the project and optionally close it."""
        try:
            stop_response = requests.post(f"{self.server_url}/v2/projects/{self.project_id}/nodes/stop")
            stop_response.raise_for_status()
            if close:
                close_response = requests.post(f"{self.server_url}/v2/projects/{self.project_id}/close")
                close_response.raise_for_status()
            print(f"Stopped project '{self.project_name}'" + (" and closed" if close else ""))
        except requests.RequestException as e:
            raise Exception(f"Failed to stop project: {e}")


if __name__ == "__main__":
    project = GNS3Project("BGP_1")
    project.start()
    time.sleep(30)
    project.stop(close=True)
