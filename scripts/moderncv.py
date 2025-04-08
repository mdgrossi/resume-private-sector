from IPython.display import Markdown, Latex
import pandas as pd
import re

# =============================================================================
#
# CLASSES
#
# Used with custom tribble function modeled off of R's tibble::tribble. Each
# class has a method to generate a PDF (LaTeX) output and HTML for a website.
#
# Limitation: Neither LaTeX nor HTML output renders in docx (Microsoft Word).
#
# =============================================================================

class Entry():
    
    def __init__(self, columns, *data):
        """Row-wise dataframe construction, comparabe to
        R's `tibble::tribble` function.
        
        ARGUMENTS
        ---------
        columns: list of column names for the Pandas dataframe
        ~dada: comma-separated values with which to populate the dataframe. Can  be
        any dtype and any number of items but must be a multiple of `len(columns)`.
        
        RETJRNS
        -------
        Pandas dataframe with columns `columns` filled row-wise with `data`
        """
        self.entry = self.tribble(columns, *data)

    def tribble(self, columns, *data):
        """Row-wise dataframe construction, comparabe to R's `tibble::tribble`
        function.
        
        ARGUMENTS
        ---------
        columns: list of column names for the Pandas dataframe
        ~dada: comma-separated values with which to populate the dataframe. Can  be
        any dtype and any number of items but must be a multiple of `len(columns)`.
        
        RETJRNS
        -------
        Pandas dataframe with columns `columns` filled row-wise with `data`
        """
        return pd.DataFrame( 
            data=list(zip(*[iter(data)]*len(columns))),
            columns=columns
        )

    def delatexify(self, string):
        """Remove LaTeX formatting for `html` and `docx` rendering
        
        ARGUMENTS
        ---------
        string: string of characters containing LaTeX commands such as
        '\\textbf(...)'
        
        RETURNS
        -------
        Clean character string without LatTeX formatting commands
        """
        # Remove commands
        string = re.sub("\\\\v.*?\}", "", string, flags=re.DOTALL).strip()
        string = re.sub("\\\\h.*?\}", "", string, flags=re.DOTALL).strip()
        string = string.replace("\\textit{e.g.}", "e.g.")
        
        # Remove escape characters
        string = string.replace("\\", "").strip()
        
        # Replace * with bullets
        string = string.replace("*", "<br>\u2022")
        
        # Replace other odds and ends
        string = string\
            .replace("$sim$", "~")\
            .replace("$>$", ">")
        
        return string

class Skills(Entry):
        
    def __init__(self, columns, *data):
        super().__init__(columns, *data)
    
    def to_html(self):

        html_col1 = '- {{< iconify icon-park analysis >}} **Data Analysis** [(10+ yrs.)]{style="color: grey"}\n' +\
            '- {{< iconify devicon plotly >}} **Data Science** [(8 yrs)]{style="color: grey"}\n' +\
            '- {{< iconify fluent data-usage-sparkle-20-filled >}} **Data Governance** [(4 yrs.)]{style="color: grey"}\n' +\
            '- {{< iconify devicon python >}} **Python** [(9 yrs.)]{style="color: grey"}\n' +\
            '- {{< iconify devicon rstudio >}} **R** [(3 yrs.)]{style="color: grey"}\n' +\
            '- {{< iconify ri cloud-fill >}} **Cloud** (AWS, GCP) [(1 yr. each)]{style="color: grey"}\n'
        html_col2 =  '- {{< iconify carbon machine-learning-model >}} **Machine Learning** [(8 yrs.)]{style="color: grey"}\n' +\
            '- {{< iconify mdi github >}} **Git** [(9 yrs.)]{style="color: grey"}\n' +\
            '- {{< iconify skill-icons docker >}} **Docker** [(3 yrs.)]{style="color: grey"}\n' +\
            '- {{< iconify skill-icons latex-dark >}} **LaTeX** [(10+ yrs.)]{style="color: grey"}\n' +\
            '- {{< iconify logos jupyter >}} **Jupyter** [(9 yrs.)]{style="color: grey"}\n' +\
            '- {{< iconify simple-icons quarto >}} **Quarto** [(2 yrs.)]{style="color: grey"}\n'

        display(Markdown(':::: {.columns layout-ncols="2"}'))
        
        display(Markdown(':::{.column}'))
        
        display(Markdown(html_col1))
        
        display(Markdown(':::'))
        
        display(Markdown(':::{.column}'))
        
        display(Markdown(html_col2))
        
        display(Markdown(':::'))
        
        display(Markdown('::::'))
        
        
    def to_pdf(self, skill, years, scale, ncol):
        
        # Get entry data
        tbl = self.entry.copy()
        
        # Create skill bars
        colscall = f"\\vspace{{1em}}\\begin{{multicols}}{{{ncol}}}"
        command_start = "\\cvskillbar"
        colsend = "\\end{multicols}"
        res = [f"{command_start}{{{s}}}{{{y}}}{{{c}}}\n" for s,y,c in zip(tbl[skill], tbl[years], tbl[scale])]

        res.insert(0, colscall)
        res.append(colsend)

        # Display the skills
        for s in res: display(Latex(s))

