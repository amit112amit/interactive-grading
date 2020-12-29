from pathlib import Path
from functools import partial
from itertools import dropwhile

from bokeh.layouts import column, row
from bokeh.models import (Button, CheckboxGroup, ColumnDataSource, Div, FileInput,
                          HoverTool, Label, Slider, Span, Spinner, TextInput)
from bokeh.plotting import curdoc, figure

from .helpers import get_marks_stats, prepare_histogram_data_source

# The "global" variables
course_details = {'title': "BITS FXYZ Dummy Course", "maxmarks": 100,
                  'total_students': 100, 'average_marks': 50}
hist_source = ColumnDataSource(
    data=dict(top=[], left=[], right=[], bin_value=[]))

# Make the figure
plot = figure(sizing_mode='scale_both', tools=['save'],
              x_range=(0, course_details['maxmarks']), y_range=(0, 10))
plot.xaxis.axis_label = "Score"
plot.yaxis.axis_label = "Count"

# Create a File Picker that accepts only Excel files.
fileinput = FileInput(accept='.xlsx', multiple=False, align=('end', 'end'))

# Create a TextInput for course title
coursetitleinput = TextInput(
    title='Course Title', placeholder='BITS FXYZ Dummy Course')

# Create a Spinner for maximum marks
maxmarksinput = Spinner(title='Maximum Marks', low=100,
                        high=300, step=100, value=100)

# Button to load histogram
button = Button(label="Load", button_type='primary', align=('end', 'end'))

# Create the tooltip
hovertool = HoverTool(tooltips=[("Score", "@bin_value"),
                                ("Count", "@top")])
plot.add_tools(hovertool)

# Create the base histogram
plot.quad(source=hist_source, top='top', bottom=0, left='left', right='right')

# Add the average marker
average_marker = Span(location=course_details['average_marks'], dimension='height', line_color='red',
                      line_dash='dashed', line_width=3)
plot.add_layout(average_marker)

# Store maximum marks for easy access
maxmarks = course_details['maxmarks']

# Create a Span for each grade
a_span = Span(location=int(0.8 * maxmarks), dimension='height',
              line_color='green', line_width=3)
am_span = Span(location=int(0.7 * maxmarks), dimension='height', visible=False,
               line_color='green', line_width=3)
b_span = Span(location=int(0.6 * maxmarks), dimension='height',
              line_color='green', line_width=3)
bm_span = Span(location=int(0.5 * maxmarks), dimension='height', visible=False,
               line_color='green', line_width=3)
c_span = Span(location=int(0.4 * maxmarks), dimension='height',
              line_color='green', line_width=3)
cm_span = Span(location=int(0.3 * maxmarks), dimension='height', visible=False,
               line_color='green', line_width=3)
d_span = Span(location=int(0.2 * maxmarks), dimension='height',
              line_color='green', line_width=3)
e_span = Span(location=int(0.1 * maxmarks), dimension='height', visible=False,
              line_color='green', line_width=3)

# Create a Label for each grade
a_label = Label(x=int(0.8 * maxmarks), y=9, text=f"A: 0")
am_label = Label(x=int(0.7 * maxmarks), y=9, text=f"A-: 0", visible=False)
b_label = Label(x=int(0.6 * maxmarks), y=9, text=f"B: 0")
bm_label = Label(x=int(0.5 * maxmarks), y=9, text=f"B-: 0", visible=False)
c_label = Label(x=int(0.4 * maxmarks), y=9, text=f"C: 0")
cm_label = Label(x=int(0.3 * maxmarks), y=9, text=f"C-: 0", visible=False)
d_label = Label(x=int(0.2 * maxmarks), y=9, text=f"D: 0")
e_label = Label(x=int(0.1 * maxmarks), y=9, text=f"E: 0", visible=False)

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
        "CutOff": int(0.8 * maxmarks),
        "Slider": a_slider,
        "Span": a_span,
        "Label": a_label
    },
    'A-': {
        "Enabled": False,
        "Weight": 9,
        "CutOff": int(0.7 * maxmarks),
        "Slider": am_slider,
        "Span": am_span,
        "Label": am_label
    },
    'B': {
        "Enabled": True,
        "Weight": 8,
        "CutOff": int(0.6 * maxmarks),
        "Slider": b_slider,
        "Span": b_span,
        "Label": b_label
    },
    'B-': {
        "Enabled": False,
        "Weight": 7,
        "CutOff": int(0.5 * maxmarks),
        "Slider": bm_slider,
        "Span": bm_span,
        "Label": bm_label
    },
    'C': {
        "Enabled": True,
        "Weight": 6,
        "CutOff": int(0.4 * maxmarks),
        "Slider": c_slider,
        "Span": c_span,
        "Label": c_label
    },
    'C-': {
        "Enabled": False,
        "Weight": 5,
        "CutOff": int(0.3 * maxmarks),
        "Slider": cm_slider,
        "Span": cm_span,
        "Label": cm_label
    },
    'D': {
        "Enabled": True,
        "Weight": 4,
        "CutOff": int(0.2 * maxmarks),
        "Slider": d_slider,
        "Span": d_span,
        "Label": d_label
    },
    'E': {
        "Enabled": False,
        "Weight": 2,
        "CutOff": int(0.1 * maxmarks),
        "Slider": e_slider,
        "Span": e_span,
        "Label": e_label
    },
}


