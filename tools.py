import datetime

def repetitiveEventToThisWeek(events):
    for ev in events:
        if ev.repetitive == True:
            ev.repetitive = False
            # get yesterday
            yesterday = datetime.datetime.today() - datetime.timedelta(days=1)
            ev.date = next_weekday(yesterday, ev.repetitive_day)
            if ev.time_specified:
                time_parts = ev.repetitive_time.split(':')
                ev.date = ev.date.replace(hour=int(time_parts[0]), minute=int(time_parts[1]))
            ev.date = ev.date.strftime("%Y-%m-%d %H:%M:%S")


    return events

def sortEvents(events):
    events.sort(key=lambda item:item.date)
    return events

def selectEvents(events, week, group):

    # consider that the first prev saturday is now
    previous_saturday = datetime.datetime.now()
    next_saturday = next_weekday(previous_saturday, 6)

    for i in range(0, week - 1):
        previous_saturday = next_saturday
        next_saturday = next_weekday(previous_saturday, 6)

    #no_repetitive_events = repetitiveEventToThisWeek(events)

    selected_events = []
    for ev in events:
        if ev.repetitive == False:
            if week == -1:
                if group != "all":
                    if ev.group == group or ev.group == "all":
                        selected_events.append(ev)
                else:
                    selected_events.append(ev)
            else:
                date_formatted = datetime.datetime.strptime(
                    ev.date, "%Y-%m-%d %H:%M:%S")
                if previous_saturday < date_formatted < next_saturday:
                    if group != "all":
                        if ev.group == group or ev.group == "all":
                            selected_events.append(ev)
                    else:
                        selected_events.append(ev)
        else:
            if group != "all":
                if ev.group == group or ev.group == "all":
                    selected_events.append(ev)
            else:
                selected_events.append(ev)

    selected_events = repetitiveEventToThisWeek(selected_events)
    selected_events = sortEvents(selected_events)

    return selected_events

def next_weekday(d, weekday): # 0 = Monday, 1=Tuesday, 2=Wednesday...
    days_ahead = weekday - d.weekday()
    if days_ahead <= 0: # Target day already happened this week
        days_ahead += 7
    return d + datetime.timedelta(days_ahead)

def translateDM(text):
    for eng, ro in {
        "Monday": "Luni",
        "Tuesday": "Marti",
        "Wednesday": "Miercuri",
        "Thursday": "Joi",
        "Friday": "Vineri",
        "Saturday": "Sambata", 
        "Sunday": "Duminica", 
        "January": "Ian", 
        "February": "Feb", 
        "March": "Mar", 
        "April": "Apr", 
        "May": "Mai", 
        "June": "Iun", 
        "July": "Iul", 
        "August": "Aug", 
        "September": "Sep", 
        "October": "Oct", 
        "November": "Noi", 
        "December": "Dec"
        }.items():
        text = text.replace(eng, ro)
    return text
