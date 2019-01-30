# coeus-python-template
Example implementation of coeus-python-framework for Unity UI tests

## About
This repository both serves as an example, and to provide a `BaseTestCase` which can be used to simplify setup for product UI integration tests.

### Downstream Changes

The base repository: [https://github.com/AgeOfLearning/coeus-python-template](https://github.com/AgeOfLearning/coeus-python-template) should be forked into a product specific test repository. All downstream changes should be pulled into your branches. 

This ensures that libraries and expectations are met.

## Requirements
This project uses the following python packages. Be sure to run `pip install -r requirements.txt`.

* [coeus-python-framework](https://github.com/AgeOfLearning/coeus-python-framework)
* [coeus-unity-python-framework](https://github.com/AgeOfLearning/coeus-unity-python-framework)
* [coeus-appium-bindings](https://github.com/AgeOfLearning/coeus-appium-bindings)

## Project Structure
`builds/`: Should contain product specific builds organized by product name and platform.

`tests/{productName}/`: Contains the collection of product unit-test cases.

`tests/support/`: Contains utilities provided by the template. These shouldn't be changed in the forks, and instead accept downstream changes.

### Android / Android Simulator
1. Install Appium Desktop Application
2. Create a new Android Simulator in AndroidStudio and ensure it is running `OR` connect a local android device.
3. Run your tests.

### iOS Simulator
1. Install Appium Desktop Application
3. Run your tests. 

### iOS Device
1. Install Appium Desktop Application
2. Follow documentation on manual config for Appium. This requires re-building of iOS library for WebDriverAgentRunner with a custom bundle-id. Once built, the web driver agent should run correctly.
3. If enterprise signed, you may need to trust the profile in Settings/General everytime you run.
3. Run your tests. 

## Writing Tests

### Setup TestCase
Create a new class under the `tests/{product}/` folder where `{product}` is your product name, and extend the BaseTestCase.

```python
from source.coeus_template.base_test_case import BaseTestCase

class MyProductTestCase(BaseTestCase):
```

### Setup Appium
Override the static method `setup_appium` to control per-platform capabilities, and to inform where your `app` is located.

```python
@staticmethod
def setup_appium(cls):
    if cls.platform == "android-simulator":
        # Use provided quick-start setup or fill out capabilities yourself...
        cls.appium.setup_android_simulator()
        cls.appium.capabilities["app"] = "/Users/admin/Desktop/myproduct.apk"

    if cls.platform == "iphone-simulator":
        cls.appium.setup_iphone_simulator()
        cls.appium.capabilities["app"] = "/Users/admin/Library/Developer/Xcode/DerivedData/Unity-iPhone-bgwiyygblppdbabnvyanazndtqxx/Build/Products/ReleaseForRunning-iphonesimulator/myproduct.app"

```

### Setup Coeus
If you want to override the defaults, you can implement the following static methods. Since `coeus` is a TCP protocol, you may need to forward ports in certain cases.

```python
@staticmethod
def get_coeus_port(cls):
    if cls.is_android:
        return 31204
    if cls.is_ios and cls.is_iphone_simulator:
        return 31203

@staticmethod
def setup_port_forwarding(cls):
    if cls.is_android:
        PortForwarding.setup_android_port_forwarding(31203, 31204)
    if cls.is_ios:
        PortForwarding.setup_ios_port_forwarding(31203, 31204)
```

### Create Tests
Each test should follow a pattern like: `test_##_{test_name}` where `##` is a sequence of numbers. This allows your tests to be invoked in order, since by default, `unittest` sorts by name. This allows you to modularize your tests and ensure they are called in the specific order for state control.

```python
def test_00_login_to_product(self):
    ...

def test_01_launch_activity(self):
    ...
```

### Adding Builds
Builds should be added into the `builds/{product}/{platform}` folder path. This allows the repository to version the builds with the integration tests that they cover. Be sure to use Git LFS to track the binaries.

## Running Tests

To run the tests, run `py.test --log-cli-level=INFO`. Make sure to export the following environment variables:

`PLATFORM`: `ios, android`

`SIMULATOR` : `android-simulator, iphone-simulator, ipad-simulator`

## Debugging Tests
Use the included `main.py` to run with your IDE. From here, you can debug with breakpoints. 
```python
python main.py
```