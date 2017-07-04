#Time Table Manager
#deploy proxies
#is it better to have a proxy as an object?
#handle end_time
#neat proxies display -- in tabular form
#the really cool 'dive into' feature - which allows user to go to a particular day in history to see exactly, for
#example, which teacher was assigned proxy in, say, 6a during the 5th session of October 28, 2005. The user can also
#go to a future day to plan that day-assign proxies beforehand if s/he knows that a teacher would be absent on that day,
#etc.
#rename history pickle files with a .his extension or .past extension.
#write code to access history of a particular teacher.
#add numerals for present teachers, absent teachers, classes which require monitoring, etc.
#display proxies in a tabular form, if there are lots of them.
#if status is desired, also print the subject, e.g; "She is most probably in class 6B, teaching math."
#it may be worthwhile to create a class for classes (i.e, grades).

import datetime, string, pickle, os, random #random has a very little purpose here.
print "\t\t\tTIME TABLE MANAGER"
print " This program manipulates proxies and monitors school activity.\n\n"
class Teacher():
    def __init__(self, f_name, l_name, classes, subjects, schedule,\
                 free_pos = "staff room", recess_pos = "staff room", gender = "female", is_present=False): #include title
        self.first_name = f_name.capitalize()
        self.title_name = self.first_name #only for teachers having distinct names. For those who have same names,
                                          #modification is done later.
        self.last_name = l_name.capitalize()
        self.name = self.first_name + " " + self.last_name
        self.classes = sorted(classes) #try to deduce this from sched, and '12' < '9'! (Try that operation in the shell!)
        self.subjects = sorted(subjects)
        self.is_present = is_present
        self.schedule = schedule #list of lists, containing daily schedules
        self.free_pos = free_pos
        self.recess_pos = recess_pos
        self.gender = gender
        self.today_sched = self.schedule[datetime.datetime.weekday(datetime.datetime.now().date())] #probably we don't need this anymore
        self.history = {} #a dictionary (initially empty) containing teacher's stats
        self.proxies = []#list of proxies assigned to, or in place of, the teacher.

        self.sched = "Note: 'f' stands for free session and 'r' stands for recess.\n\n" #get this formatted and create a modifier for the process, it's more natural than a method
        self.sched += make_sched(self.schedule)

        if self.gender == "female": #say 'Don't you know even that?' when asked for
            self.status = "She"
        else:
            self.status = "He"
        self.assigned = {} #will be useful when the teacher is absent
        #kind of polymorphism for pres and abs_teachers
        for s in range(8):
            self.assigned[s] = False

    def update_status(self): #updates status
        if not self.is_present:
            return
        self.today_sched.insert(4, 'r')
        time_passed = int((datetime.datetime.now() - start).seconds)#consider recess' approximation here
        self.pres_pos = self.today_sched[(time_passed / (30 * 60))]
        if self.gender == "female":
                self.status = "She"
        else:
                self.status = "He"
        self.status += " is most probably "
        if self.pres_pos == "r":
                self.status += "near %s." % self.recess_pos
        elif self.pres_pos == "f":
                self.status += "near %s." % self.free_pos
        else:
                self.status += "in class %s" % (self.pres_pos.upper())
                for proxy in proxies:
                    if proxy[2] == self.pres_pos and proxy[3] == session:
                        self.status += " (in place of %s)" % proxy[1].title_name
                        break
                self.status += "."
        self.today_sched.remove('r')

    def __str__(self):
        if len(self.classes) > 1:
            class_n = "classes "
        else:
            class_n = "class "
        msg = self.name + " is a teacher of " + class_n
        for grade in self.classes:
            msg += str(grade) + ", "
        msg = msg.strip(", ")
        if len(self.classes) > 1:
            msg_l = []
            for i in msg:
                msg_l.append(i)
            #check the following
            msg_l.insert((len(msg) - len(str(self.classes[len(self.classes) - 1]))), "and ")
            del msg_l[(len(msg_l) - len(str(self.classes[len(self.classes) - 1])) - 3)]
            #till here
            msg = ""
            for j in msg_l:
                msg += j

        msg += " who teaches "
        for subject in self.subjects:
            msg += subject + ", "
        msg = msg.strip(", ") + "."
        if len(self.subjects) > 1:
            msg_l = []
            for i in msg:
                msg_l.append(i)
            msg_l.insert((len(msg) - len(self.subjects[len(self.subjects) - 1]) - 1), "and ")
            del msg_l[(len(msg_l) - len(self.subjects[len(self.subjects) - 1]) - 4)]
            msg = ""
            for j in msg_l:
                msg += j
        return msg

