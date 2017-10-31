#after making changes here, delete the compiled Python file which goes by the same name, otherwise the changes won't work.
import string
from __main__ import teachers, same_name_teachers, proxy_teachers, proxyFormat, printProxies, make_tod_sched, claMoni,\
     days, today, removed_proxies, comp_proxies, s_proxies, proxies, gen_proxies, custom_proxies, possible_positions,\
     pres_teachers, free_teachers, pres_session, outshell
'''Indices defined here'''
def find_indices(ele, list):
    locations = []
    for i in range(len(list)):
        if list[i] == ele:
            locations.append(i)
    return locations

def suggest_proxies(abs_teachers, pres_teachers, s_proxies):
                                               #actually, a lot of proxies can be suggested.
    for abs_teacher in abs_teachers:
        abs_teacher.saved_assignments = {}
        for i in range(8):
            abs_teacher.saved_assignments[i] = abs_teacher.assigned[i]
            if abs_teacher.assigned[i]:
                abs_teacher.assigned[i] = False
    for pres_teacher in pres_teachers:
        pres_teacher.saved_assignments = {}
        for i in range(8):
            pres_teacher.saved_assignments[i] = pres_teacher.assigned[i]
            if pres_teacher.assigned[i]:
                pres_teacher.assigned[i] = False

    for abs_teacher in abs_teachers:
        
        abs_teacher_today_sched = abs_teacher.today_sched[:]
        for pres_teacher in pres_teachers:
            free_sessions = find_indices("f", pres_teacher.today_sched)
            if free_sessions:
                pres_teacher_today_sched = pres_teacher.today_sched[:]
                for fs in free_sessions: #fs for free session
                    aP = abs_teacher_today_sched[fs] # aP for absent teacher's position
                    if aP != 'f':
                        newP = aP #newP for new position
                        proxy = [pres_teacher, abs_teacher, newP, fs]
                        s_proxies.append(proxy)
                        if not abs_teacher.assigned[fs] and not pres_teacher.assigned[fs]: #fs not abs_teacher.assigned[fs]
                                                      #is done to check whether the
                                                      #proxy for a particular session for an absent
                                                      #teacher has already been assigned or not
                                                      #similar is the stuff for pres_teachers
                            comp_proxies.append(proxy)
                            pres_teacher.assigned[fs] = newP
                            abs_teacher.assigned[fs] = pres_teacher

    for abs_teacher in abs_teachers:
        abs_teacher.assigned = abs_teacher.saved_assignments
    for pres_teacher in pres_teachers:
        pres_teacher.assigned = pres_teacher.saved_assignments

def assign_proxy(proxy):
    pres_teacher = proxy[0]
    abs_teacher = proxy[1]
    newP = proxy[2]
    fs = proxy[3]

    proxies.append(proxy)
    if proxy in s_proxies:
        gen_proxies.append(proxy)
    
    pres_teacher.today_sched[fs] = newP
    pres_teacher.proxies.append(proxy)
    abs_teacher.proxies.append(proxy)
    for p in [pres_teacher.proxies, abs_teacher.proxies]:
        proxySort(p)
    if not pres_teacher in proxy_teachers:
        proxy_teachers.append(pres_teacher)
    pres_teacher.assigned[fs] = newP
    abs_teacher.assigned[fs] = pres_teacher
    make_tod_sched(pres_teacher)#updates the stuff to be displayed
    pres_teacher.update_status()#same thing here

