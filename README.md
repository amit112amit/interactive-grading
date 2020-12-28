# interactive-grading
A Bokeh dashboard and a Jupyter notebook for interactively deciding grades of students.

## Bokeh Dashboard
1. It also needs a `course_details.json` file containing name of the course, maximum marks and a string containing path to an Excel sheet.
2. The Excel sheet that has a column named `Total`. The marks in this column should be integers.
3. Run this using `bokeh serve --show gradeapp`

## Jupyter Notebook
1. A much simpler way for interactive histogram plotting for grades is to use a Jupyter Notebook.
2. You can set the Excel file location, course title and maximum marks in one of the cells.
3. You can enter the grade cut-offs in another cell.
4. Run the subsequent cells to plot a histogram with grade cut-offs marked.
