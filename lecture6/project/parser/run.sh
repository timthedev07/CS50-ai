i=1

while [ $i -lt 2 ]
do
  python3 parser.py sentences/$i.txt
  let i+=1
done