#!/bin/bash

JAVAC="ecj -5" # use eclipse java compiler

cd $(dirname "$0")
scriptpath=$PWD
logfile=$scriptpath/transform.log

rm $logfile

transform() {
    local src=$1
    echo "- transforming $src ..."
    src=${src%.java}
    local adir=$(dirname $src)/aterm # dir containing all intermediate aterm output
    local adst=$adir/$(basename $src)
    mkdir -p $adir
    local dst=$(dirname $src)/$(basename $src).py # where py goes
    
    #parse
    $scriptpath/../tools/parse-java --preserve-comments -i $src.java  > $adst.aterm
    
    #do python conversions
    cat $adst.aterm | $scriptpath/j2py.py > $adst.j2py 2>&1 #
    
    #transform ast -> python
    cat $adst.j2py | $scriptpath/../tools/java2py > $dst    

    # make nice intermediate outputs
    cat $adst.aterm | pp-aterm > $adst.aterm.pp
    cat $adst.j2py  | pp-aterm > $adst.j2py.pp

}


compile_and_run() {

    #compile java
    echo "- compiling java $1 ..."
    $JAVAC $1
    local path=$(dirname $1)
    local class=$(basename ${1%.java})
   
    #run java
    echo "- running java ... "
    pushd $path > /dev/null
    java $class > $class.java.run
    
    #run python
    echo -n "- running python ... "
    local dst=$class.py
    $scriptpath/run.py $dst  2>&1  > $dst.run 

    #compare output
    ( diff $class.java.run $dst.run && echo "OK" ) || 
      ( (echo "Output differs: $1" >> $logfile) && ( echo "Error") \
        && (diff $class.java.run $dst.run >> $logfile))
    popd > /dev/null
}


for src in $(find test/java2python -iname "*.java" | sort ); do
    echo "## $src ###################################"
    echo "## $src ###################################" >> $logfile

    transform $src
    compile_and_run $src
    echo
    echo 
done


