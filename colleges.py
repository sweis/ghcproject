import urllib2

# A comma-separated values (CSV) file is a text file where each line contains a
# list of values separated by commas, like:
# Name, Date, Favorite Color
# Alice, 1/1/1990, blue
# Bob, 2/12/1992, yellow

# This is a URL is a CSV file with some data about colleges:
url = "https://raw.githubusercontent.com/sweis/ghcproject/master/collegedata.csv"

# These are the headers in the file. They also appear in the file itself, but
# we're going to define some shorter ones here for convenience.
headers = [ "Institution", "State", "Region", "Level", "Degree Status",
    "Out-of-state price", "In-state price", "Enrollment", "Doctorates",
    "Masters", "Bachelors", "% Admitted", "Admissions Yield", "% Admitted Men",
    "% Admitted Women" ]

# Here are some numbers used to represent different types of levels
levels = {
    1 : "Four or more years",
    2 : "At least 2 but less than 4 years",
    3 : "Less than 2 years (below associate)",
    -3 : "{Not available}"
}

regions = {
    0: "US Service",
    1: "New England",
    2: "Mid East",
    3: "Great Lakes",
    4: "Plains",
    5: "Southeast",
    6: "Southwest",
    7: "Rocky Mountains",
    8: "Far West"
}

# Here are some numbers used to represent different degree granting statuses
degree_status = { 1: "Degree-granting", 2 : "Nondegree-granting", -3:"N/A" }

# This uses a library called urllib2 (URL library version 2) to open the URL
# response = urllib2.urlopen(url)
# This will read data from the URL into a list (or array) of lines,
# called 'lines'
#lines = response.readlines()
with open('/Users/saw/Workspace/ghcproject/collegedata.csv') as f:
    lines = f.readlines()

# This creates an empty list (or array) of all colleges, where we'll add data
# as we process it
all_colleges = [ ]
num_colleges_to_read = 100

# This will read each line in the list of lines from 1 to num_colleges_to_read
# We're actually skipping the first line, since it counts from 0. That contains
# the header row in the file that we're going to ignore.
for line in lines[1:]: #[1:num_colleges_to_read]:
    # This takes a line, and strips off what its called a "linebreak" at the
    # end. That just means the enter key. Then it splits it into a smaller
    # list called 'fields', using a comma to separate between items. So
    # this,is,some,datawould become ['this', 'is', 'some', 'data']
    fields = line.strip().split(',')

    # This creates a datatype called a dictionary or a map called 'college'.
    # Maps will map keys to values, so you can have something like:
    # my_map[key] = value or my_map["Name"] = "Alice"
    college = { }
    # This creates a variable 'i' that counts from 0 up to the number of fields
    for i in range(0, len(fields)):
        # For 'entry', this will map the ith key value to the ith field. This
        # will map headers to actual field values for this row
        college[headers[i]] = fields[i]

    all_colleges.append(college)

# This is a function which can take an college and convert it to a easily
# readable string that we can print out.
def pretty_print(college):
    # The {} in this template will be fileld in by the format() function.
    # The "\" character lets you write a long line
    template = "{} ({} - {}) Students {} "  \
        "Out ${} In ${} " \
        "Admitted: {}% Women Admitted: {}%"
    # Format will put each value into the corresponding template placeholder
    return template.format(
        college["Institution"],
        regions[int(college["Region"])],
        college["State"],
        college["Enrollment"],
        college["Out-of-state price"] or "?",
        college["In-state price"] or "?",
        college["% Admitted"] or "?",
        college["% Admitted Women"] or "?"
    )

def convert_to_int(college, field_name):
    value = college[field_name]  # Might be empty
    if value:
        return int(value)
    else:
        return 0

sorted_colleges = sorted(all_colleges,
    key = lambda college : convert_to_int(college, "% Admitted Women"),
    reverse = False)

filtered_colleges = \
    filter(lambda college: convert_to_int(college, "% Admitted Women") != 0, \
        sorted_colleges)

for college in filtered_colleges:
    enrollment = college["Enrollment"]  # This might be empty
    state = college["State"]
    if state == 'CA' and enrollment and int(enrollment) > 1000:
        print pretty_print(college)
