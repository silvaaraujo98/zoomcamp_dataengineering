## Module 2 Homework

ATTENTION: At the end of the submission form, you will be required to include a link to your GitHub repository or other public code-hosting site. This repository should contain your code for solving the homework. If your solution includes code that is not in file format, please include these directly in the README file of your repository.

> In case you don't get one option exactly, select the closest one 

For the homework, we'll be working with the _green_ taxi dataset located here:

`https://github.com/DataTalksClub/nyc-tlc-data/releases/tag/green/download`

To get a `wget`-able link, use this prefix (note that the link itself gives 404):

`https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/`

### Assignment

So far in the course, we processed data for the year 2019 and 2020. Your task is to extend the existing flows to include data for the year 2021.

![homework datasets](../../../02-workflow-orchestration/images/homework.png)

As a hint, Kestra makes that process really easy:
1. You can leverage the backfill functionality in the [scheduled flow](../../../02-workflow-orchestration/flows/09_gcp_taxi_scheduled.yaml) to backfill the data for the year 2021. Just make sure to select the time period for which data exists i.e. from `2021-01-01` to `2021-07-31`. Also, make sure to do the same for both `yellow` and `green` taxi data (select the right service in the `taxi` input).
2. Alternatively, run the flow manually for each of the seven months of 2021 for both `yellow` and `green` taxi data. Challenge for you: find out how to loop over the combination of Year-Month and `taxi`-type using `ForEach` task which triggers the flow for each combination using a `Subflow` task.

### Quiz Questions

Complete the quiz shown below. It's a set of 6 multiple-choice questions to test your understanding of workflow orchestration, Kestra, and ETL pipelines.

1) Within the execution for `Yellow` Taxi data for the year `2020` and month `12`: what is the uncompressed file size (i.e. the output file `yellow_tripdata_2020-12.csv` of the `extract` task)?
- [ ] 128.3 MiB
- [x] <span style="color:green"> **134.5 MiB** </span>
- [ ] 364.7 MiB
- [ ] 692.6 MiB

**Solution:**

    I inserted two tasks.

    The first one, get_size, retrieves the file, calculates the size, and stores it in a .txt file.

    The second one, log_result, displays the value stored in the .txt file within the logs.

```yaml
id: 02_homework
namespace: zoomcamp
description: |
  The CSV Data used in the course: https://github.com/DataTalksClub/nyc-tlc-data/releases

inputs:
  - id: taxi
    type: SELECT
    displayName: Select taxi type
    values: [yellow, green]
    defaults: green

  - id: year
    type: SELECT
    displayName: Select year
    values: ["2019", "2020","2021"]
    defaults: "2019"

  - id: month
    type: SELECT
    displayName: Select month
    values: ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
    defaults: "01"

variables:
  file: "{{inputs.taxi}}_tripdata_{{inputs.year}}-{{inputs.month}}.csv"
  staging_table: "public.{{inputs.taxi}}_tripdata_staging"
  table: "public.{{inputs.taxi}}_tripdata"
  data: "{{outputs.extract.outputFiles[inputs.taxi ~ '_tripdata_' ~ inputs.year ~ '-' ~ inputs.month ~ '.csv']}}"

tasks:
  - id: set_label
    type: io.kestra.plugin.core.execution.Labels
    labels:
      file: "{{render(vars.file)}}"
      taxi: "{{inputs.taxi}}"

  - id: extract
    type: io.kestra.plugin.scripts.shell.Commands
    outputFiles:
      - "*.csv"
    taskRunner:
      type: io.kestra.plugin.core.runner.Process
    commands:
      - wget -qO- https://github.com/DataTalksClub/nyc-tlc-data/releases/download/{{inputs.taxi}}/{{render(vars.file)}}.gz | gunzip > {{render(vars.file)}}

  - id: get_size
    type: io.kestra.plugin.scripts.shell.Commands
    commands:
      - stat -c%s {{render(vars['data'])}} > size.txt
    outputFiles:
      - size.txt


  - id: log_result
    type: io.kestra.plugin.core.log.Log
    message: "The captured size is {{ read(outputs.get_size.outputFiles['size.txt'])}} bytes."
```


