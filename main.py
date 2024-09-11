import json

import requests
import threading


class SingletonInteger:
    def __init__(self, value):
        self.val = value


def fetch_data(post_id):
    try:
        response = requests.get(base_url + str(post_id))
        return response.json()
    except Exception as e:
        print(f"failed to fetch data for post {post_id}")
        return -1


class Worker(threading.Thread):
    def __init__(self, post_id, f_lock, file, curr_id, curr_id_lock):
        super(Worker, self).__init__()
        self.post_id = post_id
        self.file_lock = f_lock
        self.file = file
        self.curr_id = curr_id
        self.curr_id_lock = curr_id_lock

    def run(self):
        post_to_be_fetched = 0
        while True:
            with self.curr_id_lock:
                if self.curr_id.val == 78:
                    break
                else:
                    post_to_be_fetched = self.curr_id.val
                    self.curr_id.val += 1

            res = fetch_data(post_to_be_fetched)

            if res == -1:
                continue

            with self.file_lock:
                data = json.load(open(self.file))
                data.append(res)
                with open(self.file, 'w') as file:
                    json.dump(data, file)


if __name__ == '__main__':
    base_url = "https://jsonplaceholder.typicode.com/posts/"
    filename = 'result.json'

    with open(filename, 'w') as f:
        json_array = []
        json.dump(json_array, f)
        f.close()

    file_lock = threading.Lock()
    num_posts = 77
    num_threads = 30

    curr_post = SingletonInteger(1)
    curr_post_lock = threading.Lock()

    threads = []
    for i in range(num_threads):
        thread = Worker(i, file_lock, filename, curr_post, curr_post_lock)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
