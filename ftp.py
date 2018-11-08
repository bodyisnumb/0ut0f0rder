import ftplib


#  Connect and login to the FTP server.
ftp = ftplib.FTP("192.168.0.127")
ftp.login(user='pi', passwd='feedus321')
ftp.cwd('/files')


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

# Check if file exists
ftp.sendcmd("TYPE i")
file_size = ftp.size("/home/pi/ftp/files/photo.jpg")
if file_size < 0:
    print("file does not exist")
else:
    print("file exists and is " + str(file_size) + " bytes in size")


# Get file from the remote directory
file_name = "photo.jpg"
local_file = open(file_name, 'rb')
ftp.retrbinary('RETR' + file_name, local_file.write, 1024)

ftp.quit()





