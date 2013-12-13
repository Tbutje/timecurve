import os
import tkFileDialog


def askopenfilename():

    """Returns an opened file in read mode.
    This time the dialog just returns a filename and the file is opened by your own code.
    """
    file_opt = options = {}
    options['defaultextension'] = '.csv'
    options['filetypes'] = [('all files', '.*'), ('csv files', '.csv')]
    options['initialdir'] = os.getcwd()
    options['initialfile'] = 'profile.csv'
    options['title'] = 'choose file'

    # get filename
    filename = tkFileDialog.askopenfilename(**file_opt)

    # open file on your own
    return filename