class Stats:
    def __init__(self, teachers, abs_teachers, pres_teachers, proxy_teachers, comp_proxies, s_proxies, proxies, gen_proxies, custom_proxies,\
                 removed_proxies, clamoni):
        self.teachers = teachers
        self.abs_teachers = abs_teachers
        self.pres_teachers = pres_teachers
        self.proxy_teachers = proxy_teachers
        self.comp_proxies = comp_proxies
        self.s_proxies = s_proxies
        self.proxies = proxies
        self.gen_proxies = gen_proxies
        self.custom_proxies = custom_proxies
        self.removed_proxies = removed_proxies
        self.clamoni = clamoni

def proxyFormat(proxy):
    msg = proxy[0].title_name + "'s proxy (in place of " + proxy[1].title_name + ") in class " + str(proxy[2])\
          +" during session " + str(proxy[3]+1) + '.'
    return msg

def  printProxies(proxies):
    if len(proxies) == 1:
        msg = '\n' + proxyFormat(proxies[0])
    else:
        msg = ''
        num = 1
        for proxy in proxies:
            msg += "\n" + str(num) + ". " + proxyFormat(proxy)
            num += 1
    print msg

def welcome(): #welcomes the teacher to ABPS.
    print "Welcome to The Aditya Birla Public School.\n"
    print  "Please enter your information carefully. If you want to quit from anywhere, just type 'quit'."
    print "Also, if you don't want to enter optional information, just hit enter."
    prompts = ["What's your first name? ", "What's your last name? ", "To which classes would you teach? (separate the classes by commas) ",\
              "Which subjects would you teach? (again, separate them by commas) ", "What is your gender? ", \
               "Where would you be during your free sessions? Default place is staff room. ",\
               "Where would you be during recess? Default place is staff room. "]
    inputs = []
    global response
    response = "We don't have such a place in our school. Please retype."
    L = len(prompts)
    i = 0
    while i < L:
        err = 0
        ans = raw_input('\n' + prompts[i])
        ans = ans.lower()
        if ans == 'quit':
            return

        elif 0 <= i <= 1:
            if ans == '':
                print "Please enter a valid name."
                err = 1
            for char in ans:
                if char not in string.letters+'.':
                    print "Please type your name correctly."
                    err = 1
                    break
        elif 2 <= i <=3:
            if i == 3:
                if ans == '':
                    print "Please enter something."
                    err = 1

            ans = ans.split(',')
            if i == 2:
                for ele in ans:
                    if ele not in [str(j) for j in range(1, 13)]:
                        print "Please enter valid classes. Do not enter sections."
                        err = 1
                        break
        elif i == 4:
            if ans not in ['male', 'female', 'other']:
                print "Please type your gender correctly."
                continue
        elif 5 <= i <= 6:
            if ans == '':
                ans = 'staff room'
            elif ans.lower() not in possible_positions:
                print response
                continue

        if err:
            continue
        else:
            print random.choice(['Great', 'Nice']) + '!'
            inputs.append(ans)
        i += 1

    f_name = inputs[0].capitalize()
    l_name = inputs[1].capitalize()
    classes = inputs[2]
    subjects = inputs[3]
    gender = inputs[4]
    free_pos = inputs[5] #if a class is entered, we assume that s/he would be present near this class during free time
    recess_pos = inputs[6] #same here
    schedule = input_schedule()
    if schedule:
        while 1:
            print "\nPlease check that the below schedule is your correct schedule ('r' stands for recess).\n"
            print make_sched(schedule)
            c = raw_input("\nType 're' to re-enter your schedule, or anything else to continue: ")
            c = c.lower()
            if c == 're':
                schedule = input_schedule()
            else:
                break
        teacher = Teacher(f_name, l_name, classes, subjects, schedule, free_pos, recess_pos, gender, True)
        teacher.is_present = True
        teacher.sched = make_sched(schedule)
        make_tod_sched(teacher)
        teacher.update_status()
        pres_teachers.append(teacher)
        teachers.append(teacher)
        file_name = teacher.name + '.pkl' #assuming this serves as a unique identifier. Otherwise assign roll numbers.
        file_name = 'Teachers/' + file_name
        t_file = open(file_name, 'wb+')
        pickle.dump(teacher, t_file)
        t_file.close()
        n = open('Names.pkl', 'rb')
        names = pickle.load(n)
        n.close()
        names.append(teacher.name)
        n = open('Names.pkl', 'wb')
        pickle.dump(names, n)
        n.close()
        print "\nThat's it! Welcome to the ABPS family!"
        return 1

