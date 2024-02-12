#!/bin/bash -l
#$ -l h_rt=96:00:00
#$ -l mem=4.5G
#$ -pe mpi 80
#$ -N pso_cata
#$ -A KCL_Cedric 
#$ -P GoldLong
#$ -cwd 


module purge
module load gcc-libs/4.9.2
module load compilers/intel/2017/update1
module load mpi/intel/2017/update1/intel
module load vasp/5.4.4-18apr2017/intel-2017-update1
module load openblas/0.3.7-serial/gnu-4.9.2
module load python3/3.8

startstep=$(grep -Po '(?<=startstep=)\d+' input.dat)
maxstep=$(grep -Po '(?<=maxstep=)\d+' input.dat)
popsize=$(grep -Po '(?<=popsize=)\d+' input.dat)
command=$(grep -Po '(?<=command=).+' input.dat)
#####################################################################################################################################
gen_count=$startstep
#####################################################################################################################################

python extract_cluster_for_molucule.py
while [ $gen_count -le $maxstep ]
do
    gen_folder="gen$gen_count"
    mkdir "$gen_folder"

    if [[ $gen_count -le 1 ]]; then
        cd "$gen_folder"
        cp ../threshold.py .
        
        for ((i=1; i<=popsize; i++))
        do
            config_folder="$config$i"
            mkdir "$config_folder"
            cp -p ../substrate.poscar ../POTCAR ../cluster.poscar ../structure_create.py ../random_generate.py ../INCAR "$config_folder"
            cp -p ../init_velocity.py ../iteration_process.py ../xy_range.dat "$config_folder"
            cd "$config_folder"
            python init_velocity.py            
            python random_generate.py
            python structure_create.py
            eval $command


            while true; do
                if grep -q 'reached required accuracy' OUTCAR; then
                    echo "Required accuracy reached. Continuing program..."
                    break
                else
                    echo "Required accuracy not reached. Executing Python scripts..."
                    python init_velocity.py
                    python random_generate.py
                    python structure_create.py
                    eval $command
                fi
            done

            grep "energy  without entropy" OUTCAR | tail -1 | awk '{print $7}' >> structure.param
            cp structure.param pbest.param
            rm CHG* WAVECAR XDATCAR vasprun.xml REPORT PCDAT OSZICAR IBZKPT EIGENVAL DOSCAR POTCAR *.py *.txt PROCAR
            python iteration_process.py
            cd ..    
        done
        python threshold.py
        cd ..
        python gbest_param_finder.py
        
#####################################################################################################################################        
    else
        cd "$gen_folder"
        cp ../threshold.py .
        
        for ((i=1; i<=popsize; i++))
        do
            config_folder="$config$i"
            mkdir "$config_folder"
            gen_count_last=$((gen_count-1))
            gen_last_folder="gen$gen_count_last"
            cp ../"$gen_last_folder"/"$config_folder"/pbest.param "$config_folder"/pbest_backup.param
            cp ../"$gen_last_folder"/"$config_folder"/velocity.dat "$config_folder"/velocity_backup.dat
            cp ../"$gen_last_folder"/"$config_folder"/structure.param "$config_folder"/structure_backup.param
            cp ../"$gen_last_folder"/threshold.dat "$config_folder"/threshold_backup.dat
            cp ../gbest.param "$config_folder"/gbest_backup.param
            cp -p ../substrate.poscar ../POTCAR ../cluster.poscar ../structure_create.py ../random_generate.py ../INCAR ../init_velocity.py ../pso_v.py  "$config_folder"
            cp -p ../pso_x.py ../choose_pbest.py ../iteration_process.py ../xy_range.dat "$config_folder"
            cd "$config_folder"
            structure_num=$(tail -n 1 structure_backup.param)
            # Read the first line of numbers from threshold_backup.dat
            threshold_num=$(head -n 1 threshold_backup.dat)
            if (( $(echo "$structure_num > $threshold_num" | bc -l) )); then
                rm pbest_backup.param threshold_backup.dat velocity_backup.dat structure_backup.param gbest_backup.param
                python init_velocity.py
                python random_generate.py
                python structure_create.py
                eval $command

                while true; do
                    if grep -q 'reached required accuracy' OUTCAR; then
                        echo "Required accuracy reached. Continuing program..."
                        break
                    else
                        echo "Required accuracy not reached. Executing Python scripts..."
                        python init_velocity.py
                        python random_generate.py
                        python structure_create.py
                        eval $command
                    fi
                done

                grep "energy  without entropy" OUTCAR | tail -1 | awk '{print $7}' >> structure.param
                cp structure.param pbest.param
                rm CHG* WAVECAR XDATCAR vasprun.xml REPORT PCDAT OSZICAR IBZKPT EIGENVAL DOSCAR POTCAR *.py *.txt PROCAR
                python iteration_process.py
            else
                rm threshold_backup.dat
                python pso_v.py
                python pso_x.py
                python structure_create.py             
                eval $command

                while true; do
                    if grep -q 'reached required accuracy' OUTCAR; then
                        echo "Required accuracy reached. Continuing program..."
                        break
                    else
                        echo "Required accuracy not reached. Executing Python scripts..."
                        python init_velocity.py
                        python random_generate.py
                        python structure_create.py
                        eval $command
                    fi
                done
                
                
                grep "energy  without entropy" OUTCAR | tail -1 | awk '{print $7}' >> structure.param
                python choose_pbest.py           
                rm CHG* WAVECAR XDATCAR vasprun.xml REPORT PCDAT OSZICAR IBZKPT EIGENVAL DOSCAR POTCAR *.py *.txt PROCAR
                python iteration_process.py
            fi
            cd ..
        done
        python threshold.py
        cd ..
        python gbest_param_finder.py
    fi
    ((gen_count++))
done