def proxy_assignment():
    global outshell #has a very little purpose
    L = len(s_proxies)
    if L == 0:
        print "There aren't any suggestions today!"
        if len(pres_teachers) == len(teachers):
            print "Everyone is present today."
        return
    if L == 1:
        print "Suggested proxy:"
        printProxies(s_proxies)
        choice = raw_input("\nType 'a' to assign the above proxy, anything else to quit: ")
        if choice.lower() == 'a':
            if s_proxies[0] not in proxies:
                assign_proxy(s_proxies[0])
                print '\nProxy assigned.'
            else:
                print 'This proxy has already been assigned.'
            return
    
    print "Suggested proxies:"
    printProxies(s_proxies)
    err = 1
    print "\nTo exit, type 'quit'."
    while err:
        choice = raw_input("\nHow many proxies do you want to assign (single/multiple/auto assign)? ")
        choice = choice.lower()
        if choice == 'quit':
            return
        if choice == 'single':
            try:
                num = raw_input("Which one? ")
                if num.lower() == 'quit':
                    return
                num = eval(num)
                p = s_proxies[num-1] #num-1 is the required index; num represents the position for humans.
                print
                print proxyFormat(p)
                
                if p not in proxies:
                    ops = []
                    c = 1
                    for i in range(len(proxies)):
                        proxy = proxies[i]
                        if (proxy[0], proxy[3]) == (p[0], p[3]) or (proxy[1], proxy[3]) == (p[1], p[3]):
                            ops.append(proxy)
                            c = 0
                    if c:
                        assign_proxy(p)
                        print '\nProxy assigned.'
                    else:
                        override(ops, p, 'single')
                else:
                    print "This proxy has already been assigned."
                err = 0
            except:
                pass
        elif choice == 'multiple': #should the chosen proxies be displayed for 'surity'?
                msg = "Please enter a valid input."
                try:
                    inp = raw_input("Which ones? Separate the numbers by commas: ")
                    nums = eval('['+ inp+']')
                except:
                    print msg
                    continue
                for ele in nums:
                    if type(ele) != int:
                        nums.remove(ele)
                if nums == []:
                    print msg
                    continue
                for n in range(len(nums)):
                    c = 1
                    for i in range(len(nums)):
                        if i != n and nums[i] == nums[n]:
                            c = 0
                            break
                    num = nums[n]
                    if not (1 <= num <= len(s_proxies)) or c == 0:
                        break
                else:
                    spn = [] #simultaneous proxies' numbers
                    c = 1
                    for num in nums:
                        p = s_proxies[num-1]
                        if c == 0: #as soon as simultaneous proxies are found, the loop is exited.
                            break
                        for i in nums:
                            if i != num:
                                proxy = s_proxies[i-1]
                                if (proxy[0], proxy[3]) == (p[0], p[3]) or (proxy[1], proxy[3]) == (p[1], p[3]):
                                    spn.append(i-1+1) #added one so that it displays in human language
                                    c = 0
                        if c == 0:
                            spn.insert(0, num-1+1)#same here
                        if spn:
                            msg = neaten(spn)
                            print '\nProxies %s cannot be assigned simultaneously!' % msg
                    if c == 1:
                        count = 0
                        assigned_nums = []
                        for num in nums:
                            p = s_proxies[num-1]
                            if p not in proxies:
                                ops = []
                                existing_proxies = proxies[:]
                                cond = 1
                                for proxy in existing_proxies:
                                    if (proxy[0], proxy[3]) == (p[0], p[3]) or (proxy[1], proxy[3]) == (p[1], p[3]):
                                        ops.append(proxy)
                                        cond = 0
                                if cond:
                                    assign_proxy(p)
                                    count += 1
                                override(ops, p, 'multiple')
                            else:
                                assigned_nums.append(num)

                        if assigned_nums != []:
                            msg = neaten(assigned_nums)
                            if len(assigned_nums) == 1:
                                word = '\nProxy'
                                w2 = 'is'
                            else:
                                word = '\nProxies'
                                w2 = 'are'
                            print word, msg, w2, 'already assigned.'
                
                        if count != 0:
                            if count == 1:
                                word = 'Proxy'
                            else:
                                word = 'Proxies'
                            if len(assigned_nums) == 0 and len(ops) == 0:
                                w2 = ''
                            else:
                                w2 = 'Other '
                                word = word.lower()
                            print '\n%s%s assigned.' % (w2, word)
                        err = 0
        elif choice == 'auto assign':
            if outshell:
                w = ''
                outshell = False
            else:
                w = 'New '
            if comp_proxies == proxies:
                print "All auto proxies have already been assigned."
                return
            while len(proxies) != 0:
                removeProxy(proxies, 0)

            for proxy in comp_proxies:
                if proxy in removed_proxies:
                    removed_proxies.remove(proxy)
                assign_proxy(proxy)
            if len(comp_proxies) == 1:
                word = 'Proxy'
            else:
                word = 'Proxies'
            print '\n%s assigned.' % word
            proxySort(proxies)
            print "\n%s%s:" % (w, word)
            printProxies(proxies)
            err = 0
        if err:
            print "Please enter a valid input."

