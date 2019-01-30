from coeus_unity import assertions as ua
from coeus_unity import commands as uc

from tests.support.interaction_utility import InteractionUtility
from tests.support.base_test_case import BaseTestCase

import os
import pytest


@pytest.mark.skip(reason="Example Test Case to show off features...")
class ExampleTestCase(BaseTestCase):
    """
    This example showcases the minimum setup for your
    product test case, and simple usage of unity commands/assertions
    from coeus-test-unity.
    """

    @staticmethod
    def setup_appium(cls):
        if not cls.is_device_farm:
            if cls.is_android:
                # Use provided quick-start setup or fill out capabilities yourself...
                cls.appium.setup_android_simulator()
                cls.appium.capabilities["app"] = os.path.abspath("builds/example/android/myproduct.apk")

            if cls.is_ios and cls.is_iphone_simulator:
                cls.appium.setup_iphone_simulator()
                cls.appium.capabilities["app"] = os.path.abspath("builds/example/ios/myproduct.app")

            if cls.is_ios and cls.is_ipad_simulator:
                cls.appium.setup_ipad_simulator()
                cls.appium.capabilities["orientation"] = "LANDSCAPE"
                cls.appium.capabilities["app"] = os.path.abspath("builds/example/ios/myproduct.app")

            if cls.is_ios and not cls.is_simulator:
                cls.appium.setup_ios_device("device-id-12345")
                cls.appium.capabilities["app"] = os.path.abspath("builds/example/ios/myproduct.ipa")
                cls.appium.capabilities["udid"] = "my-device-UUID"
                cls.appium.capabilities['xcodeOrgId'] = 'team-org'
                cls.appium.capabilities['xcodeSigningId'] = 'iPhone Developer'

    def test_00_setup(self):
        # Set host to production...
        ua.assert_scene_loaded(self.cli, "StartupUnityScene")
        InteractionUtility.tap_transform(self, "HostViewPrefab(Clone)/Panel/ProductionToggle")
        InteractionUtility.tap_transform(self, "HostViewPrefab(Clone)/Panel/SetHost")

    def test_01_login(self):
        self.unity_login()

    def unity_login(self):
        """
        Example of assigning the input fields directly via
        assign_component_value.
        :return:
        """
        ua.assert_await_scene_loaded(self.cli, "LoginPage")
        uc.assign_component_value(self.cli, "Canvas/LoginViewPrefab(Clone)/Panel/UsernameField", "InputField", "text", "test@test.com")
        uc.assign_component_value(self.cli, "Canvas/LoginViewPrefab(Clone)/Panel/PasswordField", "InputField", "text", "password")
        InteractionUtility.tap_transform(self, "Canvas/LoginViewPrefab(Clone)/Panel/Login Button")
