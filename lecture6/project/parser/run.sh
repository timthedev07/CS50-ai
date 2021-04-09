i=1

while [ $i -lt 10 ]
do
  python3 parser.py sentences/$i.txt
  let i+=1
done