import os
import subprocess
import threading

process = None

def start_ocpp_simulator():
    global process

    project_dir = os.path.expanduser("~/Projects")
    jar_file = "OCPPSimulatorWeb-0.01.jar"

    jar_path = os.path.join(project_dir, jar_file)
    if not os.path.isfile(jar_path):
        raise FileNotFoundError(f"Unable to access jarfile {jar_file}")

    env = os.environ.copy()

    java_command = ["java", "-jar", jar_file]
    process = subprocess.Popen(java_command, cwd=project_dir, env=env)

    print("[OCPP Simulator] started.")

def close_ocpp_simulator():
    global process

    if process:
        print("[OCPP Simulator] Closing...")
        process.terminate()
        process = None
    else:
        print("[OCPP Simulator] is not running.")

def run_tests():
    from tests.test_app_charging import TestAppCharging

    test_app = TestAppCharging()
    test_app.test_app_different_connector_charging()

def start_simulator_and_run_tests():
    ocpp_thread = threading.Thread(target=start_ocpp_simulator)
    ocpp_thread.start()

    # Make sure the simulator has started before running tests
    ocpp_thread.join()

    run_tests()

    print("Tests finished.")