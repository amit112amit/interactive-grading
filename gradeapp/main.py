import json
from pathlib import Path
from functools import partial
from itertools import dropwhile

from bokeh.layouts import column, row
from bokeh.models import (CheckboxGroup, ColumnDataSource, Div, HoverTool, Label,
                          Slider, Span)
from bokeh.plotting import curdoc, figure

from .helpers import get_marks_stats, prepare_histogram_data_source

# Get the app directory name
appdir = Path(__file__).parent

# Read course name, Excel file name and the maximum marks
with open(f'{appdir}/data/course_details.json', 'r') as inputfile:
    course_details = json.load(inputfile)

coursetitle = course_details['title']
excelfilename = course_details['excelfile']
maxmarks = course_details['maxmarks']

marksfile = f'{appdir}/data/{excelfilename}'

# Get total number of students and the average marks
total_students, average_marks = get_marks_stats(marksfile)

# Prepare histogram data source
hist_data = prepare_histogram_data_source(marksfile, maxmarks)
hist_source = ColumnDataSource(data=hist_data)
scores = hist_data['bin_value']

# Get the lowest score in the class
for first_score, h in enumerate(hist_data['top']):
    if h > 0:
        break

# Set the ranges
xmin = scores[first_score] - 2
xmax = maxmarks
ymin = 0
ymax = max(hist_source.data['top']) + 2

# Make the figure
plot = figure(title=f'{coursetitle}', x_range=(xmin, xmax), y_range=(
    ymin, ymax), sizing_mode='scale_both', tools=[])
plot.xaxis.axis_label = "Score"
plot.yaxis.axis_label = "Count"

# Create the tooltip
hovertool = HoverTool(tooltips=[("Score", "@bin_value"),
                                ("Count", "@top")])
plot.add_tools(hovertool)

# Create the base histogram
plot.quad(source=hist_source, top='top', bottom=0, left='left', right='right')

# Add the average marker
average_marker = Span(location=average_marks, dimension='height', line_color='red',
                      line_dash='dashed', line_width=3)
plot.add_layout(average_marker)

# Create a Span for each grade
a_span = Span(location=80, dimension='height',
              line_color='green', line_width=3)
am_span = Span(location=70, dimension='height', visible=False,
               line_color='green', line_width=3)
b_span = Span(location=60, dimension='height',
              line_color='green', line_width=3)
bm_span = Span(location=50, dimension='height', visible=False,
               line_color='green', line_width=3)
c_span = Span(location=40, dimension='height',
              line_color='green', line_width=3)
cm_span = Span(location=30, dimension='height', visible=False,
               line_color='green', line_width=3)
d_span = Span(location=20, dimension='height',
              line_color='green', line_width=3)
e_span = Span(location=10, dimension='height', visible=False,
              line_color='green', line_width=3)

# Create a Label for each grade
a_label = Label(x=80, y=ymax - 1, text=f"A: 0")
am_label = Label(x=70, y=ymax - 1, text=f"A-: 0", visible=False)
b_label = Label(x=60, y=ymax - 1, text=f"B: 0")
bm_label = Label(x=50, y=ymax - 1, text=f"B-: 0", visible=False)
c_label = Label(x=40, y=ymax - 1, text=f"C: 0")
cm_label = Label(x=30, y=ymax - 1, text=f"C-: 0", visible=False)
d_label = Label(x=20, y=ymax - 1, text=f"D: 0")
e_label = Label(x=10, y=ymax - 1, text=f"E: 0", visible=False)

for l in (a_span, a_label, am_span, am_label, b_span, b_label,
          bm_span, bm_label, c_span, c_label, cm_span,
          cm_label, d_span, d_label, e_span, e_label):
    plot.add_layout(l)

# Create checkboxes and sliders for each grade
a_checkbox = CheckboxGroup(labels=["A"], active=[0], width_policy="min")
a_slider = Slider(start=0, end=maxmarks, step=1, value=80, title="")
a_row = row(a_checkbox, a_slider, margin=(0, 0, 0, 100))

am_checkbox = CheckboxGroup(labels=["A-"], width_policy="min")
am_slider = Slider(start=0, end=maxmarks, step=1,
                   value=70, title="", disabled=True)
am_row = row(am_checkbox, am_slider, margin=(0, 0, 0, 100))

