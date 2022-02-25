#!/bin/bash
s1="hi"
s2="hi"
b1="2bye"
b2="bye"
c1="car"
c2="car"
if [[ $s1 == $s2 ]] && [[ $b1 == $b2 ]] && [[ $c1 == $c2 ]]; then
  echo "It worked"
else
  echo "Not Equal"
fi
