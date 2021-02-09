import csv

with open("../Characterization/xor2_1xCharacterisation Results.csv", 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow([ '','1.2','2.3','3.4','4.5'])
    writer.writerow([ '','adf','2sdf','3.4','4.5'])
    f.close()

##import csv
##with open('eggs.csv', 'w', newline='') as csvfile:
##    spamwriter = csv.writer(csvfile, delimiter=' ',
##                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
##    spamwriter.writerow(['Spam'] * 5 + ['Baked Beans'])
##    spamwriter.writerow(['Spam', 'Lovely Spam', 'Wonderful Spam'])
    