def input_schedule(): #check for already-assigned stuff, add repeated checks so that input isn't tedious in case of mistakes
    print "\nNow, input your schedule carefully. To exit from anywhere, just type 'quit'."
    print "Type 'f' for free sessions."
    schedule = []
    for i in range(6):
        print '\n' + days[i] + ':'
        day_sched = []
        j = 0
        while j <= 7:
            prompt = "Session %i: " % (j+1) #i in %i is a format character, not the loop variable
            s = raw_input(prompt)
            s = s.lower()
            if s == 'quit':
                return
            elif s == 'f' or s in possible_positions:
                if s != 'f':
                    cond = 1 #condition that this place is not already occupied.
                    for k in range(len(teachers)):
                        teacher = teachers[k]
                        if teacher.schedule[i][j] == s:
                            print "But one of our teachers (%s) is already assigned to class %s during session %i. Please retry." %(teacher.name, s, j+1)
                            cond = 0
                            break
                    if not cond:
                        continue
                day_sched.append(s)
            else:
                print response
                continue
            j +=1
        schedule.append(day_sched)
    return schedule

def make_sched(schedule): #make this better, and add the music sign here as well (it conveys the current session).
    sched = '%-9s: ' % 'Session'
    for i in range(1, 9):
        sched += '%i\t' % i
        if i == 4:
            sched += 'r\t'
    sched += '\n'
    sched += '_' * 80
    sched += '\n\n'
    for d in schedule:
            d.insert(4, 'r')
            day = days[schedule.index(d)]
            sched += '%-9s: ' % day
            for c in d:
                if c not in ['r', 'f']:
                    s = c.upper()
                else:
                    s = c
                sched += '%s\t' % s

            if today == day:
                sched = sched.strip('\t')
                sched += '   <- today'
            sched += '\n'
            d.remove('r')
    sched = sched.strip()
    return sched

def make_tod_sched(teacher): #make sure that a fixed-width font is used, look for good symbols to represent pres_session
    tod_sched = '\n%-7s:' %('Status')
    lwords = []
    free = False
    for i in range(8):
        position = teacher.today_sched[i]
        if position == 'f':
            word = teacher.free_pos
            if teacher.is_present:
                word += '*' # '*' denotes that teacher is free somewhere around here.
                free = True
        else:
            word = position.upper()

        if teacher.assigned[i] == position: #this would happen only for pres_teachers, unless someone has a numerical name.
           word += '(proxy)'
        word += ' ' #for neatness
        length = len(word)
        lwords += [length]
        tod_sched += '%s\t' % word

        if i == 3:
            r = teacher.recess_pos.upper()
            tod_sched += '%s\t' % r
            lwords.append(len(r))

    sessions = '%-7s:' %('Session')
    slist = []
    if pres_session > 3:
        comp = pres_session
    else:
        comp = pres_session + 1
    for i in range(1, 9):
        slist += [i]
        if i == 4:
            slist += ['RECESS']

    n = 1
    for ses in slist:
        length = lwords[n-1]
        tnums = length / 8 + 1
        if type(ses) != str: #check for non-recess sessions
            if ses < 5:
                snum = ses - 1
            else:
                snum = ses
            if snum == pres_session: #this never happens for 4
                ses = str(ses) + '\x0e'
        else:
            if pres_session == 4:
                ses += '\x0e'
        sessions += '%s' % ses
        sessions += '\t' * tnums
        n += 1
    free_message = "Note:'*' denotes that %s is free in, or somewhere around %s.\n\n" % (teacher.first_name,
                                                                                   teacher.free_pos)
    teacher.tod_sched = sessions + tod_sched
    if free: #happens only for pres_teachers
        teacher.tod_sched = free_message + teacher.tod_sched
    if not teacher.is_present:
        teacher.tod_sched = '('+teacher.status+')\n\n' + teacher.tod_sched

