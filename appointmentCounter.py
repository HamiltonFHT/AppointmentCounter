''' Appointment Counter 
    Copyright (C) 2014  Tom Sitter; Hamilton Family Health Team

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along
    with this program; if not, write to the Free Software Foundation, Inc.,
    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.'''


from tkinter.filedialog import askopenfilename, asksaveasfilename, Tk
import csv

#Prevent tk window from displaying
root = Tk()
root.withdraw()

appointments = {}
currentPatient = ''

#Get user to select a file
filename = askopenfilename(title='Select a PSS patient appointment report to analyze')

with open(filename, 'r') as f:
    reader = csv.reader(f, delimiter=",", quotechar='"')
    #Read file row by row
    for row in reader:
        #Skip empty rows (usually at top or bottom of file)
        if len(row) == 0:
            continue
        #Skip header
        elif row[0] == 'Patient #':
            continue
        #If first entry in row is a number (Patient ID)
        #Begin counting appointment for a new patient
        elif row[0].isdigit():
            currentPatient = ", ".join(reversed(row[1:3]))
            appointments[currentPatient] = 0
            print(currentPatient)
        #If the appointment has 'cancelled' or 'deleted' in the title, skip it
        #Otherwise, increase the number of appointments by 1
        elif (not 'deleted' in row[0] and
                not 'cancelled' in row[0] and
                not 'CANCELLED' in row[0] and
                not 'DELETED' in row[0]):
                appointments[currentPatient] += 1
        else:
            continue

#Ask the user to select a file for output
output_file = asksaveasfilename(initialfile='Patient_Appointment_Count.csv', defaultextension='.csv',
                   filetypes=[('CSV','*.csv')],title='Export Count of Patient Appointments As...')

#If no file select, print to console
if output_file == "":
    print("No file selected, printing to console")
    for w in sorted(appointments, key=appointments.get, reverse=True):
        print("%s: %d" % (w, appointments[w]))
else:
    #Otherwise open the file and write appointments data to it
    with open(output_file, 'w', newline="") as f:
            writer = csv.writer(f, delimiter=',')
            writer.writerow(["Patient", "# Appointments"])
            writer.writerow(["Total", sum(appointments.values())])
            # To sort by number of appointments, use this condition in the for loop
            #for w in sorted(appointments, key=appointments.get, reverse=True):
            for w in sorted(appointments):
                writer.writerow([w, appointments[w]])
