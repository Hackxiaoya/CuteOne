#!/etc/bash


function install_eq(){
    echo "Updateing pip3..."
    pip3 install --upgrade pip
    echo "Updateing pip3 compatible"
    echo "Installation requirements..."
    pip3 install -r requirements.txt
    echo "Install requirements compatible"
}


function optimize(){
    mysql = "pgrep 'mysql'"
    #echo $mysql
    if [ 0 == $mysql ];then
        echo "mysql is not install."
        exit
    fi

    mongodb = "pgrep 'mongodb'"
    #echo $mongodb
    if [ 0 == $mongodb ];then
        echo "mongodb is not install."
        exit
    fi
}



function install_sql(){
    read -p "mysql host:" host
    if [ ! -n "$host" ];then
        echo "mysql host cannot be empty"
        install_sql
    fi
    read -p "mysql user:" mysql_user
    if [ ! -n "$mysql_user" ];then
        echo "mysql user cannot be empty"
        install_sql
    fi
    read -p "mysql pass:" mysql_pass
    if [ ! -n "$mysql_pass" ];then
        echo "mysql pass cannot be empty"
        install_sql
    fi
    read -p "mysql db name:" mysql_db
    if [ ! -n "$mysql_db" ];then
        echo "mysql db name cannot be empty"
        install_sql
    fi
    read -p "mysql db port:" mysql_port
    if [ ! -n "$mysql_port" ];then
        echo "mysql port cannot be empty"
        install_sql
    fi
    python3 install.py $host $mysql_user $mysql_pass $mysql_port $mysql_db
}



install_eq
optimize
install_sql