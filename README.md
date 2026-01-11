# SQLite enum storing benchmark

A small benchmark to see how much impact storing enums
as string has on performance.

The generated dataset is 15 million rows per table by default.
Each table having a different way of storing enum values.

- Storing enums as a string
- Storing enums via a foreign key integer
- Storing enums as a integer and do mapping in the application

### Size of each table

enum_as_fk and enum_as_int use the same dataset.

- enum_as_string: 626 MB
- enum_as_fk: 396 MB
- enum_as_int: 396 MB

Clearly showing the disadvantage of the table size being larger
when storing enums as strings for each row.

### Benchmarked on the following machine:

- CPU: AMD Ryzen 5800X3D
- Memory: 32GB of DDR4 at 2666MT/s
- Storage: Crucial MX500 2TB

## Hypothesis

My assumption is that the more complex the queries the more the string based enums will
fall behind. Foreign key based lookup will be a bit slower then integers but not a whole
lot slower.

## Result

You can lookup the exact query by name in benchmark.py.

|                          Name                         | Mean (ms) | Median (ms) | StdDev (ms) |
|-------------------------------------------------------|-----------|-------------|-------------|
|                  enum_as_string_color                 |   0.751   |    0.734    |    0.063    |
|                    enum_as_fk_color                   |   0.789   |    0.788    |    0.012    |
|                   enum_as_int_color                   |   0.650   |    0.628    |    0.058    |
|                enum_as_string_color_in                |   0.742   |    0.733    |    0.028    |
|                  enum_as_fk_color_in                  |   0.798   |    0.784    |    0.051    |
|                  enum_as_int_color_in                 |   0.643   |    0.634    |    0.040    |
|            enum_as_string_color_and_status            |   0.845   |    0.791    |    0.098    |
|              enum_as_fk_color_and_status              |   1.029   |    1.007    |    0.107    |
|              enum_as_int_color_and_status             |   1.216   |    1.214    |    0.021    |
|     enum_as_string_color_and_status_and_order_type    |   1.577   |    1.497    |    0.251    |
|       enum_as_fk_color_and_status_and_order_type      |   1.305   |    1.221    |    0.244    |
|      enum_as_int_color_and_status_and_order_type      |   0.703   |    0.703    |    0.026    |
|   enum_as_string_two_negative_status_and_order_type   |  162.908  |   162.488   |    2.653    |
|     enum_as_fk_two_negative_status_and_order_type     |   0.945   |    0.946    |    0.006    |
|     enum_as_int_two_negative_status_and_order_type    |   0.651   |    0.652    |    0.005    |
| enum_as_string_todo_in_progress_status_and_order_type |   0.764   |    0.764    |    0.006    |
|   enum_as_fk_todo_in_progress_status_and_order_type   |   0.945   |    0.945    |    0.008    |
|   enum_as_int_todo_in_progress_status_and_order_type  |   0.647   |    0.647    |    0.007    |

## Conclusion

So I was wrong, strong based lookup is not that slow and can be quicker then foreign key based
lookups.

But string based enums can be really slow (160x slower) when you can do a index lookup over the where clauses. For example: `where status != 'FAILED' and status != 'COMPLETED' and order_type = 'ONLINE'`.

But with knowledge of all other `status` values we can transform it into an `IN` query and 
the performance is back to normal again.

I know that all three tables should use the same dataset but after running the generator multiple
times and seeing how close the results are I doubt it will have much impact and is not the cause
of the 160x slow down.

## Running the benchmark

Requirements: have python and uv installed.
There is a single dependency to pretty print the output to the CLI.

1. `uv run generate_data.py`
3. `./load_data.sh`
2. `uv run benchmark.py`

Output will be in the `benchmark_results.csv` and outputted in table form in the cli.
