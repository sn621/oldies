import argparse
import pandas as pd
import numpy as np

# argument configuration
parser = argparse.ArgumentParser(description='reshape run conditions')
parser.add_argument('-d','--date',help='Analysis Date')
args=parser.parse_args()



abspath_condition = '/Users/ssakurai/Research/Backup/MAGIC/DataConditionCSV/1ES1959+650'
convdate = args.date[0:4]+"_"+args.date[4:6]+"_"+args.date[6:8]

def main():
    datalist = pd.read_csv(abspath_condition+'/'+convdate+'_check_quality_1ES1959+650_moon.csv')
    dataset = datalist.sort_values(by=datalist.columns[1])
    dataset.set_index(datalist.columns[1],inplace=True)
    # main loop
    priv_runnumber = np.unique(np.sort(dataset.query('Name=="Runnumber"')[datalist.columns[2]]))[0]
    runnums=[]

    trans9=[]
    meantrans9=[]
    mintrans9=[]
    maxtrans9=[]

    trans6=[]
    meantrans6=[]
    mintrans6=[]
    maxtrans6=[]

    trans3=[]
    meantrans3=[]
    mintrans3=[]
    maxtrans3=[]

    humis=[]
    meanhumis=[]
    minhumis=[]
    maxhumis=[]

    clouds=[]
    meanclouds=[]
    minclouds=[]
    maxclouds=[]

    czds=[]
    meanczds=[]
    minczds=[]
    maxczds=[]

    nzds=[]
    meannzds=[]
    minnzds=[]
    maxnzds=[]

    nstars=[]
    meannstars=[]
    minnstars=[]
    maxnstars=[]

    mhvs=[]
    meanmhvs=[]
    minmhvs=[]
    maxmhvs=[]

    meddcs=[]
    meanmeddcs=[]
    minmeddcs=[]
    maxmeddcs=[]

    mdcs=[]
    meanmdcs=[]
    minmdcs=[]
    maxmdcs=[]

    for i in range(dataset.shape[0]):
        item = dataset.iloc[i]['Name']
        value = dataset.iloc[i][' Value']
        if(item=="Runnumber"):
            if(priv_runnumber!=value):
                runnums.append(priv_runnumber)
                if (len(trans9) != 0):
                    mintrans9.append(np.min(trans9));maxtrans9.append(np.max(trans9));meantrans9.append(np.mean(trans9))
                    mintrans6.append(np.min(trans6));maxtrans6.append(np.max(trans6));meantrans6.append(np.mean(trans6))
                    mintrans3.append(np.min(trans3));maxtrans3.append(np.max(trans3));meantrans3.append(np.mean(trans3))
                else:
                    mintrans9.append(0);maxtrans9.append(0);meantrans9.append(0)
                    mintrans6.append(0);maxtrans6.append(0);meantrans6.append(0)
                    mintrans3.append(0);maxtrans3.append(0);meantrans3.append(0)
                if (len(humis) != 0):
                    minhumis.append(np.min(humis));maxhumis.append(np.max(humis));meanhumis.append(np.mean(humis))
                else:
                    minhumis.append(0);maxhumis.append(0);meanhumis.append(0)

                minclouds.append(np.min(clouds));maxclouds.append(np.max(clouds));meanclouds.append(np.mean(clouds))
                minnzds.append(np.min(nzds));maxnzds.append(np.max(nzds));meannzds.append(np.mean(nzds))
                minczds.append(np.min(czds));maxczds.append(np.max(czds));meanczds.append(np.mean(czds))
                if (len(nstars) != 0):
                    minnstars.append(np.min(nstars));maxnstars.append(np.max(nstars));meannstars.append(np.mean(nstars))
                else:
                    minnstars.append(0);maxnstars.append(0);meannstars.append(0)
                minmhvs.append(np.min(mhvs));maxmhvs.append(np.max(mhvs));meanmhvs.append(np.mean(mhvs))
                minmeddcs.append(np.min(meddcs));maxmeddcs.append(np.max(meddcs));meanmeddcs.append(np.mean(meddcs))
                minmdcs.append(np.min(mdcs));maxmdcs.append(np.max(mdcs));meanmdcs.append(np.mean(mdcs))
                priv_runnumber=value
                trans9=[]
                trans6=[]
                trans3=[]
                humis=[]
                clouds=[]
                czds=[]
                nzds=[]
                nstars=[]
                mhvs=[]
                meddcs=[]
                mdcs=[]
            else:
                continue
        if(item=="Trans9km"):
            trans9.append(value)
        if(item=="Trans3km"):
            trans3.append(value)
        if(item=="Trans6km"):
            trans6.append(value)
        if(item=="Humidity"):
            humis.append(value)
        if(item=="Cloudiness"):
            clouds.append(value)
        if(item=="MeanDC"):
            mdcs.append(value)
        if(item=="MedDC"):
            meddcs.append(value)
        if(item=="MeanHV"):
            mhvs.append(value)
        if(item=="CurZd"):
            czds.append(value)
        if(item=="NomZd"):
            nzds.append(value)
        if(item=="NumStars"):
            nstars.append(value)
        #print(i,priv_runnumber)
    runnums.append(priv_runnumber)
    ##print(priv_runnumber)
    if (len(trans9) != 0):
        mintrans9.append(np.min(trans9));maxtrans9.append(np.max(trans9));meantrans9.append(np.mean(trans9))
        mintrans6.append(np.min(trans6));maxtrans6.append(np.max(trans6));meantrans6.append(np.mean(trans6))
        mintrans3.append(np.min(trans3));maxtrans3.append(np.max(trans3));meantrans3.append(np.mean(trans3))
    else:
        mintrans9.append(0);maxtrans9.append(0);meantrans9.append(0)
        mintrans6.append(0);maxtrans6.append(0);meantrans6.append(0)
        mintrans3.append(0);maxtrans3.append(0);meantrans3.append(0)
    if (len(humis) != 0):
        minhumis.append(np.min(humis));maxhumis.append(np.max(humis));meanhumis.append(np.mean(humis))
    else:
        minhumis.append(0);maxhumis.append(0);meanhumis.append(0)
    if (len(clouds) != 0):
        #minhumis.append(np.min(humis));maxhumis.append(np.max(humis));meanhumis.append(np.mean(humis))
        minclouds.append(np.min(clouds));maxclouds.append(np.max(clouds));meanclouds.append(np.mean(clouds))
    else:
        minclouds.append(0);maxclouds.append(0);meanclouds.append(0)
        #minhumis.append(0);maxhumis.append(0);meanhumis.append(0)
    #minclouds.append(np.min(clouds));maxclouds.append(np.max(clouds));meanclouds.append(np.mean(clouds))
    minnzds.append(np.min(nzds));maxnzds.append(np.max(nzds));meannzds.append(np.mean(nzds))
    minczds.append(np.min(czds));maxczds.append(np.max(czds));meanczds.append(np.mean(czds))
    if (len(nstars) != 0):
        minnstars.append(np.min(nstars));maxnstars.append(np.max(nstars));meannstars.append(np.mean(nstars))
    else:
        minnstars.append(0);maxnstars.append(0);meannstars.append(0)
    minmhvs.append(np.min(mhvs));maxmhvs.append(np.max(mhvs));meanmhvs.append(np.mean(mhvs))
    minmeddcs.append(np.min(meddcs));maxmeddcs.append(np.max(meddcs));meanmeddcs.append(np.mean(meddcs))
    minmdcs.append(np.min(mdcs));maxmdcs.append(np.max(mdcs));meanmdcs.append(np.mean(mdcs))
    priv_runnumber=value

    for i in range(len(runnums)):

        # HV check
        if (meanmhvs[i] >= 900):
            hvflag='Nominal'
        else :
            hvflag='Reduced'

            # NSB check
        if (hvflag=='Nominal'):
            if(meanmeddcs[i] < 2.2):
                dcflag='NSB1-2'
            elif (meanmeddcs[i] >= 2.2 and meanmeddcs[i] < 3.3):
                dcflag='NSB2-3'
            elif (meanmeddcs[i] >= 3.3 and meanmeddcs[i] < 5.5):
                dcflag='NSB3-5'
            elif (meanmeddcs[i] >= 5.5 and meanmeddcs[i] < 8.8):
                dcflag='NSB5-8'
            elif (meanmeddcs[i] >= 8.8 and meanmeddcs[i] < 13.2):
                dcflag='NSB8-12'
            else:
                dcflag='TooBlight'
        else:
            if(meanmeddcs[i] < 3.2):
                dcflag='TooDark'
            elif (meanmeddcs[i] >= 3.2 and meanmeddcs[i] < 5.2):
                dcflag='NSBr5-8'
            elif (meanmeddcs[i] >= 5.2 and meanmeddcs[i] < 7.8):
                dcflag='NSBr8-12'
            elif (meanmeddcs[i] >= 7.8 and meanmeddcs[i] < 11.6):
                dcflag='NSBr12-18'
            else:
                dcflag='TooBlight'


        # Zd Check
        if (maxczds[i] <= 62):
            zdvalue=''
        else:
            zdvalue='Zd > 62'

        #clouf Check
        if (maxclouds[i] <= 35):
            cdvalue=''
        else:
            cdvalue='Cloud > 35'

        print('| {:s} || {:.0f} || {:.1f} || {:.1f} || {:.1f} || {:s} || {:s} || {:.1f} || {:.1f} || {:s} || {:.2f} || {:.2f} || {:.2f} || {:.1f} || {:s} || {:.1f} || {:.1f}'.format(
            args.date,
            runnums[i],minmeddcs[i],maxmeddcs[i],meanmeddcs[i],dcflag,hvflag,
            minnzds[i],maxnzds[i],zdvalue,
            meantrans3[i],meantrans6[i],meantrans9[i],
            meanclouds[i],cdvalue,meanhumis[i],meannstars[i]))
        print('|-')

if __name__ == "__main__":
    main()
