import random
import requests
from concurrent.futures import ThreadPoolExecutor as ThreadPool
import logging
import time
from config import HOST

PROMPT_SAMPLE = ["Illustrate a scene inside the labyrinth of the Moon Palace, where the 'Magical Pig Snout' is sniffing out the direction towards Chang'e. The labyrinth should look vast and complex, with Pigsy appearing both determined and hopeful.",
                 "The 'Magical Pig Snout': This item is full of absurdity and humor. Typically, a pig's snout represents gluttony. The image should capture this humor by showing the snout in action, sniffing out food in the most unexpected places."]


def mj_fetch_task(task_id):
    time_cnt = 1
    limit = 120
    while time_cnt <= limit:
        res = requests.get(HOST + "/mj/task/{}/fetch".format(task_id))
        if res.status_code == 200:
            res = res.json()
            logging.info(res)
            if res["status"] == "SUCCESS":
                return res["imageUrl"]
            else:
                logging.info(
                    "task_id {} action {} Waiting for result, cnt {}...".format(task_id, time_cnt))
                time.sleep(1)
                time_cnt += 1
        else:
            limit = 3
            logging.info("task_id {} status {} Waiting for result, cnt {}...".format(
                task_id, res.status_code, time_cnt))
            time.sleep(1)
            time_cnt += 1
            return None
    return None


def mj_imagine(prompt):
    try:
        res = requests.post(HOST + "/mj/submit/imagine",
                            json={"prompt": prompt})
        task_id = res.json()["result"]
        if not mj_fetch_task(task_id):
            logging.info("imagine task_id {} failed".format(task_id))
            return None
        return task_id

    except Exception as e:
        logging.info(str(e), str(e.with_traceback()))
        return None


def mj_upscale(task_id):
    try:
        res = requests.post(HOST + "/mj/submit/change",
                            json={"action": "UPSCALE", "taskId": task_id, "index": 1})
        task_id = res.json()["result"]
        if not mj_fetch_task(task_id):
            logging.info("upscale task_id {} failed".format(task_id))
            return None
        return mj_fetch_task(task_id)

    except Exception as e:
        logging.info(str(e), str(e.with_traceback()))
        return None


def imagine(prompt):
    task_id = mj_imagine(prompt)
    if task_id:
        image = mj_upscale(task_id)
        if image:
            logging.info(image)
    return None


def main():
    logging.basicConfig(filename='imagine.log', level=logging.DEBUG)
    with ThreadPool(max_workers=10) as pool:
        for prompt in PROMPT_SAMPLE:
            pool.submit(mj_imagine, prompt)
            time.sleep(random.randint(1, 5))
        pool.shutdown(wait=True)


if __name__ == "__main__":
    main()