class Softskills(Entry):
        
    def __init__(self, columns, *data):
        super().__init__(columns, *data)
    
    def to_html(self, skills):
        
        # Get entry data
        tbl = self.entry.copy()
        
        # Create skill list
        [print(f'- **Soft Skiils:** {s}') for s in tbl[skills]]
    
    def to_pdf(self, skills):
        
        # Get entry data
        tbl = self.entry.copy()
        
        # Create skill list
        command_start = '\\cvitem{\\textcolor{color1}{$\\triangleright$} \\hspace{0.2em} Soft Skills}'
        command_end = '\\vspace{\\cvspace}'
    
        # Create list
        print(command_start + f'{{tbl[skills]}}' + command_end)

class Education(Entry):
    
    def __init__(self, columns, *data):
        super().__init__(columns, *data)
    
    def to_html(self, degree, institution, where, date, award, minor):
    
        # De-LaTeXify
        tbl = self.entry.copy()
        tbl = tbl.map(self.delatexify)
            
        # Create tables, one per job
        for _, school in tbl.iterrows():
            # Building blocks
            table_start = '<table class = "mytable">\n<tbody>\n'
            table_end = '<tbody>\n<table>\n'
            degreerow = f'<tr>\n<th scope="row"><b>{school[degree]}</b></th>\n<td align="right"><b>{school[date]}</b></td>\n</tr>\n'
            if len(school[award]) > 2:
                schoolrow = f'<tr>\n<th scope="row"><i>{school[institution]}, {school[award]}</i></th>\n<td align="right"><i>{school[where]}</i></td>\n</tr>\n'
            else:
                schoolrow = f'<tr>\n<th scope="row"><i>{school[institution]}</i></th>\n<td align="right"><i>{school[where]}</i></td>\n</tr>\n'
            if len(school[minor]) > 2:
                extrarow = f'<tr>\n<th scope="row" colspan="2">Minor in {school[minor]}</th>\n</tr>\n'
            else:
                extrarow = ''

            # Assemble
            html_table = table_start + degreerow + schoolrow + extrarow + table_end
            print(html_table)
    
    def to_pdf(self, degree, institution, where, date, award, minor):
        
        # Get entry data
        tbl = self.entry.copy()

        # Create LaTeX moderncv `\cventry`` call
        def create_str(tbl, degree, institution, where, date, award, minor):
            """Create LaTeX moderncv `\cventry` call"""
            command_start = '\\cventry'
            command_end = '\\vspace{0.5em}'
            print(
                command_start + '{' + tbl[where] + '}' +\
                '{' + tbl[institution] + '}' +\
                '{' + tbl[degree] + '}' +\
                '{' + tbl[date] + '}' +\
                '{' + tbl[award] + '}' +\
                '{' + tbl[minor] + '}' +\
                command_end
            )
        
        # Replicate for all jobs
        [create_str(row, degree, institution, where, date, award, minor) for _, row in tbl.iterrows()]