def load_course_data():
    """
    1. Process the Excel sheet.
    2. Set the course title.
    3. Set the maximum marks.
    4. Update plot range and title
    """
    course_details['maxmarks'] = maxmarksinput.value
    course_details['title'] = coursetitleinput.value
    excelfilecontents = fileinput.value
    hist_data = prepare_histogram_data_source(excelfilecontents, course_details['maxmarks'])

    # Get some stats
    total_students, average_marks = get_marks_stats(excelfilecontents)
    course_details['total_students'] = total_students
    course_details['average_marks'] = average_marks

    # Update the histogram column source
    hist_source.data = hist_data

    # Get the lowest score in the class
    for first_score, h in enumerate(hist_data['top']):
        if h > 0:
            break

    # Set the ranges
    xmin = hist_data['bin_value'][first_score] - 2
    ymax = max(hist_data['top']) + 2

    # Update the label locations
    a_label.y = ymax - 1
    am_label.y = ymax - 1
    b_label.y = ymax - 1
    bm_label.y = ymax - 1
    c_label.y = ymax - 1
    cm_label.y = ymax - 1
    d_label.y = ymax - 1
    e_label.y = ymax - 1

    # Update plot ranges, title and the average marker
    plot.title.text = f"{course_details['title']} MGPA: 0.0"
    plot.x_range.start = xmin
    plot.x_range.end = course_details['maxmarks']
    plot.y_range.end = ymax
    average_marker.location = average_marks

    # Update the slider limits
    a_slider.end = course_details['maxmarks']
    am_slider.end = course_details['maxmarks']
    b_slider.end = course_details['maxmarks']
    bm_slider.end = course_details['maxmarks']
    c_slider.end = course_details['maxmarks']
    cm_slider.end = course_details['maxmarks']
    d_slider.end = course_details['maxmarks']
    e_slider.end = course_details['maxmarks']

    # Update grade markers
    update_plot()


# Add callback to the button
button.on_click(load_course_data)


def calculate_stats():
    """
    Calculate count and MGPA based on the current state of `grades_data`.
    """
    counts = {}
    mgpa = 0.0
    upperlimit = course_details['maxmarks'] + 1
    for grade, data in grades_data.items():
        if not data['Enabled']:
            continue

        # Count the number of students from histogram data
        lowerlimit = data['CutOff']
        count = sum(hist_source.data['top'][lowerlimit: upperlimit])

        # Update MGPA
        mgpa += count * data['Weight']

        # Store the count
        counts[grade] = count

        # Update the upperlimit for the next grade
        upperlimit = lowerlimit

    # Normalize the MGPA
    mgpa /= course_details['total_students']

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
            data['Slider'].value = data['CutOff']
        else:
            # Turn off the disabled grades
            data['Span'].visible = False
            data['Label'].visible = False

            # Disable the slider
            data['Slider'].disabled = True

    # Set the MGPA in the title
    plot.title.text = f'{course_details["title"]} MGPA:{round(mgpa, 2)}'


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
            highercutoff = min(course_details['maxmarks'], lowercutoff + 2)
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
appdir = Path(__file__).parent
desc = Div(text=open(f"{appdir}/description.html").read())

# Arrange all the controls nicely
layout = column(desc, row(coursetitleinput, maxmarksinput, fileinput, button),
                row(plot, column(a_row, am_row, b_row, bm_row, c_row, cm_row,
                                 d_row, e_row, align=('end', 'center'))))

# Initialization of the plot
update_plot()

# Set the title of the app and add the plot and controls to the document
curdoc().title = 'BITS Pilani Grading App'
curdoc().add_root(layout)
