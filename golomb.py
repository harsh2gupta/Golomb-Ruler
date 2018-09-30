#do not modify the function names
#You are given L and M as input
#Each of your functions should return the minimum possible L value alongside the marker positions
#Or return -1,[] if no solution exists for the given L

#Your backtracking function implementation

def getGolombLen(markarray):
    i=0
    j = len(markarray) - 1
    first = 0;
    last = 0;
    while(i < len(markarray)):
        if(markarray[i] == 1):
            first = i;
            break;
        i+=1;
    while (j >= 0):
        if (markarray[j] == 1):
            last = j;
            break;
        j -= 1;

    if(last == 0):
        return 0
    else:
        return abs(last - first)

def isUnique(list):
    temp = set()
    for x in list:
        if x in temp: return False
        temp.add(x)
    return True

# # returns a sorted list of diffs between consecutive pairs
# def findDiffs(markarray):
#     difflist = list()
#     i = 0
#     reason = 0
#     while(i < len(markarray)):
#         if(markarray[i] == 1):
#             j = i+1;
#             while(j < len(markarray)):
#                 if(markarray[j] == 1):
#                     diff = abs(j-i)
#                     difflist.append(diff)
#                     i = j
#                     reason = 1
#                     break
#                 j+=1
#
#             if(reason == 1):
#                 reason = 0;
#                 continue;
#         i+=1
#
#     #print "finddiff ",difflist
#     return sorted(difflist)

# returns a sorted list of diffs between consecutive pairs
def findDiffs(markarray):
    difflist = list()
    i = 0
    while(i < len(markarray)):
        if(markarray[i] == 1):
            j = i+1;
            while(j < len(markarray)):
                if(markarray[j] == 1):
                    diff = abs(j-i)
                    if(diff > 0):
                        difflist.append(diff)
                j+=1
        i+=1

    #print "finddiff ",difflist
    return sorted(difflist)

def findDistanceForIndex(index,markarray):
    difflist = list()
    i = index
    j = 0;
    while(j < len(markarray)):
        if(markarray[j] == 1 and (j != i)):
            diff = abs(j-i)
            if(diff > 0):
                difflist.append(diff)
        j+=1

    #print "finddiff ",difflist
    return sorted(difflist)

counter = 0

def backtrack(L,M,curmarks,markarray):
    global counter
    counter+=1
    #print "recursion called for mark: ", curmarks," , arr: ",markarray
    if(L == 0 or M == 0 or curmarks > M):
        return -1,[]

    # check for different distance
    list = findDiffs(markarray)
    if(curmarks == M and isUnique(list)):
        #print "got vals, marks: ",curmarks," , list: ",list," , arr: ",markarray, " , golomb: ",getGolombLen(markarray)
        if(getGolombLen(markarray) == L):
            return len(markarray)-1,markarray
        else:
            return  -1,[]

    if(curmarks == M):
        return -1,[]

    i = 0;
    while(i <= L):
        if(markarray[i] == 0):
            markarray[i] = 1;
            ret = backtrack(L, M, curmarks + 1, markarray)
            if(ret[0] == -1):
                markarray[i] = 0;
                i += 1
                continue
            else:
                return ret
        i+=1

    return -1,[]

def BT(L, M):
    "*** YOUR CODE HERE ***"
    # # create a tuple of values for L, to be passed to recursion
    # # Solution 1 : start from given L and move down
    # length = L
    # prevSolutions = list()
    # lastsoln = -1,[]
    # while(length >= M): # use this loop to reduce length for optimal answer check
    #     markarray = [0]*(length+1)
    #     markarray[0] = 1
    #
    #     #print "sending arr: ",markarray
    #     current = backtrack(length,M,1,markarray)
    #     #print "returned val: ", current," , actual: ",length
    #     if(current[0] == -1):
    #         return lastsoln
    #     elif(current[0] == length):
    #         print "got solution : ", current
    #         prevSolutions.append(current)
    #         lastsoln = current
    #
    #     length-=1
    #
    # return lastsoln

    # Solution 2 : using Robin's heuristic ;) <goes from lowest possible L to higher L>
    length = 0
    prevSolutions = list()
    lastsoln = -1,[]
    mark = M - 1
    while(mark > 0):
        length+= mark
        mark-=1

    print "length: ", length, " , L: ", L
    while(length <= L): # use this loop to reduce length for optimal answer check
        markarray = [0]*(length+1)
        markarray[0] = 1

        print "current arr: ",markarray, " , length: ",length
        current = backtrack(length,M,1,markarray)
        print "returned val: ", current," , actual: ",length
        if(current[0] == length):
            print "got solution : ", current
            prevSolutions.append(current)
            lastsoln = current
            return lastsoln

        length+=1

    return lastsoln