def override(ops, p, mode):
    count = 0
    if len(ops) == 0:
        return
    else:
        if len(ops) == 1:
            word = 'proxy'
        else:
            word = 'proxies'
        if mode == 'single':
            msg = "\nThis will override the following existing %s:" % word
        else:
            msg = "\nProxy %i will override the following existing %s:" % (s_proxies.index(p)+1, word)
        print msg
        printProxies(ops)
        prompt = "\nType 'o' to override the %s, anything else to quit: " % word
        ch = raw_input(prompt)
        if ch.lower() == 'o':
            for proxy in ops:
                i = proxies.index(proxy)
                removeProxy(proxies, i)
            assign_proxy(p)
            print "%s overriden." % word.capitalize()

def neaten(list):
    msg = ''
    for n in list:
        msg += str(n) + ', '
    msg = msg.strip(', ')
    return msg

def custom_removal():
    if len(proxies) == 0:
        print "There's no proxy to remove!"
    elif len(proxies) == 1:
        print
        print proxyFormat(proxies[0])
        choice = raw_input("\nType 'r' to remove the above proxy, anything else to quit: ")
        if choice.lower() != 'r':
            return
        removeProxy(proxies, 0)
        print '\nProxy removed.'
                
    else:
        print "Today's proxies:\n"
        printProxies(proxies)
        print "\nTo quit from anywhere, just type 'quit'."
        msg = "Please enter a valid input."
        ch = raw_input('How many proxies do you want to remove (single/multiple/all)? ')
        ch = ch.lower()
        if ch == 'single':
            while 1:
                p_index = raw_input('\nWhich proxy do you want to remove? ') #p_index for proxy index
                if p_index.lower() == 'quit':
                    return
                p_index = eval(p_index)
                if type(p_index) != int:
                    print msg
                elif not (0 <= p_index <= len(proxies)):
                    print msg
                else:
                    print proxyFormat(proxies[p_index-1])
                    choice = raw_input("\nType 'r' to remove the above proxy, anything else to quit: ")
                    if choice.lower() != 'r':
                        return
                    removeProxy(proxies, p_index-1)
                    print '\nProxy removed.'
                    return
        elif ch == 'multiple':
            while 1:
                try:
                    inp = raw_input("\nWhich ones? Separate the numbers by commas: ")
                    if inp.lower() == 'quit':
                        return
                    nums = eval('['+ inp+']')
                except:
                    print msg
                for ele in nums:
                    if type(ele) != int:
                        nums.remove(ele)
                if len(nums) == 0:
                    print msg
                else:
                    for n in range(len(nums)):
                        c = 1
                        for i in range(len(nums)):
                            if i != n and nums[i] == nums[n]:
                                c = 0
                                break
                            num = nums[n]
                        if not (1 <= num <= len(s_proxies)) or c == 0:
                            print msg
                            break
                    else:
                        nums.sort()
                        if len(nums) == 1:
                            word = 'Proxy'
                        else:
                            word = 'Proxies'
                        j = 0
                        while j < len(nums):
                            index = nums[j] - 1
                            removeProxy(proxies, index)
                            for k in range(j+1, len(nums)):
                                nums[k] -= 1
                            j += 1
                        print "\n%s removed." % word
                        return
        elif ch == 'all':
            while proxies != []:
                removeProxy(proxies, 0)
            print '\nAll proxies removed.'
      
def removeProxy(proxies, i): #having proxies as a non-argument wasn't working
    #probably we need to modify 'assigned' attribute here
    proxy = proxies[i]
    T1 = proxy[0] #the one who takes the proxy
    T1.today_sched[proxy[3]] = 'f' #makes T1 free instead of assigning her/him to the original position. It is possible
                                   #that someone has a proxy at the orginal position
    T1.assigned[proxy[3]] = False
    make_tod_sched(T1)#updates the stuff to be displayed.
    T1.update_status() #same here
    T2 = proxy[1]
    T2.assigned[proxy[3]] = False
    T1.update_status()
    make_tod_sched(T1)#updates the stuff to be displayed

    for list in [proxies, T1.proxies, T2.proxies]:
        list.remove(proxy)
    
    if proxy in gen_proxies:
        gen_proxies.remove(proxy)
    else:
        custom_proxies.remove(proxy)
    #following block may be made more efficient
    #following for-else block checks whether T1 is still a proxy-taking teacher, if not, T1 is removed from the list.
    for j in range(len(proxies)):
        if T1 == proxies[j][0]:
            break
    else:
        proxy_teachers.remove(T1)
    if not proxy in removed_proxies:
        removed_proxies.append(proxy)

