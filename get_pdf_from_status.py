import subprocess
import logging
import argparse
import datetime

# argument configuration
parser = argparse.ArgumentParser(description='make pdf from Status*root')
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

abspath_soft = '/Users/ssakurai/Research/Backup/MAGIC/magicsoft'

def run_process(command):
    returns = subprocess.Popen(command,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    stdout, stderr = returns.communicate()
    return stdout.decode('utf-8'), stderr.decode('utf-8')

def pdf_flute(args):
    cmd_flute = ['root','-b','-q','{0}/SaveCanvasFlute.C(\"./Status_flute_{1.nsb:}_{1.date:}_{2}.root\")'.format(abspath_soft,args,sizecut[args.nsb])]
    ret_flute = run_process(cmd_flute)
    logger.info(ret_flute[0])
    logger.error(ret_flute[1])

def pdf_star(args):
    cmd_star = ['root','-b','-q','{0}/SaveCanvasStar.C(\"./star_{1.nsb:}_{1.date:}_M1.root\")'.format(abspath_soft,args)]
    ret_star = run_process(cmd_star)
    logger.info(ret_star[0])
    logger.error(ret_star[1])
    cmd_star = ['root','-b','-q','{0}/SaveCanvasStar.C(\"./star_{1.nsb:}_{1.date:}_M2.root\")'.format(abspath_soft,args)]
    ret_star = run_process(cmd_star)
    logger.info(ret_star[0])
    logger.error(ret_star[1])

def pdf_odie(args):
    cmd_odie = ['root','-b','-q','{0}/SaveCanvasOdie.C(\"./Output_odie_FR_{1.nsb:}_{1.date:}.root\")'.format(abspath_soft,args)]
    ret_odie = run_process(cmd_odie)
    logger.info(ret_odie[0])
    logger.error(ret_odie[1])
    cmd_odie = ['root','-b','-q','{0}/SaveCanvasOdie.C(\"./Output_odie_LE_{1.nsb:}_{1.date:}.root\")'.format(abspath_soft,args)]
    ret_odie = run_process(cmd_odie)
    logger.info(ret_odie[0])
    logger.error(ret_odie[1])

def main():
    pdf_flute(args)
    pdf_odie(args)
    pdf_star(args)

if __name__ == "__main__":
    main()