2) What is the rendered value of the variable `file` when the inputs `taxi` is set to `green`, `year` is set to `2020`, and `month` is set to `04` during execution?
- [ ] `{{inputs.taxi}}_tripdata_{{inputs.year}}-{{inputs.month}}.csv` 
- [x] <span style="color:green"> **`green_tripdata_2020-04.csv`** </span>
- [ ] `green_tripdata_04_2020.csv`
- [ ] `green_tripdata_2020.csv`

**Solution:**
- I performed some reverse engineering and built the variable using the inputs.

- To be certain, I ran the workflow with those inputs and retrieved the file "green_tripdata_2020-04.csv" from the output of the extract task.

**Notes:**
- The next three questions are based on the following flow:
```yaml
id: test_for_each
namespace: zoomcamp
NYC Taxi Data Kestra Pipeline. An iterative workflow that utilizes ForEach to download .csv.gz files, processes them within a container using Pandas to extract metrics (row count), and executes UPSERT queries in PostgreSQL to maintain a file processing history.

variables:
  # We use single quotes so Kestra treats this as a literal string 
  # and doesn't try to find 'month' yet.
  file_template: "{{ inputs.taxi }}_tripdata_{{ inputs.year }}-{{ taskrun.value}}.csv"
  table: "public.{{inputs.taxi}}_tripdata"
  staging_table: "public.{{inputs.taxi}}_tripdata_staging"
  data: "{{ outputs.extract[taskrun.value].outputFiles[render(vars.file_template)] }}"

inputs:
  - id: taxi
    type: SELECT
    values: [yellow, green]
    defaults: green
  - id: year
    type: SELECT
    values: ["2019", "2020", "2021"]
    defaults: "2019"

tasks:
  - id: iterating_over_months
    type: io.kestra.plugin.core.flow.ForEach
    values: ["01","02","03","04","05","06","07","08","09","10","11","12"]
    tasks:
      - id: log_file
        type: io.kestra.plugin.core.log.Log
        # We manually pass 'taskrun.value' into the 'month' placeholder
        message: "File is: {{ render(vars.file_template) }}"

      - id: extract
        type: io.kestra.plugin.scripts.shell.Commands
        outputFiles:
        - "*.csv"
        taskRunner:
          type: io.kestra.plugin.core.runner.Process 
        commands:
          - wget -qO- https://github.com/DataTalksClub/nyc-tlc-data/releases/download/{{inputs.taxi}}/{{render(vars.file_template)}}.gz | gunzip >  "{{render(vars.file_template)}}"
      - id: check_file
        type: io.kestra.plugin.core.log.Log
        message: "O arquivo desta iteração é: {{ outputs.extract[taskrun.value].outputFiles }}"

      - id: read_rows
        type: io.kestra.plugin.scripts.python.Script
        dependencies:
          - pandas
          - kestra
          - numpy
        inputFiles: 
          data.csv: "{{vars.data}}"
        script: |
          import pandas as pd
          from kestra import Kestra
          df = pd.read_csv("data.csv")
          length = len(df)
          outputs = {
          'length': length}
          Kestra.outputs(outputs)

      - id: create_table_in_postgres
        type: io.kestra.plugin.jdbc.postgresql.Queries
        sql: |
         CREATE TABLE IF NOT EXISTS public.metadados_arquivos (
             nome_arquivo VARCHAR(255) UNIQUE NOT NULL,
             quantidade_linhas INTEGER
             );

      - id: check_log
        type: io.kestra.plugin.core.log.Log
        message: "{{outputs.read_rows[taskrun.value]}}"

      - id: insert_data_in_postgres
        type: io.kestra.plugin.jdbc.postgresql.Queries
        sql: |
           INSERT INTO metadados_arquivos (nome_arquivo, quantidade_linhas)
           VALUES ('{{ render(vars.file_template) }}', {{outputs.read_rows[taskrun.value].vars.length}})
           ON CONFLICT (nome_arquivo) 
           DO NOTHING
           ;
        



pluginDefaults:
  - type: io.kestra.plugin.jdbc.postgresql
    values:
      url: jdbc:postgresql://pgdatabase:5432/ny_taxi
      username: root
      password: root

```