def getClaMoni(abs_teachers, proxies): #WHAT IS THE ORDER OF DISPLAY OF claMoni?
    #may be made more efficient
    #add code for the consequences of custom added proxies
    for abs_teacher in abs_teachers:
        for i in range(len(abs_teacher.today_sched)):
            grade = abs_teacher.today_sched[i]
            if grade != 'f': #although f can never be a 'grade'!
                sessions = find_indices(grade, abs_teacher.today_sched)
                if grade not in claMoni:
                    claMoni[grade] = sessions
                else:
                    for session in sessions:
                        if session not in claMoni[grade]:
                            claMoni[grade].append(session)

    for proxy in proxies:
        if proxy[2] in claMoni:
            if proxy[3] in claMoni[proxy[2]]:
                claMoni[proxy[2]].remove(proxy[3])
    claCopy = {}
    for key in claMoni:
        claCopy[key] = claMoni[key]
    for item in claCopy:
        if claCopy[item] == []:
            del claMoni[item]

def proxySort(proxies): #by default, it sorts proxies in the chronological order. Enhance sorting flexibility if possible
    #use more efficient sorting techniques, if there are any
    #Proxies is an alternate for proxies
    sProxies = [] #list of sorted proxies
    s = [] #list of sessions
    n = len(proxies)
    for p in range(n):
        s.append(proxies[p][3])
    s.sort()
    for p in range(n):
        session = s[p]
        k = 0
        while k < len(proxies): #a simple for loop didn't work
            if proxies[k][3] == session:
                sProxies.append(proxies.pop(k))
                #break should not be placed here, as it is possible for multiple proxies to have the same session
            k += 1
    #proxies = sProxies[:] - this doesn't work
    for i in range(n):
        proxies.append(sProxies[i])
    del sProxies

def teacherSeek(grade, session): #grade here means class, or some other room
    #class timetable would probably be more efficient here.
    #add proxy tag when the result (teacher) is a substitute in the input class (grade).
    from __main__ import pres_session #let this be here, for now.
    if session != 'recess':
        try:
            session = int(session)
        except:
            return
    if grade in possible_positions:
        if session == 'recess':
            sessi = 4
        else:
            sessi = session
        if sessi < 5:
            ses = sessi - 1
        else:
            ses = sessi

        if ses == pres_session:
            word = 'presently'
            w = 's'
        else:
            if ses < pres_session:
                w = 'd'
            else:
                w = 's'
            word = 'during session %s' % session

        msg = 'No teacher.'
        add_msg = ' Class %s require%s monitoring %s.' % (grade.upper(), w, word) #(optional) print the name of the expected teacher. add_msg for additional msg
        msg_list = [] #list of concerned teachers
        if session != 'recess':
            if session in range(1, 9):
                for i in range(len(pres_teachers)):
                    teacher = pres_teachers[i]
                    if teacher.today_sched[session-1] != 'f':
                        if teacher.today_sched[session-1] == grade:
                            msg_list.append(teacher)
                            for proxy in proxies: #if the seeked teacher is on a proxy in the grade during this session.
                                if proxy[0] == teacher and proxy[2] == grade and proxy[3] == session-1:
                                    msg_list.extend(['proxy', proxy[1]])
                            return msg_list
                    else: #this block is executed after the above block so that, if there is some teacher assigned to the
                         #free_pos, (say 6A), her/his name would be returned.
                        if teacher.free_pos == grade:
                            msg_list.append(teacher) #there may be other teachers present there, so return is not used here.
                if msg_list != []:
                    return msg_list
                else:
                    if grade in claMoni.keys():
                        if (session-1) in claMoni[grade]:
                            msg += add_msg
                    return msg #really appropriate here? Try to have a different msg for places like staff room.
        else: #when session is recess.
            for i in range(len(pres_teachers)):
                teacher = pres_teachers[i]
                if teacher.recess_pos.lower() == grade:
                    msg_list.append(teacher)
            if msg_list != []:
                return msg_list
            else:
                return msg #classes usually don't prefer monitoring over them during recess, so msg isn't returned here.

def find_free_teachers(session):
    try:
        session = int(session)
    except ValueError:
        return
    if not (1 <= session <= 8):
        return
    msg_list = []
    for teacher in pres_teachers:
        if teacher.today_sched[session-1] == 'f':
            msg_list.append(teacher)
    if msg_list == []:
        return 'No teacher.'
    return msg_list