b_checkbox = CheckboxGroup(labels=["B"], active=[0], width_policy="min")
b_slider = Slider(start=0, end=maxmarks, step=1, value=60, title="")
b_row = row(b_checkbox, b_slider, margin=(0, 0, 0, 100))

bm_checkbox = CheckboxGroup(labels=["B-"], width_policy="min")
bm_slider = Slider(start=0, end=maxmarks, step=1,
                   value=50, title="", disabled=True)
bm_row = row(bm_checkbox, bm_slider, margin=(0, 0, 0, 100))

c_checkbox = CheckboxGroup(labels=["C"], active=[0], width_policy="min")
c_slider = Slider(start=0, end=maxmarks, step=1, value=40, title="")
c_row = row(c_checkbox, c_slider, margin=(0, 0, 0, 100))

cm_checkbox = CheckboxGroup(labels=["C-"], width_policy="min")
cm_slider = Slider(start=0, end=maxmarks, step=1,
                   value=30, title="", disabled=True)
cm_row = row(cm_checkbox, cm_slider, margin=(0, 0, 0, 100))

d_checkbox = CheckboxGroup(labels=["D"], active=[0], width_policy="min")
d_slider = Slider(start=0, end=maxmarks, step=1, value=20, title="")
d_row = row(d_checkbox, d_slider, margin=(0, 0, 0, 100))

e_checkbox = CheckboxGroup(labels=["E"], width_policy="min")
e_slider = Slider(start=0, end=maxmarks, step=1,
                  value=10, title="", disabled=True)
e_row = row(e_checkbox, e_slider, margin=(0, 0, 0, 100))

# The following data-structure stores the state of the app -- which grades are
# enabled, what are their cutoffs and counts.
grades_data = {
    'A': {
        "Enabled": True,
        "Weight": 10,
        "CutOff": 80,
        "Slider": a_slider,
        "Span": a_span,
        "Label": a_label
    },
    'A-': {
        "Enabled": False,
        "Weight": 9,
        "CutOff": 70,
        "Slider": am_slider,
        "Span": am_span,
        "Label": am_label
    },
    'B': {
        "Enabled": True,
        "Weight": 8,
        "CutOff": 60,
        "Slider": b_slider,
        "Span": b_span,
        "Label": b_label
    },
    'B-': {
        "Enabled": False,
        "Weight": 7,
        "CutOff": 50,
        "Slider": bm_slider,
        "Span": bm_span,
        "Label": bm_label
    },
    'C': {
        "Enabled": True,
        "Weight": 6,
        "CutOff": 40,
        "Slider": c_slider,
        "Span": c_span,
        "Label": c_label
    },
    'C-': {
        "Enabled": False,
        "Weight": 5,
        "CutOff": 30,
        "Slider": cm_slider,
        "Span": cm_span,
        "Label": cm_label
    },
    'D': {
        "Enabled": True,
        "Weight": 4,
        "CutOff": 20,
        "Slider": d_slider,
        "Span": d_span,
        "Label": d_label
    },
    'E': {
        "Enabled": False,
        "Weight": 2,
        "CutOff": 10,
        "Slider": e_slider,
        "Span": e_span,
        "Label": e_label
    },
}


def calculate_stats():
    """
    Calculate count and MGPA based on the current state of `grades_data`.
    """
    counts = {}
    mgpa = 0.0
    upperlimit = maxmarks + 1
    for grade, data in grades_data.items():
        if not data['Enabled']:
            continue

        # Count the number of students from histogram data
        lowerlimit = data['CutOff']
        count = hist_data['top'][lowerlimit: upperlimit].sum()

        # Update MGPA
        mgpa += count * data['Weight']

        # Store the count
        counts[grade] = count

        # Update the upperlimit for the next grade
        upperlimit = lowerlimit

    # Normalize the MGPA
    mgpa /= total_students

    return counts, mgpa


def update_plot():
    """
    Update the grade spans, labels and title based on the current state
    of `grades_data`.
    """
    # Get the MGPA and count
    counts, mgpa = calculate_stats()

    for grade, data in grades_data.items():
        if data['Enabled']:
            # Set the locations for the Span and the Label
            data['Span'].location = data['CutOff'] - 0.5
            data['Label'].x = data['CutOff'] - 0.5

            # Update the Label text
            data['Label'].text = f'{grade}: {counts[grade]}'

            # Make the Span and the Label visible
            data['Span'].visible = True
            data['Label'].visible = True

            # Enable the slider
            data['Slider'].disabled = False
        else:
            # Turn off the disabled grades
            data['Span'].visible = False
            data['Label'].visible = False

            # Disable the slider
            data['Slider'].disabled = True

    # Set the MGPA in the title
    plot.title.text = f'{coursetitle}, MGPA:{round(mgpa, 2)}'


