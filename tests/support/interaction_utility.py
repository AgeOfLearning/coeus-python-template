from coeus_unity import assertions, commands
from appium.webdriver.common.touch_action import TouchAction


class InteractionUtility:
    """
    Utilities for simplifying the interaction based on
    platform. Do not change this directly in your repository. Instead,
    change and submit a merge-request to the original coeus-test-template.
    Always consume downstream changes.
    """
    @staticmethod
    def tap_transform(test_case, transform_path):
        """
        Awaits for the transform to exist,
        then fetches the screen position. Finally,
        it invokes a tap event through appium.
        :param test_case:
        :param transform_path:
        :return:
        """
        assertions.assert_await_transform_exists(test_case.cli, transform_path)

        if test_case.is_android:
            result = commands.fetch_transform_screen_position(test_case.cli, transform_path)
            InteractionUtility.tap(test_case, result[0], result[1])

        if test_case.is_ios:
            result = commands.fetch_transform_normalized_screen_position(test_case.cli, transform_path)
            InteractionUtility.tap_normalized(test_case, result[0], result[1])

    @staticmethod
    def tap(test_case, x, y):
        actions = TouchAction(test_case.appium.driver)
        actions.tap(element=None, x=x, y=y)
        actions.release()
        actions.perform()

    @staticmethod
    def tap_normalized(test_case, nx, ny):
        # Find actual position from normalized...
        window_rect = test_case.appium.driver.get_window_size()
        x = window_rect["width"] * nx
        y = window_rect["height"] * ny

        InteractionUtility.tap(test_case, x, y)

    @staticmethod
    def close_keyboard(test_case):
        test_case.appium.driver.hide_keyboard(strategy="press", key_name="Go")

    @staticmethod
    def submit_keyboard(test_case):
        if test_case.is_android:
            test_case.appium.driver.keyevent(61)
            test_case.appium.driver.keyevent(66)
