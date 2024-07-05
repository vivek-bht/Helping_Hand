from multiprocessing import Manager, Pool
from app import NextApp
from backend import BlinkWinkApp

def run_next_app(shared_dict, lock):
    NextApp(shared_dict, lock).run()

def run_blink_wink_app(shared_dict, lock):
    bwa = BlinkWinkApp(shared_dict, lock)
    bwa.blink_wink_detection()

if __name__ == "__main__":
    manager = Manager()
    lock = manager.Lock()
    shared_dict = manager.dict()

    shared_dict['angle'] = 0.0
    shared_dict['distance'] = 0.0
    shared_dict['blink'] = False
    shared_dict['keyboard_mode'] = False
    shared_dict['image'] = manager.list()
    shared_dict['voice_mode'] = False
    shared_dict['msg'] = "Helping Hand is running! :)"
    shared_dict['x_y'] = [300, 250]
    shared_dict['backend_stat'] = True
    shared_dict['scroll'] = False

    pool = Pool(processes = 2)
    p1=pool.apply_async(run_next_app, args=(shared_dict, lock))
    p2=pool.apply_async(run_blink_wink_app, args=(shared_dict, lock))

    p1.get()
    p2.get()

    pool.close()
    pool.join()

    