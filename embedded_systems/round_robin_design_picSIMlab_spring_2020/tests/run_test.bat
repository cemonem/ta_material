python populate_template.py %1
call mdb %1.render > %1.out 2>nul
;call mdb %1.render > %1.out

python %2 %1.out %3

rm -f %1.out %1.render
