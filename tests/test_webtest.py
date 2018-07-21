import capybara
from capybara.tests.suite import DriverSuite


@capybara.register_driver("webtest")
def init_webtest_driver(app):
    from capybara_webtest.driver import Driver

    return Driver(app)


WebTestDriverSuite = DriverSuite(
    "webtest",
    skip=["css", "frames", "hover", "js", "modals", "screenshot", "send_keys", "server", "windows"])