def dispClaMoni(claMoni, special=''): #special to be used in displaystats()
    if len(claMoni) == 0:
        print 'No class requires monitoring!'
        return
    print 'Classes which require%s monitoring:\n' % special
    print 'Class\tSession(s)'

    for i in claMoni.items():
        g = i[0] #g for grade
        pS = i[1] #p for position
        pString = ''
        for j in pS:
            pString += str(j+1) + ', ' #added 1 to convert from computer 'language' to human 'language'
        pString = pString.strip(', ')
        print g + '\t' + pString
    if len(claMoni) > 2:
        print "\n(Total %i.)" % len(claMoni)

def attendance(): #the list thus formed can be used to obtain the chronological order of the coming of teachers
    print "\nHello teachers, type your good names below to mark your attendance, and press enter after each:\n\
When finished, just type 'quit'.\n"
    l = len(teachers)
    count = 0
    while count < l:
        name = raw_input()
        name = name.lower()
        if name == 'quit':
            break
        elif name in same_first_names:
            print "Please provide your full name.\n"
            continue
        elif name not in names:
            print "Please type your name correctly. If this message persists, please consult the management.\n"
            continue

        c = 0
        for i in range(len(pres_teachers)):
            teacher = pres_teachers[i]
            if name.lower() == teacher.title_name.lower() or name == teacher.name.lower():
                print "Why are you retyping your name? Please let others type theirs, or type 'quit' if \
everyone has completed doing so.\n"
                c = 1
                break
        if c:
            continue
        for t in range(len(abs_teachers)):
            teacher = abs_teachers[t]
            if name == teacher.title_name.lower() or name == teacher.name.lower(): #the probability that first_name of a teacher is the (full) name of another teacher, is very less.
                teacher.is_present = True
                teacher.status = teacher.status[:3]
                pres_teachers.append(abs_teachers.pop(t))
                break
        print "Have a nice day, %s.\n" % teacher.title_name
        count += 1
    if count == l:
        print "Enough! It seems all are present today."
    elif count == 0:
        print "No one is present today!" #add additional options here
        print 'Exiting the shell.'
        exit()

def out(): #for quitting the shell
    today_stats = Stats(teachers, abs_teachers, pres_teachers, proxy_teachers, comp_proxies, s_proxies, proxies, gen_proxies,
                                custom_proxies, removed_proxies, claMoni)
    with open(filename, 'wb') as today_file:
        pickle.dump(today_stats, today_file)
    with open('log.pkl', 'wb') as log_file:
        pickle.dump(datetime.datetime.now(), log_file)

def printItems(list): #only for teachers
    if list == []:
        print 'No teacher.'
        return
    if 'proxy' in list: #when the seeked teacher has a proxy at her/his present position.
        print list[0].name + ' (proxy, in place of ' + list[2].title_name + ')'
        return
    else:
        if len(list) > 2:
            print "(Total %i.)\n" % len(list)
    for i in range(len(list)):
        print list[i].name

def pause():
    print '_' * random.randint(20, 40)
def displayStats(d):
    filename = 'History/' + d + '.pkl'
    if os.path.exists(filename):
        f = open(filename, 'rb')
        stat = pickle.load(f)
        f.close()
        date_list = d.split('-')
        day = days[datetime.datetime.weekday(datetime.date(int(date_list[0]), int(date_list[1]), int(date_list[2])))]
        today_date_str = str(datetime.datetime.now().date())
        if d == today_date_str: #to print today's date for today_stats.
            w = '(%s)' % today_date_str
        else:
            w = ''
        print '\nDay: %s %s' % (day, w)
        pause()
        print '\nPresent teachers:\n'
        printItems(stat.pres_teachers)
        pause()
        print '\nAbsent Teachers:\n'
        printItems(stat.abs_teachers)
        pause()
        print '\nProxies:\n'

        printProxies(proxies)
        pause()
        if d != today_date_str:#to decide whether to use 'require' or 'required'.
            sp = 'd'
        else:
            sp = ''
        print
        dispClaMoni(stat.clamoni, sp)
        pause()
    else:
        print 'Record unavailable.'

