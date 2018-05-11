import subprocess

class Executor:

    def execute(self, args):
        print "Start executing: {}".format(args)
        csync = [a.strip() for a in args.split('|')]

        if len(csync) > 1:
            print "Csync: %s" % csync
            map(self.excall, csync)

    def excall(self, args):
        print "---"
        for arg in args:
            if arg == ' ':
                continue
            if arg == 'a':
                subprocess.call(["echo", "fu"])
            elif arg == 'b':
                subprocess.call(["echo", "bar"])
            elif arg == 'c':
                subprocess.call(["echo", "hello"])
            elif arg == 'd':
                subprocess.call(["echo", "world"])
            else:
                subprocess.call(["echo", "baz"])
        print "---"

if __name__ == "__main__":
    e = Executor()

    e.execute('a | b')
    e.execute('a | c d')