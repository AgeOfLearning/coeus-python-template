import time
import unittest
import logging
import os

from coeus_test import client
from coeus_appium import appium_driver
from coeus_test.port_forwarding import PortForwarding

# Constants...
DEFAULT_APP_START_DELAY = 10
ANDROID_PLATFORM = "android"
ANDROID_PLATFORM_SIMULATOR = "android-simulator"
IOS_PLATFORM = "ios"
IPHONE_PLATFORM_SIMULATOR = "iphone-simulator"
IPAD_PLATFORM_SIMULATOR = "ipad-simulator"

# AWS Device Farm Constants...
DEVICE_FARM_APP_PATH_KEY = "DEVICEFARM_APP_PATH"
DEVICE_FARM_DEVICE_PLATFORM_NAME_KEY = "DEVICEFARM_DEVICE_PLATFORM_NAME"


class BaseTestCase(unittest.TestCase):
    """
    Inherit this class in your TestCase. Do not
    make changes locally to this class. Always pull downstream changes
    from original coeus-test-template repository. Submit changes
    as merge request to original coeus-template-template repository.
    """
    cli = None
    appium = None
    platform = None
    simulator = None
    root_path = None

    is_android = False
    is_ios = False
    is_simulator = False
    is_ipad_simulator = False
    is_iphone_simulator = False
    is_android_simulator = False
    is_device_farm = False

    @classmethod
    def setUpClass(cls):
        cls.platform = cls.get_platform()
        cls.simulator = cls.get_simulator()

        # Set Platform states...
        cls.is_android = ANDROID_PLATFORM == cls.platform
        cls.is_ios = IOS_PLATFORM == cls.platform
        cls.is_iphone_simulator = IPHONE_PLATFORM_SIMULATOR == cls.simulator
        cls.is_ipad_simulator = IPAD_PLATFORM_SIMULATOR == cls.simulator
        cls.is_android_simulator = ANDROID_PLATFORM_SIMULATOR == cls.simulator
        cls.is_simulator = cls.simulator in [ANDROID_PLATFORM_SIMULATOR, IPHONE_PLATFORM_SIMULATOR, IPAD_PLATFORM_SIMULATOR]
        cls.is_device_farm = DEVICE_FARM_APP_PATH_KEY in os.environ

        logging.info("Initializing for platform '{0}' and simulator '{1}'".format(cls.platform, cls.simulator))

        logging.info("Setup appium...")
        # Setup appium...
        cls.appium = appium_driver.AppiumDriver()
        cls.setup_appium(cls)
        cls.appium.connect()

        logging.info("Sleeping for app start delay...")
        # Wait for app start...
        time.sleep(cls.get_app_start_delay())

        logging.info("Connecting to coeus...")
        # Connect to coeus...
        cls.setup_port_forwarding(cls)
        cls.cli = client.Client(tcp_port=cls.get_coeus_port(cls), tcp_ip="0.0.0.0")
        cls.cli.connect()

        logging.info("Ready for tests...")

    @classmethod
    def tearDownClass(cls):
        logging.info("Tearing down...")

        cls.teardown(cls)
        cls.cli.stop()
        cls.cli = None
        cls.appium = None
        cls.appium.stop()

    @staticmethod
    def get_simulator():
        if 'SIMULATOR' in os.environ:
            return os.environ['SIMULATOR']

    @staticmethod
    def get_platform():
        if 'PLATFORM' in os.environ:
            return os.environ['PLATFORM']

        if DEVICE_FARM_DEVICE_PLATFORM_NAME_KEY in os.environ:
            return os.environ[DEVICE_FARM_DEVICE_PLATFORM_NAME_KEY].lower()

        raise Exception("No platform supplied for tests! Be sure to pass PLATFORM as environment variable.")

    @staticmethod
    def get_coeus_port(cls):
        if cls.is_android:
            return 31204

        if cls.is_ios:
            if cls.is_simulator:
                return 31203
            else:
                return 31204

    @staticmethod
    def setup_port_forwarding(cls):
        if cls.is_android:
            PortForwarding.setup_android_port_forwarding(31203, 31204)
        if cls.is_ios and not cls.is_simulator:
            PortForwarding.setup_ios_port_forwarding(31203, 31204)

    @staticmethod
    def get_app_start_delay():
        return DEFAULT_APP_START_DELAY

    @staticmethod
    def setup_appium(cls):
        raise Exception("You must implement the setup_appium method!")

    @staticmethod
    def teardown(cls):
        return
