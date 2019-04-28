import allure
import pytest


def pytest_addoption(parser):
   parser.addoption("--driver", action="store", default="chrome", help="Type in browser type")
   parser.addoption("--url", action="store", default="https://qa.moodle.net/", help="url")
   parser.addoption("--username", action="store", default="manager", help="username")
   parser.addoption("--password", action="store", default="test", help="password")


@pytest.fixture(scope="module")
def username(request):
   return request.config.getoption("--username")


@pytest.fixture(scope="module")
def password(request):
   return request.config.getoption("--password")


@pytest.fixture(scope="module")
def url(request):
   return request.config.getoption("--url")


@pytest.fixture(autouse=True, scope='session')
def driver(request):
    from selenium import webdriver
    driver = webdriver.Chrome()
    driver.set_page_load_timeout(5)
    driver.get("about:blank")
    driver.implicitly_wait(10)
    driver.maximize_window()
    for item in request.node.items:
        cls = item.getparent(pytest.Class)
        setattr(cls.obj, "driver", driver)
    yield driver
    driver.close()


@pytest.fixture(autouse=True, scope='session')
def errors():
    errors = []
    return errors


# def pytest_exception_interact(node, call, report):
#     allure.attach(
#         name='Screenshot',
#         body=node.parent._obj.driver.get_screenshot_as_png(),
#         attachment_type=allure.attachment_type.PNG
#     )
#
#     webdriver_log = node.parent._obj.driver.get_log('driver')
#     errors = []
#     for log in webdriver_log:
#         if log['level'] == "SEVERE":
#             errors.append(log['message'])
#
#     if len(errors) > 0:
#         allure.attach(
#             name="WebDriver-ERRORS!",
#             body=str(errors).encode(),
#             attachment_type=allure.attachment_type.TEXT
#         )
#
#     browser_console__log = node.parent._obj.driver.get_log('browser')
#     errors = []
#     for log in browser_console__log:
#         if log['level'] == "SEVERE":
#             errors.append(log['message'])
#             errors.append("<br>")
#
#     if len(errors) > 0:
#         allure.attach(
#             name="Console-ERRORS!",
#             body=str(errors).encode(),
#             attachment_type=allure.attachment_type.TEXT
#         )
#
#
