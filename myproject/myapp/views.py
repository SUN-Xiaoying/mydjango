from django.shortcuts import redirect, render, HttpResponse

from .utils import wake_up_ocpp_simulator, close_wake_up_ocpp_simulator

# Create your views here.
def home(request):
    return render(request, 'home.html')


def start_simulator(request):
    wake_up_ocpp_simulator()
    return redirect('home')

def stop_simulator(request):
    close_wake_up_ocpp_simulator()
    return redirect('home')

def run_tests_view(request):
    start_simulator_and_run_tests()
    return redirect('home')