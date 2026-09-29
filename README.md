# Locust + FastAPI Load Test

FastAPI 기반 테스트용 API 서버를 구축하고, Locust를 활용하여 API 부하 테스트를 수행하는 프로젝트입니다.

## 1. 프로젝트 목적

API 환경을 직접 구성하고 부하 테스트를 수행하여 다음 항목을 검증하는 것을 목적으로 합니다.

* API 응답 및 HTTP 상태 코드 검증
* API별 호출 비율을 고려한 부하 테스트
* GET / POST API 성능 테스트
* 부하 상황에서의 요청 성공 / 실패 확인
* Locust 기반 테스트 결과 확인

## 2. 테스트 환경

| 항목         | 환경              |
| ---------- | --------------- |
| Language   | Python 3.14     |
| API Server | FastAPI         |
| Load Test  | Locust          |
| Server     | Uvicorn         |
| OS         | Windows / Linux |
| CI         | GitHub Actions  |

## 3. 프로젝트 구조

```text
locust-fastapi-loadtest/
├─ .github/
│  └─ workflows/
│     └─ locust.yml
├─ api_server.py
├─ locustfile.py
├─ requirements.txt
└─ README.md
```

## 4. API 구성

테스트를 위해 FastAPI 기반의 간단한 상품 API를 구성했습니다.

### 상품 목록 조회

```http
GET /api/items
```

상품 목록을 조회합니다.

### 상품 상세 조회

```http
GET /api/items/{item_id}
```

상품 ID를 기준으로 특정 상품을 조회합니다.

### 상품 생성

```http
POST /api/items
```

상품 정보를 전달하여 새로운 상품을 생성합니다.

Request Example:

```json
{
  "name": "test-item",
  "price": 1000
}
```

정상적으로 생성된 경우 HTTP `201` 상태 코드를 반환하도록 구성했습니다.

## 5. Locust 테스트 구성

Locust에서 API별 호출 비율을 다르게 설정하여 실제 사용 패턴을 고려한 부하 테스트를 구성했습니다.

```python
@task(3)
def get_items():
    ...

@task(2)
def get_item_detail():
    ...

@task(1)
def create_item():
    ...
```

API 호출 비율:

```text
GET /api/items        3
GET /api/items/{id}   2
POST /api/items       1
```

즉, 전체 요청 중 목록 조회 API가 가장 많이 호출되도록 구성했습니다.

## 6. HTTP 상태 코드 검증

POST API의 경우 `catch_response=True`를 사용하여 HTTP 상태 코드에 따라 테스트 성공 / 실패를 판단하도록 구현했습니다.

```python
with self.client.post(
    "/api/items",
    json=payload,
    name="POST /api/items",
    catch_response=True
) as resp:

    if resp.status_code == 201:
        resp.success()
    else:
        resp.failure(
            f"예상치 못한 상태 코드: {resp.status_code}"
        )
```

이를 통해 단순히 요청을 전송하는 것이 아니라 예상 결과에 따라 성공 / 실패를 판단하도록 구성했습니다.

## 7. 실행 방법

### ① FastAPI 서버 실행

프로젝트 루트에서:

```bash
uvicorn api_server:app --reload
```

서버가 실행되면:

```text
http://127.0.0.1:8000
```

으로 접근할 수 있습니다.

FastAPI Swagger 문서:

```text
http://127.0.0.1:8000/docs
```

### ② Locust 실행

새로운 터미널에서:

```bash
locust
```

Locust Web UI:

```text
http://localhost:8089
```

Host:

```text
http://localhost:8000
```

설정 후 부하 테스트를 실행합니다.

## 8. Headless 부하 테스트

Web UI를 사용하지 않고 터미널에서 직접 테스트할 수도 있습니다.

```bash
locust \
  -f locustfile.py \
  --headless \
  -u 10 \
  -r 2 \
  -t 30s \
  --host
```