#instead of computing some terms on demand, such as current proxies, save them, for each session. Then display them as
#per user's demand.
def on_going():
    global session, pres_session, free_teachers, s_proxies, comp_proxies, err_count

    command_error = True
    choice = raw_input(prompt)
    choice = choice.lower()


    mSession = (datetime.datetime.now() - start).seconds #mSession because it's mathematical
    session = int(mSession) / (30 * 60)#consider recess' approximation here
    ses = session
    if ses == 4:
        ses = 'recess'
    elif pres_session < 4:
        ses = session + 1

    if session > 9:
        out()
        print "School time is over. Today's data has been saved. Thank you."

    if pres_session != session: #notify the user if it feels good
        pres_session = session
        free_teachers = []
        for teacher in pres_teachers:
            teacher.update_status()

            teacher.today_sched.insert(4, 'r')
            if teacher.today_sched[session] == 'f':
                free_teachers.append(teacher)
            teacher.today_sched.remove('r')

        for teacher in teachers:#if the user is interested in viewing the tod_scheds of absent teachers also.
            make_tod_sched(teacher) #a function like update_tod_sched would probably be better for just updating.
        out() #to save the day's data every time a session gets over, for safety.

    if not choice:
        command_error = False
    if choice == "now proxies":
        choice = 'proxies during ' + str(ses)
    if "-" in choice:
        choice_elements = choice.split("-")
        if choice_elements[0] in same_first_names and len(choice_elements) == 2:
            print "Please enter %s's full name." % choice_elements[0].capitalize()
            command_error = False
        else:
            for teacher in teachers:
                if choice_elements[0] == teacher.title_name.lower():
                    if choice_elements[1] == 'proxies':
                        tp = teacher.proxies
                        if len(tp) == 0:
                            print 'No proxies.'
                        else:
                            for i in range(len(tp)):
                                p = tp[i]
                                print proxyFormat(p)
                        command_error = False
                    else:

                        try:
                            if choice_elements[1] == 'gender':
                                f = "Don't you know even that? It's "
                                l = '.'
                            else:
                                f = l = ''
                            outp = f+str(getattr(teacher, choice_elements[1]))+l
                            print outp
                            command_error = False
                        except:
                            pass
                    break

        if choice_elements[1] == 'proxies' and choice_elements[0] in ['custom', 'generated', 'removed']+possible_positions:
            if choice_elements[0] == 'custom':
                list = custom_proxies
            elif choice_elements[0] == 'generated':
                list = gen_proxies
            elif choice_elements[0] == 'removed':
                list = removed_proxies
            else:
                list = []
                for proxy in proxies:
                    if proxy[2] == choice_elements[0]:
                        list.append(proxy)
            if list == []:
                print 'No proxies.'
            else:
                for i in range(len(list)):
                    print proxyFormat(list[i])
                if len(list) > 2:
                    print "\n(Total %i.)" % len(list)
            command_error = False

        if choice_elements[1] == 'teachers' and choice_elements[0] in ['abs', 'pres', 'proxy', 'free', 'same_name']:
            if choice_elements[0] == 'abs':
               p_list = abs_teachers
            elif choice_elements[0] == 'pres':
                p_list = pres_teachers
            elif choice_elements[0] == 'free':
                p_list = free_teachers
            elif choice_elements[0] == 'same_name':
                p_list = same_name_teachers
            else:
                p_list = proxy_teachers
            if choice_elements[0] == 'free' and pres_session == 4:
                print recess_message
            else:
                printItems(p_list)
            command_error = False

    elif ' during ' in choice:
            choice_elements = choice.split(' during ')
            grade = choice_elements[0].lower()
            inp_session = choice_elements[1] #let it be a string, for now.
            if grade == 'proxies' and inp_session in [str(x) for x in range(1, 9)]+['recess']: #sounds weird!
                command_error = False
                c = 0
                for proxy in proxies:
                    if proxy[3] == int(inp_session)-1:
                        c+=1
                        print proxyFormat(proxy)
                if c == 0:
                    print "No proxies."

            if grade == 'free':
                if inp_session == 'recess':
                    val = recess_message
                else:
                    val = find_free_teachers(inp_session)
            else:
                val = teacherSeek(grade, str(inp_session))
            if val:
                if type(val) == type([3]):
                    printItems(val)
                else:
                    print val
                command_error = False

    #just like 'now proxies' command is used, the following block can be shortened.
    elif 'now in' in choice:
        choice_elements = choice.split('now in')
        if len(choice_elements) == 2:
            grade = choice_elements[1].lstrip().lower() #lstrip() is used to remove the space at the left.
            if pres_session < 4:
                arg = pres_session + 1 #added one because pres_session is in computer speak, starts from 0.
            elif pres_session == 4:
                arg = 'recess'
            else:
                arg = pres_session
            val = teacherSeek(grade, str(arg))
            if val:
                if type(val) == type([3]):
                    printItems(val)
                else:
                    print val
                command_error = False

    elif choice == "today":
        command_error = False
        print "Today is", today, "(" + str(datetime.datetime.now().date()) + ")." #display date in a cleaner format,
                                                                                  #like '28th June, 2016', or don't
                                                                                  #display it.
    elif choice == "suggest proxies":
        if len(s_proxies) == 0:
            print 'No proxies!'
        else:
            printProxies(s_proxies)
        command_error = False
    elif choice == "proxies":
        if len(proxies) == 0:
            print 'No proxies today!'
        else:
            if len(proxies) == 1:
                word = 'proxy'
            else:
                word = 'proxies'
            print "Today's %s:" % word
            printProxies(proxies)
        command_error = False

    elif choice == "assign proxies":
        proxy_assignment()
        getClaMoni(abs_teachers, proxies)
        proxySort(proxies)
        command_error = False
    elif choice == 'clamoni':
        dispClaMoni(claMoni)
        command_error = False
    elif choice == 'remove proxies':
        custom_removal()
        getClaMoni(abs_teachers, proxies)
        command_error = False
    elif choice == 'introduce':
        if welcome():
            s_proxies = []
            comp_proxies = []
            suggest_proxies(abs_teachers, pres_teachers, s_proxies)
            print "New proxies may have been added to suggestions. You should check them out."
        command_error = False
    elif choice == 'q':
        command_error = False
        choice_2 = raw_input("Sure to quit (Y/N)? ")
        if choice_2 == 'y':
            out()
            quit()

    elif choice == 'session':
        command_error = False
        if pres_session != 4:
            print "It's session %s going on." % ses
        elif pres_session == 4:
            print "It's RECESS! Don't you hear the noise?" #what if the user responds to this question?
    elif choice == 'teachers':
        printItems(teachers)
        command_error = False
    elif choice == 'display stats':
        out()
        d = raw_input('Enter the date in format YYYY-MM-DD: ')
        displayStats(d)
        command_error = False
    elif choice == 'today stats':
        out()
        d = str(datetime.datetime.now().date())
        displayStats(d)
        command_error = False
    elif choice == 'help':
        print help_message
        command_error = False
    else:
        for teacher in teachers:
            if choice == teacher.name.lower():
                print teacher
                command_error = False
                break

    if command_error:
        err_count += 1
        if err_count >3: #to print extra stuff when the user types incorrect commands for 3 times straight. Try to think
                         #of better help responses.
            w = "Type 'help' to see a list of queries."
            err_count = 0
        else:
            err_count = 0
            w = ''
        print error_message, w

