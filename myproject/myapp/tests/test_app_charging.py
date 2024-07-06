import random
import time
from config import Config
from service.app_session_service import AppSessionService
from service.browser_service import BrowserService
from service.ocpp_simulator_service import OcppSimulatorService
from service.sky_ocpi_service import SkyOcpiService
from tests.utils.test_helper import TestHelper
from .test_data_set import test_p360_abb_multiple_evses

class TestAppCharging:

    def __init__(self):
        self.sky_ocpi_service = SkyOcpiService()
        self.browser = BrowserService.get_instance()
        self.token = Config.APP_ID_TAG

    def test_app_charging(self) -> bool:
        random_evse = TestHelper.get_random_evse(test_p360_abb_multiple_evses)
        app_service = AppSessionService(random_evse)
        ocpp_service = OcppSimulatorService(random_evse)

        # Start Session
        session_id = app_service.start_session()
        time.sleep(self.browser.timeout_middle)

        if session_id:
            
            app_tx_id = ocpp_service.start_trasanction(self.token)
            time.sleep(self.browser.timeout_middle)

            session_status = app_service.wait_for_session_status(session_id=session_id, status="started")
            if session_status == 'started':
                print(f"APP: Session {app_tx_id} has started successfully.")
            else:
                print(f"APP: Session {session_id} did not start. Current status: {session_status}")

        else:
            print("APP: Failed to start session from TNM.")
            return False
        
        time.sleep(Config.WAIT_ONE_MINUTE)

        # Stop Session
        if app_service.stop_session(session_id):
            ocpp_service.stop_transaction(tx_id=app_tx_id, id_tag=self.token)
            time.sleep(self.browser.timeout_middle)

            session_status = app_service.wait_for_session_status(session_id=session_id, status="stopped")
            if session_status == 'stopped':
                print(f"APP: Session {app_tx_id} has stopped successfully.")
            else:
                print(f"APP: Session {session_id} did not stop. Current status: {session_status}")
        return True


    def test_app_diiferent_connector_charging(self) -> bool:
        random_evse = TestHelper.get_connector(test_set=test_p360_abb_multiple_evses, connector_id="1")
        app_service = AppSessionService(random_evse)
        ocpp_service = OcppSimulatorService(random_evse)

        # Start Session
        session_id = app_service.start_session()
        time.sleep(self.browser.timeout_middle)

        if session_id:
            
            app_tx_id = ocpp_service.start_tx_different_connectors(self.token)
            time.sleep(self.browser.timeout_middle)

            session_status = app_service.wait_for_session_status(session_id=session_id, status="started")
            if session_status == 'started':
                print(f"APP DIFF: Session {app_tx_id} has started successfully.")
            else:
                print(f"APP DIFF: Session {session_id} did not start. Current status: {session_status}")

        else:
            print("APP DIFF: Failed to start session from TNM.")
            return False
        
        time.sleep(Config.WAIT_ONE_MINUTE)

        # Stop Session
        app_service.stop_session(session_id)
        ocpp_service.stop_transaction(tx_id=app_tx_id, id_tag=self.token)
        time.sleep(self.browser.timeout_middle)

        if self.sky_ocpi_service.find_id_in_cdrs(app_tx_id):
            print(f"[PASS] APP DIFF Session {app_tx_id} has stopped successfully.")
            return True
        else:
            print(f"[FAIL] APP DIFF Session {session_id} did not stop. Current status: {session_status}")
            return False


