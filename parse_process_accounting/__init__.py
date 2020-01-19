#!/usr/bin/env python3
import io, sys, json, subprocess, os, re, pprint

pp = pprint.PrettyPrinter(indent=4).pprint
SA_CMD = "sa --separate-times --sort-real-time --user-summary"
SA_COLS = [
	{"name": "quantity","suffix":"None"},
	{"name": "elapsed_time_minutes","suffix":"re"},
	{"name": "user_cputime_seconds","suffix":"u"},
	{"name": "user_cputime_seconds","suffix":"s"},
	{"name": "average_iops","suffix":"avio"},
	{"name": "memory_kilobytes","suffix":"k"},
]


def getStats():
    proc = subprocess.Popen(SA_CMD.split(' '), stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=False,env=os.environ.copy())
    stdout, stderr = proc.communicate()
    exit_code = proc.wait()

    stdout = stdout.decode().strip().splitlines()
    Stats = {}
    R = []
    def addUserStat(stats):
        if len(stats) == len(SA_COLS):
            stats = ['_TOTALS',*stats]
        username = stats[0]
        Stats[username] = {}
        for index, stat in enumerate(stats):
            SA_COL = SA_COLS[index-1]
            if SA_COL['suffix'] and stat.endswith(SA_COL['suffix']):
                stat = re.sub("{}$".format(SA_COL['suffix']),'',stat)
            Stats[username][SA_COL['name']] = stat

        return Stats #[username][SA_COL['name']]
        
    for index, line in enumerate(stdout):
        line = [l for l in line.split(' ') if len(l)>0]
        #print('line={},{}'.format(line,type(line)))

        USER_STAT = addUserStat(line)
        #print('USER_STAT={}'.format(USER_STAT))
    return USER_STAT    
    return R

if __name__ == "__main__":
    print(json.dumps(getStats()))
    sys.exit(0)
