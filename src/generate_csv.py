import csv, tkMessageBox
from Tkinter import *
from datetime import datetime, timedelta
# from gui import MyDialog

# add "prof" as command line argument to profile program
######### profiling options ###################################################

if "prof" in sys.argv:
    profile = True
else:
    profile = False

if profile:
    import cProfile, pstats, StringIO
    pr = cProfile.Profile()
    pr.enable()
######### profiling options ###################################################


#open a dialog and store resullts
class Generate_csv(object):

    def __init__(self, input_file, year, month, day, hour, minute, second):
        self.input_file = input_file
        self.outputt_file = ""
        self.start = datetime(year = year, month  = month, day = day, hour = hour, minute = minute,
                second = second)
        self.date_time = []
        self.channel = []
        self.intensity = []
        self.interval = []
        self.copy = []

    def create(self):
        # roud our profile and add it to our datetimeclass and append that in an array
        # you'd think this is horribly slow but it's not that bad.
        try:
            with open(self.input_file, 'rb') as f:

                reader = csv.reader(f)
                next(reader, None)
                try:
                    for row in reader:
                        #TODO: make it give error when non numeric input
                        new = self.start + timedelta(hours = int(row[0]), minutes = int(row[1]), seconds = int(row[2]))
                        self.date_time.append(new)
                        self.channel.append(row[3])
                        self.intensity.append(row[4])
                        self.interval.append(row[5])
                        self.copy.append(row[6])
                except csv.Error as error:
                    sys.exit('file %s, line %d: %s' % (self.input_file, reader.line_num, error))
        except IOError:
            tkMessageBox.showwarning(
                        "input file error",
                        "input file not found\nplease check the input file name"
                    )


        # should always be same length
        # probably can't hapen but should check anyways
        if not len(self.date_time) == len(self.intensity) == len(self.interval) == len(self.copy):
            raise Exception("hours, minutes and seconds not same length")

    def write(self, output_file):

        self.output_file = output_file
        # write out stuff away
        f = open(self.output_file, "wb")
        writer = csv.writer(file)
        writer.writerow(["date(dd-mm-yyy)","time(hh:mm:ss)","channel(1-40)",
                "intensity(%)","interval(sec.)"])

        for idx in xrange(0,len(self.date_time)):
            # do we want to copy settings to all 4 armatures?
            if self.copy[idx] == "1":
                end = 4
            else:
                end = 1
            for chan in xrange(0, end):
                writer.writerow([(str(self.date_time[idx].day) + "-" +  str(self.date_time[idx].month) + "-"  + str(self.date_time[idx].year)),
                                (str(self.date_time[idx].hour) + ":" +  str(self.date_time[idx].minute) + ":"  + str(self.date_time[idx].second)),
                                int(self.channel[idx]) + (chan ) * 10 , self.intensity[idx], self.interval[idx]])
        f.close()

    ######### profiling options ###################################################
        if profile:
            pr.disable()
            s = StringIO.StringIO()
            sortby = 'cumulative'
            ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
            ps.print_stats()
            print s.getvalue()
    ######### profiling options ###################################################

if __name__ == "__main__":
    data = Generate_csv("profile.csv", "output.csv", 2000, 12, 1, 1, 1, 1)
    data.create()
    data.write()



