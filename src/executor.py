import subprocess

class Executor:

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
                self.sp_popen(self.sh_helloworld)
            elif arg == 'b':
                self.sp_popen(self.sh_helloworld)
            elif arg == 'c':
                self.sp_popen(self.sh_fubar)
            elif arg == 'd':
                self.sp_popen(self.sh_fubar)
            else:
                self.sp_popen(self.echo_baz)
        print "---"

if __name__ == "__main__":
    e = Executor()

    e.execute('a | b')
    e.execute('a | c d')