3) How many rows are there for the `Yellow` Taxi data for all CSV files in the year 2020?
- [ ] 13,537.299
- [x] <span style="color:green"> **24,648,499** </span>
- [ ] 18,324,219
- [ ] 29,430,127

**Solution**:
- After building the flow, I wrote the following query:
```sql
SELECT 
	SUM(quantidade_linhas) 
FROM 
  public.metadados_arquivos 
WHERE 
  nome_arquivo ~ '^yellow_tripdata_2020-\d{2}\.csv$';
```

4) How many rows are there for the `Green` Taxi data for all CSV files in the year 2020?
- [ ] 5,327,301
- [ ] 936,199
- [x] <span style="color:green"> **1,734,051** </span>
- [ ] 1,342,034
**Solution**:
- After building the flow, I wrote the following query:
```sql
SELECT 
	SUM(quantidade_linhas) 
FROM 
  public.metadados_arquivos 
WHERE 
  nome_arquivo ~ '^green_tripdata_2020-\d{2}\.csv$';
```

5) How many rows are there for the `Yellow` Taxi data for the March 2021 CSV file?
- [ ] 1,428,092
- [ ] 706,911
- [x] <span style="color:green"> **1,925,152** </span>
- [ ] 2,561,031
**Solution**:
- After building the flow, I wrote the following query:
```sql
SELECT 
	quantidade_linhas
FROM
	metadados_arquivos
WHERE
	nome_arquivo = 'yellow_tripdata_2021-03.csv'
```

6) How would you configure the timezone to New York in a Schedule trigger?
- [ ] Add a `timezone` property set to `EST` in the `Schedule` trigger configuration  
- [x] <span style="color:green"> **Add a `timezone` property set to `America/New_York` in the `Schedule` trigger configuration** </span>
- [ ]Add a `timezone` property set to `UTC-5` in the `Schedule` trigger configuration
- [ ] Add a `location` property set to `New_York` in the `Schedule` trigger configuration  

## Submitting the solutions

* Form for submitting: https://courses.datatalks.club/de-zoomcamp-2026/homework/hw2
* Check the link above to see the due date

## Solution

Will be added after the due date


## Learning in Public

We encourage everyone to share what they learned. This is called "learning in public".

Read more about the benefits [here](https://alexeyondata.substack.com/p/benefits-of-learning-in-public-and).

### Example post for LinkedIn

```
🚀 Week 2 of Data Engineering Zoomcamp by @DataTalksClub and @Will Russell complete!

Just finished Module 2 - Workflow Orchestration with @Kestra. Learned how to:

✅ Orchestrate data pipelines with Kestra flows
✅ Use variables and expressions for dynamic workflows
✅ Implement backfill for historical data
✅ Schedule workflows with timezone support
✅ Process NYC taxi data (Yellow & Green) for 2019-2021

Built ETL pipelines that extract, transform, and load taxi trip data automatically!

Thanks to the @Kestra team for the great orchestration tool!

Here's my homework solution: <LINK>

Following along with this amazing free course - who else is learning data engineering?

You can sign up here: https://github.com/DataTalksClub/data-engineering-zoomcamp/
```

### Example post for Twitter/X

```
Module 2 of DE Zoomcamp by @DataTalksClub @wrussell1999 done!

- @kestra_io workflow orchestration
- ETL pipelines for taxi data
- Backfill & scheduling
- Variables & dynamic flows

My solution: <LINK>

Join me here: https://github.com/DataTalksClub/data-engineering-zoomcamp/
```
