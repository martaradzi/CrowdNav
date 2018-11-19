import csv

if __name__ == "__main__":

    for i in range(600):
        with open('./data/agent_' + str(i) + '.plans', 'r') as mycsvfile:

            reader = csv.reader(mycsvfile, dialect='excel')

            for row in reader:
                j = 0
                for s in row:

                    if ":" not in s and float(s)<0:
                        print "Negative value " + s + " at point " + str(j)

                    # print str(j) + ": " +  s
                    j += 1

                i += 1
