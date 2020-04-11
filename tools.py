import datetime

def repetitiveEventToThisWeek(events):
    return events

def sortEvents(events):
    return events

def selectEvents(events, week, group):

    # consider that the first prev saturday is now
    previous_saturday = datetime.datetime.now()
    next_saturday = next_weekday(previous_saturday, 6)

    for i in range(0, week - 1):
        previous_saturday = next_saturday
        next_saturday = next_weekday(previous_saturday, 6)

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
