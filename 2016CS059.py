import itertools

class Queue:
    
    def __init__(self):
        self.items=[]

    def enqueue(self,item):
        self.items.extend(item)

    def dequeue(self):
        return self.items.pop(0)

    def isEmpty(self):
        return len(self.items)==0
    
    def rev(self):
        self.items=self.items[::-1]

#All combinations are made nodes inorder to store their separate counts
class greaterCombi:
    
    def __init__(self,data):
        self.value=data
        self.count=0

#All calculations relating to obtaining the PTS is done in the PTS class
class PTSS:
    
    def __init__(self):
        self.trustset=[] #Contains elements of PTS
        self.TV=[] #Contains A->B type formulas 
        self.allMs=[] #Contains all combinations whose count is greater than M

#if a particular combination is a subset of any combination currently in the PTS, return the
#highest count of the superset
    def existsinPTS(self,combination):
        v=0
        for element in self.trustset:
            if set(combination.value).issubset(set(element.value)):
                if element.count>v:
                    v=element.count
        return v

    def addtoPTS(self,item):
        self.trustset.append(item)
        
#Returns the probable trust set        
    def derivePTS(self,mQueue):
        while not mQueue.isEmpty():
            e=mQueue.dequeue()
            val=self.existsinPTS(e)
            if len(e.value)>1:
                if val>0:
                    if e.count>val:
                        self.addtoPTS(e)
                else:
                    self.addtoPTS(e)
        return self.trustset

#Returns the number of occurances of an element
    def getM(self,element):
        for i in self.allMs:
            if i.value==element:
                return i.count
        return 0

#Returns the A->B type formulas whose Trust Value is greater than T
    def getTrustValue(self):
        for element in self.trustset:
            LHS=[] 
            for e in range(1,len(element.value)):
                combination=list(itertools.combinations(element.value,e))
                for each in combination:
                    if set(each).isdisjoint(set(LHS)):
                        if len(each)==1:
                            cur=''.join(each)
                        else:
                            cur=each
                        val=probableSet.getM(cur)
                        if val>0:
                            if element.count/val>=T:
                                LHS.append(cur)
                                self.TV.append(','.join(cur)+'->'+','.join(set(element.value)-set(each)))
        return self.TV
    
#All integers are nodes of the Employee class   
class Employee:
    
    def __init__(self,data):
        self.ID=data
        self.count=0
        self.next=None      #Using a doubly linked list to make searching efficient
        self.previous=None
        self.adjacent=[]

class employeeListItems:
    
    def __init__(self):
        self.head=None
        self.tail=None

    def addEmployee(self,data):
        newEmp=Employee(data)
        if self.head is None:
            self.head=newEmp
        else:
            newEmp.previous=self.tail
            self.tail.next=newEmp
        self.tail=newEmp

    def prin(self):
        cur=self.head
        while cur is not None:
            print(cur.ID,'-',cur.adjacent)
            cur=cur.next
        print()

    def prin1(self):
        cur=self.head
        while cur is not None:
            for e in cur.adjacent:
                print(cur.ID,'-',[a.ID for a in e])
            cur=cur.next

#Given a list of integers along with a reference point, returns the particular objects(employees)
def returnEmpObjList(empList,empNodes,N):
    empObjList=[]
    cur=empNodes
    for e in empList:
        if int(e)>N:
            print('Contains invalid number. Please re-enter.')
            empObjList=[]
            break
        while cur.ID!=e:            #Traverses a doubly linked list to make searching efficient
            if int(e)<int(cur.ID):
                cur=cur.previous
            else:
                cur=cur.next
        cur.count+=1
        empObjList.append(cur)
    return [empObjList,empNodes]

#Returns a list of the employees whose count is greater than M
def returneligibleList(eList):
    cur=eList.head
    emp=[]
    while cur is not None:
        if cur.count>=M:
            emp.append(cur.ID)
        cur=cur.next
    return emp

#Given a combination, returns its number of occurances
def isEligible(combination,graph):
    c=0
    end=combination[0]
    cur=graph.head
    [objs,cur]=returnEmpObjList(list(combination),cur,N)
    initial=graph.head
    while int(initial.ID)<=int(end):
        for element in initial.adjacent:
            if set(objs).issubset(set(element)):
                c+=1
        initial=initial.next
    return c

def populatecomb(combgreaterM,jobGraph,M):
    cur=jobGraph.head
    while cur is not None:
        o=cur.ID
        c=cur.count
        if c>=M:
            ob=greaterCombi(o)
            ob.count=c
            combgreaterM.enqueue([ob])
        cur=cur.next

def selectEligibleCombi(allCombinations,combgreaterM,jobGraph,M):
    while not allCombinations.isEmpty():
        i=allCombinations.dequeue()
        c=isEligible(i,jobGraph)
        if c>=M:
            o=greaterCombi(i)
            o.count=c
            combgreaterM.enqueue([o])

    
        
N=int(input("Enter the number of employees: "))  
jobGraph=employeeListItems()
    
for e in range(1,N+1):  #Populate the graph with employees
    jobGraph.addEmployee(str(e))
cur_node=jobGraph.head
    
line=input("Enter the job list or press enter to end:\n")
while line!='':
    line=sorted(line.split(','))
    [line,cur_node]=returnEmpObjList(line,cur_node,N)
    if len(line)>0:
        line[0].adjacent.append(line)
    line=input()
#jobGraph.prin() #Outputs a visual representation of the jobGraph

M=int(input("Enter eligibility value M: "))
T=int(input("Enter trust threshold value T: ")[:-1])/100

empList=returneligibleList(jobGraph)
combgreaterM=Queue()
populatecomb(combgreaterM,jobGraph,M)

#Populate all the combinations into a queue
allCombinations=Queue()
for i in range (2,len(empList)+1):
    allCombinations.enqueue(list(itertools.combinations(empList,i)))
    
#print(allCombinations.items)

selectEligibleCombi(allCombinations,combgreaterM,jobGraph,M)
wholeSet=combgreaterM.items
##print([(i.value,i.count) for i in wholeSet])
combgreaterM.rev()

#Deriving the PTS
probableSet=PTSS()
PTS=probableSet.derivePTS(combgreaterM)
probableSet.allMs=wholeSet

##Print combgreaterM
##print([(i.value,i.count) for i in combgreaterM.items])
##Print PTS
##print([(i.value,i.count) for i in probableSet.derivePTS(combgreaterM)])

finalPTS=probableSet.getTrustValue()
for i in finalPTS:
    print(i)





