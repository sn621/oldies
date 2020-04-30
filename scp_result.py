import subprocess
import logging
import argparse
import datetime

# argument configuration
parser = argparse.ArgumentParser(description='you can download analysis results from MPP server')
parser.add_argument('-s','--server',help='indicate mpp server',default='mpp1')
parser.add_argument('-p','--period',help='Analysis Period',type=int)
parser.add_argument('-n','--nsb',help='NSB Level')
parser.add_argument('-d','--date',help='Analysis Date')
args=parser.parse_args()

# dictionary for filename-sufix
sizecut = {'2-3':'80','3-5':'110','5-8':'150','8-12':'200',
           'r5-8':'135','r8-12':'170','r12-18':'220'}

# logging configuration
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# config for stdstream
sh = logging.StreamHandler()
sh.setLevel(logging.WARNING)
sh_formatter = logging.Formatter(
    fmt='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%m/%d %H:%M:%S')
sh.setFormatter(sh_formatter)
logger.addHandler(sh)

# config for file
dt_now = datetime.datetime.now()
fh = logging.FileHandler(filename='/Users/ssakurai/Research/BackupLog/{0}_{1}.log'.format(parser.prog[:-3],dt_now.strftime('%Y%m%d_%H%M%S')))
fh.setLevel(logging.DEBUG)
fh_formatter = logging.Formatter(
    fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y/%m/%d %H:%M:%S')
fh.setFormatter(fh_formatter)
logger.addHandler(fh)

# path configuration
abspath_result = '/remote/ceph/user/s/ssakurai/Data/1ES1959+650'

def run_process(command):
    returns = subprocess.Popen(command,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    stdout, stderr = returns.communicate()
    return stdout.decode('utf-8'), stderr.decode('utf-8')

def main():
    logger.info('SCP starts')

    cmd_star = ['scp','{0.server}:{1:}/ST.03.{0.period:02d}/Star/NSB{0.nsb}/{0.date}/star*root'.format(args,abspath_result),'.']
    ret_star = run_process(cmd_star)
    logger.info(ret_star[0])
    logger.error(ret_star[1])

    cmd_odie = ['scp','{0.server}:{1:}/ST.03.{0.period:02d}/Odie/NSB{0.nsb}/{0.date}/Output*root'.format(args,abspath_result),'.']
    ret_odie = run_process(cmd_odie)
    logger.info(ret_odie[0])
    logger.error(ret_odie[1])

    cmd_flute = ['scp','{0.server}:{1:}/ST.03.{0.period:02d}/Flute/NSB{0.nsb}/{0.date}/*root'.format(args,abspath_result),'.']
    ret_flute = run_process(cmd_flute)
    logger.info(ret_flute[0])
    logger.error(ret_flute[1])

    logger.info('Done')


if '__main__' == __name__:
    main()
