import datetime

def formatting_filename(video):
    nowtime = datetime.datetime.now()
    print(nowtime)
    date, time = str(nowtime).split(' ')
    times = str(time).split('.')[0]
    times = times.replace(':', '-')
    filename = '_'.join([date, times, video])
    return filename