class Experience(Entry):
    
    def __init__(self, columns, *data):
        super().__init__(columns, *data)
    
    def to_html(self, employer, role, dates, where, desc):
    
        # Get enrty data
        tbl = self.entry.copy()
 
        # Remove pdf page breaks
        idx = tbl.index[tbl[role] == ''].to_list()
        for i in idx:
            tbl.loc[i-1, 'details'] = \
                tbl.loc[i-1, 'details'] + '\n ' + tbl.loc[i, 'details']
        tbl.drop(idx, inplace=True)
        
        # De-LaTeXify and remove first line break
        tbl = tbl.map(self.delatexify)
        tbl[desc] = tbl[desc].apply(lambda x: x.replace('<br>', '', 1))
            
        # Create tables, one per job
        for _, job in tbl.iterrows():
            # Building blocks
            table_start = '<table class = "mytable">\n<tbody>\n'
            table_end = '<tbody>\n<table>\n'
            employerrow = f'<tr>\n<th scope="row" colspan="2"><b>{job[employer]}</b></th>\n'
            jobrow = f'<tr>\n<th scope="row"><i>{job[role]}, {job[where]}</i></th>\n<td align="right"><i>{job[dates]}</i></td>\n</tr>\n'
            descriptionrow = f'<tr>\n<th scope="row" colspan="2">{job[desc]}</th>\n</tr>\n'

            # Assemble
            html_table = table_start + employerrow + jobrow + descriptionrow + table_end
            print(html_table)
    
    def to_pdf(self, employer, role, dates, where, desc):

        # Replace * with LaTeX list items
        tbl = self.entry.copy()
        tbl[desc] = tbl[desc].apply(lambda x: x.replace('* ', '\\item '))
        
        # Create LaTeX moderncv `\cventry`` call
        def create_str(tbl, role, employer, where, dates, desc):
            """Create LaTeX moderncv `\cventry` call"""
            command_start = '\\cventry[\\cvspace]'
            command_end = '\\vspace{0.5em}'
            print(
                command_start + '{' + tbl[dates] + '}' +\
                '{' + tbl[role] + '}' +\
                '{' + tbl[employer] + '}' +\
                '{}' +\
                '{' + tbl[where] + '}' +\
                '{' + '\\vspace{0.25em}\\begin{wideitemize}' + tbl[desc] + '\\end{wideitemize}' + '}' +\
                command_end
            )
        
        # Replicate for all jobs
        [create_str(row, role, employer, where, dates, desc) for _, row in tbl.iterrows()]
        
class Awards(Entry):
    
    def __init__(self, columns, *data):
        super().__init__(columns, *data)

    def to_html(self, awards):

        # Get entry data
        tbl = self.entry.copy()
        
        # Print each award as list
        [print(f'- {a}') for a in tbl[awards]]        

    def to_pdf(self, awards):
        
        # Get entry data
        tbl = self.entry.copy()
        
        # Print for each award
        [print(f'\\cvlistitem{{a}}') for a in tbl[awards]]

# =============================================================================
#
# MARKDOWN
#
# These functions generate Markdown output that renders in both HTML (website)
# and docx (Microsoft Word), although formatting is compromised in the latter.
# These functions are designed to be used with resume entries passed to front
# matter YAML. PDF is generated entirely using the LaTeX template, also using
# front matter YAML.
#
# =============================================================================

def list_html(items):
    list_start = "<html><ul>"
    list_end = "</ul></html>"
    key, _ = list(items[0].items())[0]
    items = "".join(f"<li>{i[key]}</li>" for i in items)
    html_list = list_start + items + list_end
    display(Markdown(html_list))

def mdlist(items):
    key, _ = list(items[0].items())[0]
    items = "".join(f"- {i[key]}\n" for i in items)
    display(Markdown(items))

