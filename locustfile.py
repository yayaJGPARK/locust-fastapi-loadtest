from locust import HttpUser, task, between


class ApiUser(HttpUser):
    # 테스트 대상 서버 주소 (본인 서버에 맞게 수정)
    host = "http://localhost:8000"

    # 각 가상 유저가 요청 사이에 1~3초 대기
    wait_time = between(1, 3)

    def on_start(self):
        """가상 유저가 시작될 때 1번 실행 (로그인 등 사전 작업)"""
        # 로그인이 필요 없다면 이 메서드는 삭제해도 됩니다.
        # resp = self.client.post("/api/login", json={"username": "test", "password": "1234"})
        # token = resp.json().get("token")
        # self.client.headers.update({"Authorization": f"Bearer {token}"})
        pass

    # 숫자는 가중치: 조회가 생성보다 3배 더 자주 호출됨
    @task(3)
    def get_items(self):
        self.client.get("/api/items", name="GET /api/items")

    @task(2)
    def get_item_detail(self):
        # name을 지정하면 URL이 달라도 하나의 항목으로 집계됨
        self.client.get("/api/items/1", name="GET /api/items/{id}")

    @task(1)
    def create_item(self):
        payload = {"name": "test-item", "price": 1000}
        # catch_response=True: 성공/실패 기준을 직접 지정
        with self.client.post(
            "/api/items", json=payload, name="POST /api/items", catch_response=True
        ) as resp:
            if resp.status_code == 201:
                resp.success()
            else:
                resp.failure(f"예상치 못한 상태 코드: {resp.status_code}")