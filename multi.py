from multiprocessing import Process, Manager, Lock
from app import NextApp
from backend import BlinkWinkApp
from soundPlayer import deaf
def run_next_app(shared_dict, lock):
    NextApp(shared_dict, lock).run()

def run_blink_wink_app(shared_dict, lock):
    bwa = BlinkWinkApp(shared_dict, lock)
    bwa.blink_wink_detection()

def monitor_keyboard_mode(shared_dict):
    while True:
        if not shared_dict['keyboard_mode'] and shared_dict['voice_mode']:
            p3 = Process(target=deaf)
            p3.start()
            p3.join()

if __name__ == "__main__":
    manager = Manager()
    lock = Lock()
    shared_dict = manager.dict()

    shared_dict['angle'] = 0.0
    shared_dict['distance'] = 0.0
    shared_dict['blink'] = False
    shared_dict['key'] = ""
    shared_dict['keyboard_mode'] = False
    shared_dict['image'] = manager.list()
    shared_dict['voice_mode'] = False
    shared_dict['canvas'] = None
    shared_dict['msg'] = "Next app is running! :)"
    shared_dict['x_y'] = [300, 250]
    shared_dict['backend_stat'] = True

    p1 = Process(target=run_next_app, args=(shared_dict, lock))
    p2 = Process(target=run_blink_wink_app, args=(shared_dict, lock))

    p1.start()
    p2.start()

    monitor_keyboard_mode(shared_dict)

    p1.join()
    p2.join()
