import requests


class WebServClient:
    def query_root(self, hostname: str) -> dict:
        url = f"http://{hostname}/"
        r = requests.get(url, timeout=5)

        if r.status_code != 200:
            raise RuntimeError(f"HTTP {r.status_code}: {r.text}")

        return r.json()


if __name__ == "__main__":
    client = WebServClient()
    data = client.query_root("127.0.0.1:8000")
    print(data)
