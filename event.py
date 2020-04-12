import json
import re
import datetime
from tools import next_weekday, selectEvents, translateDM, dayNameFromWeekday

def readEventsFromFile(file):
        events = []
        with open(file, 'r') as i:
            try:
                test = json.load(i)
                for ob in test:
                    if ob["repetitive"]:
                        events.append(event(ob["name"], ob["group"], ob["repetitive"], time_specified=ob["time_specified"], repetitive_day=ob["repetitive_day"], repetitive_time=ob["repetitive_time"]))
                    else:
                        events.append(event(ob["name"], ob["group"], ob["repetitive"], date=ob["date"], time_specified=ob["time_specified"]))

            except json.decoder.JSONDecodeError:
                print(str(file) + " is empty.")
        return events

class Events:
    def __init__(self, events_file, old_events_file):
        self.events_file = events_file
        self.old_events_file = old_events_file
        self.events = readEventsFromFile(events_file)
        self.old_events = readEventsFromFile(old_events_file)

    # Add non repetitive event
    def add(self, message:str):
        # Example: .add "Test MN" "23-04" "23:55" "313" 
        groups = re.findall('"([^"]*)"', message)
        if len(groups) < 2:
            return "Arguments incorrect."

        nume = groups[0]
        data_raw = groups[1]
        if len(groups) == 4:
            # if group is not correct
            data_raw = data_raw + ' ' + groups[2]
            date = datetime.datetime.strptime(data_raw, "%d-%m %H:%M").replace(year=2020)
            data_prelucrata = date.strftime("%Y-%m-%d %H:%M:%S")
            even = event(nume, groups[3], False, True, date=data_prelucrata)
        else:
            # if group is not correct
            date = datetime.datetime.strptime(data_raw, "%d-%m").replace(year=2020)
            data_prelucrata = date.strftime("%Y-%m-%d %H:%M:%S")
            even = event(nume, groups[2], False, False, date=data_prelucrata)

        # Add newly created event to internal list
        self.events.append(even)

        # Update events file
        f = open(self.events_file, "w")
        json.dump([ob.__dict__ for ob in self.events], f)
        return "Successful add non-repetitive event."
    

    # Add repetitive event
    def addR(self, message:str):
        # Example: .addR "Curs MN" "24-04" "18:00" "313" 
        groups = re.findall('"([^"]*)"', message)
        if len(groups) < 2:
            return "Arguments incorrect."

        nume = groups[0]
        data_raw = groups[1]
        weekday = datetime.datetime.strptime(data_raw, "%d-%m").replace(year=2020).weekday()
        
        if len(groups) == 4:
            even = event(nume, groups[3], True, True, repetitive_day=weekday, repetitive_time=groups[2])
        else:
            date = datetime.datetime.strptime(data_raw, "%d-%m").replace(year=2020)
            data_prelucrata = date.strftime("%Y-%m-%d %H:%M:%S")
            even = event(nume, groups[2], True, False, repetitive_day=weekday)

        # Add newly created event to internal list
        self.events.append(even)

        # Update events file
        f = open(self.events_file, "w")
        json.dump([ob.__dict__ for ob in self.events], f)
        return "Successful add repetitive event."
    

    def show(self, message:str, group="all"):
        # Parse week number
        splitted_msg = message.split()
        if len(splitted_msg) > 2:
            return 'Comanda `.orar` se foloseste astfel: `.orar [nr_saptamanii]`\n`nr_saptamanii` reprezentand saptamana de afisat (1 - sapt curenta).'
        if len(splitted_msg) == 1:
            weeks = 1
        elif splitted_msg[1] == 'tot' or splitted_msg[1] == 'full' or splitted_msg[1] == 'all':
            weeks = -1
            
        else:
            try:
                # Try converting to int
                weeks = int(splitted_msg[1])
                if weeks < 1:
                    return 'Comanda `.orar` se foloseste astfel: `.orar [nr_saptamanii]`\n    ->`nr_saptamanii` reprezentand saptamana de afisat (1 - sapt curenta).'
                    
            except ValueError:
                #Handle the exception
                return 'Comanda `.orar` se foloseste astfel: `.orar [nr_saptamanii]`\n    ->`nr_saptamanii` reprezentand saptamana de afisat (1 - sapt curenta).'

        # Select events
        selected_events = selectEvents(self.events, weeks, group)

        # Manage header
        if weeks == -1:
            header = "Toate evenimentele sunt:\n"
        elif weeks == 1:
            header = "Evenimentele pentru saptamana curenta sunt:\n"
        else:
            header = "Evenimentele pentru saptamana " + str(weeks) + " sunt:\n"

        # Manage content
        content = ''
        for ev in selected_events:
            date_formatted = datetime.datetime.strptime(ev.date, "%Y-%m-%d %H:%M:%S")
            if group == "all":
                if ev.time_specified == False:
                    content += '{0}: {1.name}  --> {2}\n'.format(ev.group, ev, date_formatted.strftime("%A, %d-%B"))
                else:
                    content += '{0}: {1.name}  --> {2}\n'.format(ev.group, ev, date_formatted.strftime("%A, %d-%B %H:%M"))
            else:
                if ev.time_specified == False:
                    content += '{0.name}  --> {1}\n'.format(ev, date_formatted.strftime("%A, %d-%B"))
                else:
                    content += '{0.name}  --> {1}\n'.format(ev, date_formatted.strftime("%A, %d-%B %H:%M"))

        # Translate days and months to Romainian
        final_text = translateDM(header + content)
        return final_text


    def updateOldEvents(self):
        for ev in self.events:
            if not ev.repetitive:
                date_formatted = datetime.datetime.strptime(
                    ev.date, "%Y-%m-%d %H:%M:%S")
                if ev.time_specified:
                    if date_formatted < datetime.datetime.now() - datetime.timedelta(hours=2):
                        self.delEvent(ev)
                        print("Removed event: " + str(ev.name))
                        return("Autotask: Removed event: " + str(ev.name))
                else:
                    if date_formatted.date() < datetime.datetime.now().date():
                        self.delEvent(ev)
                        print("Removed event: " + str(ev.name))
                        return("Autotask: Removed event: " + str(ev.name))

        return 0



    def delEvent(self, ev):
        # Remove event from events list
        try:
            self.events.remove(ev)
        except ValueError:
            print("Cannot delete event, because it is not in events list")
            return 0
        
        # Put event into old_events list
        self.old_events.append(ev)

        # Update events file
        f = open(self.events_file, "w")
        json.dump([ob.__dict__ for ob in self.events], f)

        # Update old_events file
        g = open(self.old_events_file, "w")
        json.dump([ob.__dict__ for ob in self.old_events], g)
        return 1

    def manager_show(self):
        if len(self.events) == 0:
            return 'Nu exista niciun eveniment.'
        header = 'Evenimentele sunt:\n'
        content = ''
        # Show events
        i = 0;
        for ev in self.events:
            if ev.repetitive:
                weekday = dayNameFromWeekday(ev.repetitive_day)
                if ev.time_specified:
                    content += f'{i}. R {ev.group}: {ev.name}  --> {weekday} {ev.repetitive_time}'
                else:
                    content += f'{i}. R {ev.group}: {ev.name}  --> {weekday} Time not specified'
            else:
                if ev.time_specified:
                    date_with_time = datetime.datetime.strptime(ev.date, "%Y-%m-%d %H:%M:%S").strftime("%A, %d-%B %H:%M")
                    content += f'{i}. {ev.group}: {ev.name}  --> {date_with_time}'
                else:
                    date_without_time = datetime.datetime.strptime(ev.date, "%Y-%m-%d %H:%M:%S").strftime("%A, %d-%B")
                    content += f'{i}. {ev.group}: {ev.name}  --> {date_without_time} Time not specified'
            i += 1
        
        final_text = translateDM(header + content)
        return final_text
        
    def delete(self, message):
        groups = message.split()
        if len(groups) == 1:
            return self.manager_show()
        else:
            try:
                # we need to delete event
                event_index = int(groups[1])
                return 'Successful deletion.' if self.delEvent(self.events[event_index - 1]) == 1 else 'Deletion failed.'
            except Exception as e:
                print(e)
                return('Comanda gresita: A se folosi cu formatul: `.del [int]`')
        


class event:
    def __init__(self, name, group, repetitive, time_specified, date = None, repetitive_day = None, repetitive_time = None):
        # Event name
        self.name = name
        # If the event is specific for a group
        self.group = group
        # If the event repeats every week
        self.repetitive = repetitive
        self.time_specified = time_specified

        if self.repetitive:
            self.repetitive_day = repetitive_day
            self.repetitive_time = repetitive_time
        else:
            self.date = date
