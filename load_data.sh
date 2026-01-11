#!/bin/env sh

sqlite3 -line benchmark.db 'drop table enum_as_string;'
sqlite3 -line benchmark.db 'drop table enum_as_int;'
sqlite3 -line benchmark.db 'drop table enum_as_fk;'
sqlite3 -line benchmark.db 'drop table color;'
sqlite3 -line benchmark.db 'drop table status;'
sqlite3 -line benchmark.db 'drop table order_type;'

for file in tables/*.sql; do
    sqlite3 benchmark.db < "$file"
done

# for file in data/*.sql; do
#     sqlite3 benchmark.db < "$file"
# done

sqlite3 benchmark.db <<EOF
.mode csv
.import --skip 1 data/enum_as_string_data.csv enum_as_string
EOF

sqlite3 benchmark.db <<EOF
.mode csv
.import --skip 1 data/enum_as_fk_data.csv enum_as_fk
EOF

sqlite3 benchmark.db <<EOF
.mode csv
.import --skip 1 data/enum_as_int_data.csv enum_as_int
EOF