def time_passed():
    #following code keeps track of time since last logout activity.
    #add code for converting from hours to days.
    if os.path.isfile('log.pkl'):
        logfile = open('log.pkl', 'rb')
        logtime = pickle.load(logfile)
        now = datetime.datetime.now()
        raw_delta = now - logtime
        #not using datetime.timedelta here, doesn't give the number of months.
        month_delta = now.month - logtime.month
        if month_delta <= 0:
            month_delta = 12 + month_delta #it's correct. Just think.
        if now.day < logtime.day and month_delta != 0: #the 1st statement never happens for the same month of same year.
            month_delta -= 1
        month_delta = month_delta % 12 #in the case month_delta == 0 and now.day < logtime.day
        num_of_days = [31, 28, 31, 30, 31, 30, 30, 31, 30, 31, 30, 31] #in corresponding months.
        if now.year % 4 == 0: #deals with leap years.
            num_of_days[1] = 29

        if now.day < logtime.day:
            day_delta = num_of_days[now.month-2] - logtime.day + now.day
        else:
            day_delta = now.day - logtime.day
        year_delta = now.year - logtime.year

        if now.time() < logtime.time():
            day_delta -= 1
            if now.day == logtime.day: #never happens for the same day of the same month of the same year, because of the
                                       #'parent' condition.
                month_delta -= 1

        if now.month < logtime.month or (now.month == logtime.month and (now.day < logtime.day or \
                                                                         (now.day == logtime.day and now.time() < \
                                                                         logtime.time()))):
            year_delta -= 1

        second_delta = raw_delta.seconds
        minute_delta = (second_delta // 60) % 60
        hour_delta = second_delta // 3600

        second_delta = second_delta % 60 #otherwise you'll get stuff like "2 minutes, 121 seconds"!
        #think of singulars
        year_delta = str(year_delta) + ' years'
        month_delta = str(month_delta) + ' months'
        day_delta = str(day_delta) + ' days'
        hour_delta = str(hour_delta) + ' hours'
        minute_delta = str(minute_delta) + ' minutes'
        second_delta = str(second_delta) + ' seconds'
        msg_of_delta = ' since last logout.' #add logout time (string) here.
        for item in [second_delta, minute_delta, hour_delta, day_delta, month_delta, year_delta]:
            if item[0] != '0': #remember that, item is a string.
                msg_of_delta = ', ' + item + msg_of_delta
        msg_of_delta = "It has been " + msg_of_delta.lstrip(', ')
    else:
        with open('log.pkl', 'wb') as f:
            pickle.dump(datetime.datetime.now(), f)
        msg_of_delta = ''
    return msg_of_delta

def same():
    #some dealing with same names
    for teacher_1 in teachers:
        teachers.remove(teacher_1)
        for teacher_2 in teachers:
            if teacher_1.first_name == teacher_2.first_name:
                same_name_teachers.append(teacher_1)
                teacher_1.title_name = teacher_1.name
                same_first_names.append(teacher_1.first_name.lower())
        teachers.append(teacher_1)
#________________________________________________Main stuff starts here_________________________________________________

teachers = []
same_name_teachers = []
same_first_names = []
comp_proxies = [] #computer choosen proxies
s_proxies = [] #suggested proxies
proxies = []
names = []
gen_proxies = [] #computer generated proxies
custom_proxies = [] #user-defined proxies
removed_proxies = []
claMoni = {} #grades which require monitoring
outshell = True #has a very little purpose
possible_positions = [] #make this list more realistic
for i in range(1, 11):
    for section in ['a', 'b', 'c']:
        pos = str(i) + section
        possible_positions.append(pos)

special_positions = ['music room', 'biology lab', 'staff room', 'library', 'ground', 'chemistry lab', 'physics lab',\
                     'computer lab']
possible_positions.extend(['11s', '11c', '12s', '12c']+special_positions)

days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

today = days[datetime.datetime.weekday(datetime.datetime.now().date())]

if today == 'Sunday':
    print "I don't think you need me on a Sunday!" #make such statements random
    #modify this block further. It's different from 'non-school times'.
    quit()

tod = datetime.datetime.now().date()
start_t = datetime.time(12) #what if it's a midnight school?
start = datetime.datetime.combine(tod, start_t)
end = start + datetime.timedelta(hours=4, minutes=30)

present = datetime.datetime.now()

#check the below couple
recess_start = start + datetime.timedelta(2, 5)#approximation of 5 minutes
recess_end = recess_start + datetime.timedelta(0, 30) #same here


pres_teachers = []
abs_teachers = []
proxy_teachers = []
free_teachers = []

if not start < present < end:
    print "It isn't school time presently." # more info to be added
    og = False
    quit()

else:
    pres_session = 'blah'
    og = True
    #loads data from saved files.
    filename = "History/" + str(datetime.datetime.now().date()) + '.pkl'
    if os.path.exists(filename):
        pre_opened = True #the program was opened earlier today.
        today_file = open(filename, 'rb')
        today_stats = pickle.load(today_file)
        today_file.close()

        teachers = today_stats.teachers
        abs_teachers = today_stats.abs_teachers
        pres_teachers = today_stats.pres_teachers
        proxy_teachers = today_stats.proxy_teachers
        comp_proxies = today_stats.comp_proxies
        s_proxies = today_stats.s_proxies
        proxies = today_stats.proxies
        gen_proxies = today_stats.gen_proxies
        custom_proxies = today_stats.custom_proxies
        removed_proxies = today_stats.removed_proxies
        same()
    else:
        name_file = open('Names.pkl', 'rb')
        Names = pickle.load(name_file) #different from names.
        #brings (all) teachers in
        for i in range(len(Names)):
            name = Names[i]
            name = 'Teachers/' + name
            t = open(name+'.pkl', 'rb')
            oteacher = pickle.load(t) #oteacher for teacher with old attributes
            t.close()
            teacher = Teacher(oteacher.first_name, oteacher.last_name, oteacher.classes, oteacher.subjects, oteacher.schedule,\
            oteacher.free_pos, oteacher.recess_pos, oteacher.gender)
            teacher.assigned = {}
            for m in range(8):
                teacher.assigned[m] = False
            teacher.is_present = False
            teacher.status = teacher.status[:3]
            teacher.status = teacher.status.strip()
            teacher.status += " is absent today."
            teacher.today_sched = teacher.schedule[datetime.datetime.weekday(datetime.datetime.now().date())]
            teachers.append(teacher)

        abs_teachers = teachers[:]
        same()
        for teacher in teachers:
            names.append(teacher.name.lower())
            if teacher.title_name.lower() not in names:
                names.append(teacher.title_name.lower())
        print "Following teachers are on roll:\n"
        printItems(teachers)
        attendance()
        pre_opened = False

    from onGoing import *

    if not pre_opened:
        suggest_proxies(abs_teachers, pres_teachers, s_proxies)
        proxySort(s_proxies)
        proxySort(comp_proxies)

error_message = "Can't identify. Try again."
err_count = 0

help_message = '''\nQueries:\n
proxies                 : To display proxies.
<teacher name>-proxies  : To get the teacher's proxies.
<class>-proxies         : To get the class's proxies.
proxies during <session>: To get proxies during a particular session.
now proxies             : To get proxies during the current session.
assign proxies          : To assign the proxies for absent teachers.
proxy-teachers          : To know which teachers have proxies today.
clamoni                 : To display classes which require monitoring.

<teachername>-status    : To get the status of the teacher.
<teachername>-tod_sched : To get today's schedule of the teacher.
<teacher fullname>      : To get info about the teacher.
<teachername>-sched     : To get the weekly schedule of the teacher.
<teachername>-is_present: To check whether the teacher is present or not.

<class> during <session>: To find the teacher in the class during the given session.
free during <session>   : To get the names of free teachers during the session.
now in <class>          : To find the teacher present in this class.

free-teachers           : To know which teachers are free presently.
pres-teachers           : To know which teachers are present today.
abs-teachers            : To know which teachers are absent today.

introduce               : To introduce a teacher in the school.

today stats             : To display today's information.
display stats           : To display a given day's information.

help                    : To display these queries.'''

message = '''
Type your commands in the following lines.
To see the list of queries, type 'help'.
To quit, type 'q'.'''

recess_message = "All teachers are practically free during recess!"
prompt = '\n-|-> '

print time_passed()
print
if og:
    if not pre_opened:
        print
        #following two lines have to be here for session to be defined initially. Otherwise, assigning proxies before
        #getting into the on_going() function would give a NameError.
        mSession = (datetime.datetime.now() - start).seconds #mSession because it's mathematical
        session = int(mSession) / (30 * 60)#consider recess' approximation here
        proxy_assignment()
    getClaMoni(abs_teachers, proxies)
    print message
if og:
    while 1:
        on_going()