def enable_disable_grade(attr, old, new, grade=None):
    """
    Callback function for the checkboxes. It updates the `grades_data` and
    then the plot.
    """
    if 0 in new:
        grades_data[grade]['Enabled'] = True
    else:
        grades_data[grade]['Enabled'] = False
    
    # Finally, update the plot
    update_plot()


def update_grade_cutoff(attr, old, new, grade=None):
    """
    Update the cut-off value in `grades_data` for the specified grade.
    Make all other grades consistent with this new cut-off. Finally,
    update the plot.
    """
    cutoff = new

    # Set the cutoff value in the data structure
    grades_data[grade]['CutOff'] = cutoff

    # Check and update the cut-off values for the higher grades
    # We will take advantage of the alphabetical ordering of the grades
    # 'A' > 'A-' > 'B' > 'B-' > 'C' > 'C-' > 'D' > 'E'
    grades = list(grades_data.keys())

    # First we will traverse the `grades_data` dictionary in the usual
    # sequence.
    highercutoff = cutoff
    for g in dropwhile(lambda x: x != grade, grades):
        if g == grade:
            continue

        lowercutoff = grades_data[g]['CutOff']
        if highercutoff < lowercutoff:
            # Inconsistent lower cut-off detected. Fix it.
            lowercutoff = max(0, highercutoff - 2)
            grades_data[g]['CutOff'] = lowercutoff

        # Update the lowercutoff for the next loop iteration
        highercutoff = lowercutoff

    # Now we will traverse the `grades_data` dictionary in reverse sequence.
    lowercutoff = cutoff
    for g in dropwhile(lambda x: x != grade, reversed(grades)):
        if g == grade:
            continue

        highercutoff = grades_data[g]['CutOff']
        if highercutoff < lowercutoff:
            # Inconsistent higher cut-off detected. Fix it.
            highercutoff = min(maxmarks, lowercutoff + 2)
            grades_data[g]['CutOff'] = highercutoff

        # Update the lowercutoff for the next loop iteration
        lowercutoff = highercutoff

    # By now, cut-offs for all the grades (enabled or disabled) should be
    # consistent. So now we can update the plot.
    update_plot()


# Assign CheckBoxGroup callbacks
a_checkbox.on_change("active", partial(enable_disable_grade, grade="A"))
am_checkbox.on_change("active", partial(enable_disable_grade, grade="A-"))
b_checkbox.on_change("active", partial(enable_disable_grade, grade="B"))
bm_checkbox.on_change("active", partial(enable_disable_grade, grade="B-"))
c_checkbox.on_change("active", partial(enable_disable_grade, grade="C"))
cm_checkbox.on_change("active", partial(enable_disable_grade, grade="C-"))
d_checkbox.on_change("active", partial(enable_disable_grade, grade="D"))
e_checkbox.on_change("active", partial(enable_disable_grade, grade="E"))

# Assign Slider callbacks
a_slider.on_change("value", partial(update_grade_cutoff, grade='A'))
am_slider.on_change("value", partial(update_grade_cutoff, grade='A-'))
b_slider.on_change("value", partial(update_grade_cutoff, grade='B'))
bm_slider.on_change("value", partial(update_grade_cutoff, grade='B-'))
c_slider.on_change("value", partial(update_grade_cutoff, grade='C'))
cm_slider.on_change("value", partial(update_grade_cutoff, grade='C-'))
d_slider.on_change("value", partial(update_grade_cutoff, grade='D'))
e_slider.on_change("value", partial(update_grade_cutoff, grade='E'))

# Add some introductory text
desc = Div(text=open(f"{appdir}/description.html").read())

# Arrange all the controls nicely
layout = column(desc, row(plot, column(a_row, am_row, b_row, bm_row, c_row,
                                       cm_row, d_row, e_row)))

# Initialization of the plot
update_plot()

# Set the title of the app and add the plot and controls to the document
curdoc().title = 'BITS Pilani Grading App'
curdoc().add_root(layout)