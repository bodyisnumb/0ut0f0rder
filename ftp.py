from pymongo import MongoClient
import ftplib
import gridfs



#  Connect and login to the FTP server.
ftp = ftplib.FTP("192.168.0.127")
ftp.login(user='pi', passwd='feedus321')
ftp.cwd('/files')


def get_list():
    # Create list of photos
    files = []

# Print list of files in remote directory
    try:
        files = ftp.nlst()
    except ftplib.error_perm as resp:
        if str(resp) == "550 No files found":
            print("No files in this directory")
        else:
            raise

    for f in files:
        print(f)


def size_check():
    # Check if file exists
    ftp.cwd('/home/pi/ftp/files')
    ftp.sendcmd("TYPE i")
    file_size = ftp.size("photo.jpg")
    if file_size < 0:
        print("file does not exist")
    else:
        print("file exists and is " + str(file_size) + " bytes in size")


def grab_file():
    # Get file from the remote directory
    ftp.cwd('/home/pi/ftp/files')
    file_name = "photo.jpg"
    local_file = open(file_name, 'rb')
    ftp.retrbinary('RETR' + file_name, local_file.write, 1024)
    ftp.quit()
    local_file.close()


#def place_file():
#    filename = 'photo.jpg'
#    ftp.storbinary('STOR '+filename, open(filename, 'rb'))
#    ftp.quit()

def load_to_db_by_name():
    my_db = MongoClient().test
    fs = GridFSBucket(my_db)
    # Get file to write to
    file = open('photo.jpg','wb')
    fs.load_to_db_by_name("photo.jpg", file)

if __name__ == "__main__":
    get_list()
    size_check()
    grab_file()
#    place_file()
    load_to_db_by_name()
