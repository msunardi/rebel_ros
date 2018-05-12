import subprocess
import threading
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-9s) %(message)s',)

class Executor:
    '''
    Executor class for concurrency operator
    '''

    echo_fu = ["echo", "fu"]
    echo_bar = ["echo", "bar"]
    echo_baz = ["echo", "baz"]
    echo_hello = ["echo", "hello"]
    echo_world = ["echo", "world"]
    sh_helloworld = ["sh", "hello_world.sh"]
    sh_fubar = ["sh", "fubar.sh"]
    sp_call = subprocess.call       # Each call is blocking
    sp_popen = subprocess.Popen     # Fire-and-forget; each call does not block

    def execute(self, args):
        print "Start executing: {}".format(args)
        ctasks = [a.strip() for a in args.split('|')]

        # METHOD 1
        # if len(ctasks) > 1:
        #     print "Ctasks: %s" % ctasks
        #     map(self.excall, ctasks)     # Execute concurrent events

        # METHOD 2 (Use threads)
        # Prepare each concurrent event as task to execute
        tasks = []
        for task in ctasks:
            tasks.append(Task(task))

        for task in tasks:
            task.start()

        for task in tasks:
            task.join()

    def excall(self, args):
        print "---"
        for arg in args:
            if arg == ' ':
                continue
            if arg == 'a':
                self.sp_call(self.sh_helloworld)
            elif arg == 'b':
                self.sp_call(self.sh_helloworld)
            elif arg == 'c':
                self.sp_call(self.sh_fubar)
            elif arg == 'd':
                self.sp_call(self.sh_fubar)
            else:
                self.sp_popen(self.echo_baz)
        print "---"


class Task(threading.Thread):
    sp_call = subprocess.call
    task_buffer = []
    echo_fu = ["echo", "fu"]
    echo_bar = ["echo", "bar"]
    echo_baz = ["echo", "baz"]
    echo_hello = ["echo", "hello"]
    echo_world = ["echo", "world+"]
    sh_helloworld = ["sh", "hello_world.sh"]
    sh_fubar = ["sh", "fubar.sh"]

    def __init__(self, args):
        super(Task, self).__init__(group=None, target=None, args=args, kwargs=None, verbose=None)
        self.task_buffer = []
        for arg in args:
            if arg == ' ':
                continue
            if arg == 'a':
                darg = self.sh_fubar
            elif arg == 'b':
                darg = self.echo_bar
            elif arg == 'c':
                darg = self.sh_helloworld
            elif arg == 'd':
                darg = self.echo_world
            else:
                darg = self.sh_fubar
            self.task_buffer.append((self.sp_call, darg))

    def run(self):
        for cmd, task in self.task_buffer:
            # logging.debug('Cmd: {}, task: {}'.format(cmd, task))
            # cmd(task)
            # print(cmd)
            assert type(task) == list
            print(type(task), len(task))
            subprocess.call(task)
        print("Done with task.")

if __name__ == "__main__":
    e = Executor()

    e.execute('a | b')
    e.execute('a | c d')