#Your backtracking+Forward checking function implementation
def btwithfc(L,M,curmarks,markarray):
    global counter
    counter += 1
    #print "recursion called for mark: ", curmarks," , arr: ",markarray, " ,L: ",L, " ,M: ",M
    if (L == 0 or M == 0 or curmarks > M):
        return -1, []

    # check for different distance
    difflist = findDiffs(markarray)
    if (curmarks == M and isUnique(difflist)):
        #print "got vals, marks: ", curmarks, " , difflist: ", difflist, " , arr: ", markarray, " , golomb: ", getGolombLen(
        #    markarray)
        if (getGolombLen(markarray) == L):
            return len(markarray) - 1, markarray
        else:
            return -1, []

    if (curmarks == M):
        return -1, []

    i = 0;
    reason = 0
    localmarkarr = list(markarray)
    while (i <= L):
        if (localmarkarr[i] == -1):
            localmarkarr[i] = 1;
            sendarr = list(localmarkarr) # array with 0's populated
            # find distance of this marker from others
            distlist = findDistanceForIndex(i,sendarr)

            # update arr with 0s corresponding to max dist from others

            #print "received dist: ",distlist," ,arr: ",sendarr
            while(len(distlist) > 0):
                #print "arr: ", distlist," ,popped: ",distlist[0]
                l = distlist[0]
                if(i+l >= L):
                    break
                if(sendarr[i+l] == 1):
                    reason = 1
                    break

                sendarr[i+l] = 0
                distlist.pop(0)

            if(reason == 1):
                reason = 0
                localmarkarr[i] = -1
                i+=1
                continue

            #print "sending array: ",sendarr
            ret = btwithfc(L, M, curmarks + 1, sendarr)
            if (ret[0] == -1):
                localmarkarr[i] = -1;
                i += 1
                continue
            else:
                return ret
        i += 1

    return -1, []

def FC(L, M):
    "*** YOUR CODE HERE ***"
    # # create a tuple of values for L, to be passed to recursion
    # # Solution 1 : start from given L and move down
    # length = L
    # prevSolutions = list()
    # lastsoln = -1,[]
    # while(length >= M): # use this loop to reduce length for optimal answer check
    #     markarray = [-1]*(length+1)
    #     markarray[0] = 1
    #
    #     #print "current arr: ",markarray
    #     current = btwithfc(length,M,1,markarray)
    #     #print "returned val: ", current," , actual: ",length
    #     if(current[0] == -1):
    #         return lastsoln
    #     elif(current[0] == length):
    #         print "got solution : ", current
    #         prevSolutions.append(current)
    #         lastsoln = current
    #
    #     length-=1
    #
    # return lastsoln

    # Solution 2 : using Robin's heuristic ;) <goes from lowest possible L to higher L>
    length = 0
    prevSolutions = list()
    lastsoln = -1,[]
    mark = M - 1 # calculating this length because 1st and last mark dist will usually include other marks
    while(mark > 0):
        length+= mark
        mark-=1

    #print "length: ", length, " , L: ", L
    while(length <= L): # use this loop to reduce length for optimal answer check
        markarray = [-1]*(length+1)
        markarray[0] = 1

        print "current arr: ",markarray, " , length: ",length
        current = btwithfc(length,M,1,markarray)
        print "returned val: ", current," , actual: ",length
        if(current[0] == length):
            print "got solution : ", current
            prevSolutions.append(current)
            lastsoln = current
            return lastsoln

        length+=1

    return lastsoln

#Bonus: backtracking + constraint propagation

def btwithcp(L,M,curmarks,markarray):
    global counter
    counter += 1
    #print "recursion called for mark: ", curmarks," , arr: ",markarray, " ,L: ",L, " ,M: ",M
    if (L == 0 or M == 0 or curmarks > M):
        return -1, []

    # check for different distance
    difflist = findDiffs(markarray)
    if (curmarks == M and isUnique(difflist)):
        #print "got vals, marks: ", curmarks, " , difflist: ", difflist, " , arr: ", markarray, " , golomb: ", getGolombLen(
        #    markarray)
        if (getGolombLen(markarray) == L):
            return len(markarray) - 1, markarray
        else:
            return -1, []

    if (curmarks == M):
        return -1, []

    i = 0;
    reason = 0
    localmarkarr = list(markarray)
    while (i <= L):
        if (localmarkarr[i] == -1):
            localmarkarr[i] = 1;
            sendarr = list(localmarkarr) # array with 0's populated
            # find distance of this marker from others
            distlist = findDistanceForIndex(i,sendarr)

            # update arr with 0s corresponding to max dist from others

            #print "received dist: ",distlist," ,arr: ",sendarr
            while(len(distlist) > 0):
                #print "arr: ", distlist," ,popped: ",distlist[0]
                l = distlist[0]
                if(i+l >= L):
                    break
                if(sendarr[i+l] == 1):
                    reason = 1
                    break

                sendarr[i+l] = 0
                distlist.pop(0)

            if(reason == 1):
                reason = 0
                localmarkarr[i] = -1
                i+=1
                continue

         #   print "sending array: ",sendarr
            ret = btwithfc(L, M, curmarks + 1, sendarr)
            if (ret[0] == -1):
                localmarkarr[i] = -1;
                i += 1
                continue
            else:
                return ret
        i += 1

    return -1, []

def CP(L, M):
    "*** YOUR CODE HERE ***"
    # create a tuple of values for L, to be passed to recursion
    # Solution 1 : start from given L and move down
    length = L
    prevSolutions = list()
    lastsoln = -1,[]
    while(length >= M): # use this loop to reduce length for optimal answer check
        markarray = [-1]*(length+1)
        markarray[0] = 1

      #  print "current arr: ",markarray
        current = btwithfc(length,M,1,markarray)
      #  print "returned val: ", current," , actual: ",length
        if(current[0] == -1):
            return lastsoln
        elif(current[0] == length):
            print "got solution : ", current
            prevSolutions.append(current)
            lastsoln = current

        length-=1

    return lastsoln

def main():
    ret = BT(0,1)
    print "exiting main, final sol: ", ret, " ,counter= ",counter

if __name__ == "__main__":
    main()