# File: simpleifelse.sh

echo "Start program"

if [[ $1 -eq 4 ]]
then
  echo "You entered $1"
else
  echo "You entered: $1, not what I was looking for."
fi

echo "End program"