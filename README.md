# QA Engineer Assignment – API & UI Test Automation

Automated test suite covering REST API validation (`reqres.in`) and Web UI end-to-end testing (`www.iamdave.ai`) built with Python, `pytest`, `requests`, `Selenium`, and `Locust`.

---

## Project Structure

```text
├── tests/
│   ├── __init__.py
│   ├── test_api.py      # 5 API test cases for Reqres
│   └── test_ui.py       # 4 UI test cases for www.iamdave.ai
├── load_test.py         # Locust load test script (capped < 100 requests)
├── requirements.txt     # Python dependencies
└── README.md            # Setup, execution, and test design documentation