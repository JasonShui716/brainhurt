import imagine
import time
from callgpt import GPT
from config import STORY_PROMPT, STORY_SAMPLE, GPT_FOR_MJ_PROMPT, GPT_FOR_MJ_SAMPLE
from multiprocessing import Process, Queue
from concurrent.futures import ThreadPoolExecutor as ThreadPool


class Worker:
    def __init__(self, task, callback=None, max_workers=3, interval_sec=1, interactive=False):
        self.queue = None
        if interactive:
            self.queue = Queue()
        self.task = task
        self.callback = callback
        self.interval_sec = interval_sec
        self.pool = ThreadPool(max_workers)
        self.process = Process(target=self.worker, args=(self.queue,))

        self.process.start()

    def worker(self, queue):
        while True:
            fut = None
            if queue:
                item = queue.get()
                if item:
                    fut = self.pool.submit(self.task, item)
            else:
                fut = self.pool.submit(self.task)
            if fut and self.callback:
                fut.add_done_callback(self.callback)
            time.sleep(self.interval_sec)

    def put(self, item):
        if self.queue:
            self.queue.put(item)

    def wait(self):
        self.process.join()
        self.pool.shutdown(wait=True)


class GPTWorker:
    def __init__(self, init_prompts=None, callback=None, interactive=False):
        self.init_prompts = init_prompts
        self.task = None
        self.worker = None

        if interactive:
            def task(prompt):
                gpt = GPT()
                gpt.set_message(self.init_prompts)
                gpt.add_message(prompt)
                return gpt.call_gpt()
            self.task = task
        else:
            def task():
                gpt = GPT()
                gpt.set_message(self.init_prompts)
                return gpt.call_gpt()
            self.task = task

        self.worker = Worker(task, callback=callback, interactive=interactive)

    def put(self, item):
        self.worker.put(item)

    def wait(self):
        self.worker.wait()


def main():
    imagine_worker = Worker(imagine.imagine, callback=None,
                            interactive=True, interval_sec=10)
    mj_worker = GPTWorker(callback=imagine_worker.put, init_prompts=[
                          {"role": "user", "content": GPT_FOR_MJ_PROMPT},
                          {"role": "assistant", "content": GPT_FOR_MJ_SAMPLE}], interactive=True)
    story_worker = GPTWorker(callback=mj_worker.put, init_prompts=[
        {"role": "user", "content": STORY_PROMPT},
        {"role": "assistant", "content": STORY_SAMPLE},
        {"role": "user", "content": "不错，再来一个"}], interactive=False, interval_sec=30)

    story_worker.wait()
    mj_worker.wait()
    imagine_worker.wait()


if __name__ == "__main__":
    main()