def mdskills(items, ncol=2, icons=True):
    """Create a Markdown list with `ncol` columns from contents of dictionary
    `items`. If `icons = True`, each skill will be prefaced by an icon if
    if available (HTML only).
    """
    
    # Column configuration
    nskills = len(items)
    perrow = nskills//ncol
    
    # Include skill icons, if desired
    if icons:
        icon_dict = dict({
            'Data Analysis': '{{< iconify icon-park analysis >}}',
            'Data Science': '{{< iconify devicon plotly >}}',
            'Data Governance': '{{< iconify fluent data-usage-sparkle-20-filled >}}',
            'Python': '{{< iconify devicon python >}}',
            'R': '{{< iconify devicon rstudio >}}',
            'Cloud (AWS, GCP)': '{{< iconify ri cloud-fill >}}',
            'Machine Learning': '{{< iconify carbon machine-learning-model >}}',
            'Git': '{{< iconify mdi github >}}',
            'Docker': '{{< iconify skill-icons docker >}}',
            '\\LaTeX': '{{< iconify skill-icons latex-dark >}}',
            'Jupyter': '{{< iconify logos jupyter >}}',
            'Quarto': '{{< iconify simple-icons quarto >}}'
        })

        col1 = ''.join(f'- {icon_dict[s["skill"]]} **{s["skill"]}** [({s["years"]})]{{style="color: grey"}}\n' for i,s in enumerate(items) if i < perrow)
        col2 = ''.join(f'- {icon_dict[s["skill"]]} **{s["skill"]}** [({s["years"]})]{{style="color: grey"}}\n' for i,s in enumerate(items) if i >= perrow)
    
    else:
        
        col1 = ''.join(f'- **{s["skill"]}** [({s["years"]})]{{style="color: grey"}}\n' for i,s in enumerate(items) if i < perrow)
        col2 = ''.join(f'- **{s["skill"]}** [({s["years"]})]{{style="color: grey"}}\n' for i,s in enumerate(items) if i >= perrow)

    # De-LaTeXify
    col1 = col1.replace('\\', '')
    col2 = col2.replace('\\', '')

    # Generate table
    display(Markdown(':::: {.columns layout-ncols="2"}'))
    display(Markdown(':::{.column}'))    
    display(Markdown(col1))
    display(Markdown(':::'))
    display(Markdown(':::{.column}'))
    display(Markdown(col2))
    display(Markdown(':::'))
    display(Markdown('::::'))

def mdeducation_table(items):
    abbr = dict({
        'Bachelor of Science': 'B.S.',
        'Master of Science': 'M.S.',
        'Doctor of Philosophy': 'Ph.D.'
    })

    def md_table(entry):
        display(Markdown(f'|<br>**{abbr[entry["degree"]]}, {entry["major"]}** | <br> **{entry["date"]}** |'))
        if 'extra' in entry.keys():
            display(Markdown(f'| *{entry["institution"]}, {entry["extra"]}* | *{entry["location"]}* |'))
        else:
            display(Markdown(f'| *{entry["institution"]}* | *{entry["location"]}* |'))
        if 'minor' in entry.keys():
            display(Markdown(f'| Minor in {entry["minor"]} |  |'))
        # display(Markdown(' '))
    
    display(Markdown('| | |'))
    display(Markdown('| :-------------- | ---: |'))
    for item in items:
        md_table(entry=item)

def mdeducation(items):
    abbr = dict({
        'Bachelor of Science': 'B.S.',
        'Master of Science': 'M.S.',
        'Doctor of Philosophy': 'Ph.D.'
    })

    for item in items:
        display(Markdown(f'**{abbr[item["degree"]]}, {item["major"]}**  '))
        if 'extra' in item.keys():
            display(Markdown(f'*{item["institution"]}, {item["location"]}* ({item["extra"]})  '))
        else:
            display(Markdown(f'*{item["institution"]}, {item["location"]}*  '))
        if 'minor' in item.keys():
          display(Markdown(f'Minor in {item["minor"]}  '))
        display(Markdown(' '))

def mdexperience(items):

    # Remove pdf page breaks
    ind = [i for i,d in enumerate(items) if 'role' not in d.keys()]
    for i in ind:
        items[i-1]['details'] = items[i-1]['details'] + items[i]['details']
    items = [d for i,d in enumerate(items) if i not in ind]

    for item in items:
        # Add missing elements as placeholders
        for k in ['role', 'employer', 'where', 'dates', 'details']:
            if k not in item.keys():
                item[k] = ''

        display(Markdown('|  |  |'))
        display(Markdown('| :--- | ---: |'))
        if item['employer'] == '' and item['where'] == '':
            if 'extra' in item.keys():
                display(Markdown(f'| *{item["role"]}, {item["extra"]}* | *{item["dates"]}* |\n'.replace('****', '')))
            else:
                display(Markdown(f'| *{item["role"]}* | *{item["dates"]}* |\n'.replace('****', '')))    
        else:
            if 'extra' in item.keys():
                display(Markdown(f'| **{item["employer"]}** <br> *{item["role"]}, {item["extra"]}* | **{item["where"]}** <br> *{item["dates"]}* |\n'.replace('****', '')))
            else:
                display(Markdown(f'| **{item["employer"]}** <br> *{item["role"]}* | **{item["where"]}** <br> *{item["dates"]}* |\n'.replace('****', '')))
        display(Markdown(item["details"]))
