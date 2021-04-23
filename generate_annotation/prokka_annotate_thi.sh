for k in * 
do 
name=${k%.*}
prokka $k --outdir Annotation_prokka/"$name".prokka --prefix annot_$name; 
echo $name; 
done
