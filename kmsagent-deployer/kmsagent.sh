#!/bin/bash
BASE_DIR=$(
    cd "$(dirname "$0")" >/dev/null 2>&1 || exit
    pwd -P
)
readonly BASE_DIR
LOG_COUNT_THRESHOLD=5
readonly LOG_COUNT_THRESHOLD
LOG_SIZE_THRESHOLD=$((20 * 1024 * 1024))
readonly LOG_SIZE_THRESHOLD

if [ -z "${ASNIBLE_CONFIG}" ]; then
    export ANSIBLE_CONFIG=$BASE_DIR/ansible.cfg
fi
if [ -z "${ASNIBLE_LOG_PATH}" ]; then
    export ANSIBLE_LOG_PATH=$BASE_DIR/kmsagent.log
fi
if [ -z "${ASNIBLE_INVENTORY}" ]; then
    export ANSIBLE_INVENTORY=$BASE_DIR/inventory_file
fi
if [ -z "${ANSIBLE_CACHE_PLUGIN_CONNECTION}" ]; then
    export ANSIBLE_CACHE_PLUGIN_CONNECTION=$BASE_DIR/facts_cache
fi

function log_error() {
    local DATE_N
    DATE_N=$(date "+%Y-%m-%d %H:%M:%S")
    local USER_N
    USER_N=$(whoami)
    local IP_N
    IP_N=$(who am i | awk '{print $NF}' | sed 's/[()]//g')
    echo "[ERROR] $*"
    echo "${DATE_N} ${USER_N}@${IP_N} [ERROR] $*" >>"${BASE_DIR}"/kmsagent.log
}

function operation_log_info() {
    local DATE_N
    DATE_N=$(date "+%Y-%m-%d %H:%M:%S")
    local USER_N
    USER_N=$(whoami)
    local IP_N
    IP_N=$(who am i | awk '{print $NF}' | sed 's/[()]//g')
    echo "${DATE_N} ${USER_N}@${IP_N} [INFO] $*" >>"${BASE_DIR}"/kmsagent_operation.log
}

function check_log() {
    if [[ ! -e $1 ]]; then
        touch "$1"
    fi
    local log_size
    log_size=$(find "$1" -exec ls -l {} \; | awk '{ print $5 }')
    if [[ ${log_size} -ge ${LOG_SIZE_THRESHOLD} ]]; then
        rotate_log "$1"
    fi
}

function rotate_log() {
    local log_list
    log_list=$(find "$1"* -exec ls {} \; | sort -r)
    for item in $log_list; do
        local suffix
        suffix=${item##*.}
        local prefix
        prefix=${item%.*}
        if [[ ${suffix} != "log" ]]; then
            if [[ ${suffix} -lt ${LOG_COUNT_THRESHOLD} ]]; then
                suffix=$((suffix + 1))
                mv -f "$item" "$prefix".$suffix
            fi
        else
            mv -f "${item}" "${item}".1
            cat /dev/null >"${item}"
        fi
    done
}

function set_permission() {
    chmod 750 "${BASE_DIR}" "${BASE_DIR}"/playbooks/ "${BASE_DIR}"/resources
    chmod 600 "${BASE_DIR}"/*.log "${BASE_DIR}"/inventory_file "${BASE_DIR}"/ansible.cfg "${BASE_DIR}"/certs.py "${BASE_DIR}"/openssl.cnf 2>/dev/null
    chmod 500 "${BASE_DIR}"/kmsagent.sh 2>/dev/null
    chmod 400 "${BASE_DIR}"/*.log.? 2>/dev/null
}

function check_inventory() {
    local pass1
    pass1=$(grep -c ansible_ssh_pass "${BASE_DIR}"/inventory_file)
    local pass2
    pass2=$(grep -c ansible_sudo_pass "${BASE_DIR}"/inventory_file)
    local pass3
    pass3=$(grep -c ansible_become_pass "${BASE_DIR}"/inventory_file)
    local pass_cnt
    pass_cnt=$((pass1 + pass2 + pass3))
    if [ ${pass_cnt} == 0 ]; then
        return
    fi
    log_error "The inventory_file contains password, please use the SSH key instead"
    return 1
}

function bootstrap() {
    if [ "$(find "${python_dir}"/bin -name "python3.[7|8|9]" 2>/dev/null)" ] && [ "$(find "${python_dir}"/bin -name "ansible")" ]; then
        export PATH=${python_dir}/bin:$PATH
        export LD_LIBRARY_PATH=${python_dir}/lib:$LD_LIBRARY_PATH
        unset PYTHONPATH
    else
        log_error "The python version is incorrect or ansible is not installed"
        return 1
    fi
}

function generate_ca_cert() {
    mkdir -p "${BASE_DIR}"/resources/cert/ && chmod 750 "${BASE_DIR}"/resources/cert/
    local passout
    local passout2
    openssl rand -writerand ~/.rnd
    read -srp "Enter pass phrase for ca.key:" passout
    echo ""
    if [ "${#passout}" -lt 6 ]; then
        log_error "The CA certificate is generated failed"
        return 1
    fi
    read -srp "Verifying - Enter pass phrase for ca.key:" passout2
    echo ""
    if [ "${passout}" = "${passout2}" ]; then
        openssl genrsa -passout pass:"${passout2}" -aes256 -out "${BASE_DIR}"/resources/cert/ca.key 4096 2>/dev/null &&
            openssl req -new -key "${BASE_DIR}"/resources/cert/ca.key -subj "${subject}" -out ca.csr -passin pass:"${passout2}" &&
            openssl x509 -req -in ca.csr -signkey "${BASE_DIR}"/resources/cert/ca.key -days 3650 -extfile openssl.cnf -extensions v3_ca -out "${BASE_DIR}"/resources/cert/ca.pem -passin pass:"${passout2}" 2>/dev/null
        local result_status=$?
        if [ $result_status -ne 0 ]; then
            log_error "The CA certificate is generated failed"
            return 1
        fi
        echo "The CA certificate is generated successfully"
    else
        log_error "The CA certificate is generated failed"
        return 1
    fi
}

function zip_extract() {
    zip_list=$(find "${BASE_DIR}"/resources -name "*.zip")
    rm -rf "${BASE_DIR}"/resources/fuse_*
    for zip_file in $zip_list; do
        if [[ $zip_file =~ x86_64.zip ]]; then
            unzip -q "$zip_file" -d "${BASE_DIR}"/resources/fuse_and_docker_x86_64
            rm -f "$zip_file"
        fi
        if [[ $zip_file =~ aarch64.zip ]]; then
            unzip -q "$zip_file" -d "${BASE_DIR}"/resources/fuse_and_docker_aarch64
            rm -f "$zip_file"
        fi
    done
}

function download_haveged_and_docker() {
    if ! python3 download.py; then
        return 1
    fi
    tar -xf "${BASE_DIR}"/resources/fuse_and_docker_x86_64/docker* -C "${BASE_DIR}"/resources/fuse_and_docker_x86_64/
    rm -f "${BASE_DIR}"/resources/fuse_and_docker_x86_64/docker*.tgz
    tar -xf "${BASE_DIR}"/resources/fuse_and_docker_aarch64/docker* -C "${BASE_DIR}"/resources/fuse_and_docker_aarch64/
    rm -f "${BASE_DIR}"/resources/fuse_and_docker_aarch64/docker*.tgz
    cp "${BASE_DIR}"/docker.service "${BASE_DIR}"/resources/
}

function process_deploy() {
    if [ -z "${aivault_ip}" ] || [ -z "${aivault_port}" ] || [ -z "${cfs_port}" ] || [ -z "${cert_op_param}" ] || [ -z "${subject}" ] || [ -z "${python_dir}" ]; then
        log_error "parameter error"
        print_usage
        return 1
    fi
    zip_extract
    if ! download_haveged_and_docker; then
        log_error "download files failed"
        return 1
    fi
    if ! generate_ca_cert; then
        return 1
    fi
    local deploy_play
    deploy_play=${BASE_DIR}/playbooks/deploy.yml
    echo "ansible-playbook -i ./inventory_file playbooks/deploy.yml -e hosts_name=ascend -e aivault_ip=${aivault_ip} -e aivault_port=${aivault_port} -e cfs_port=${cfs_port} -e cert_op_param=${cert_op_param} ${DEBUG_CMD}"
    ansible-playbook -i "${BASE_DIR}"/inventory_file "${deploy_play}" -e hosts_name=ascend -e aivault_ip="${aivault_ip}" -e aivault_port="${aivault_port}" -e cfs_port="${cfs_port}" -e cert_op_param="${cert_op_param}" ${DEBUG_CMD}
}

function process_check() {
    local check_play
    check_play=${BASE_DIR}/playbooks/check.yml
    echo "ansible-playbook -i ./inventory_file playbooks/check.yml -e hosts_name=ascend ${DEBUG_CMD}"
    ansible-playbook -i "${BASE_DIR}"/inventory_file "${check_play}" -e hosts_name=ascend ${DEBUG_CMD}
}

function process_modify() {
    local modify_play
    modify_play=${BASE_DIR}/playbooks/modify.yml
    echo "ansible-playbook -i ./inventory_file playbooks/modify.yml -e hosts_name=ascend ${DEBUG_CMD}"
    ansible-playbook -i "${BASE_DIR}"/inventory_file "${modify_play}" -e hosts_name=ascend ${DEBUG_CMD}
}

function print_usage() {
    echo "Usage: ./kmsagent.sh <option> [args]"
    echo ""
    echo "options:"
    echo "-h, --help              show this help message and exit"
    echo "--aivault-ip            specify the IP address of aivault"
    echo "--aivault-port          specify the port of aivault"
    echo "--cfs-port              specify the port of cfs"
    echo "--cert-op-param         parameter for the user info"
    echo "                        example: 'yanfabu|chengdu|sichuan|Huawei|CN'"
    echo "--check                 check time on all environments"
    echo "--modify                modify the time on the remote environments"
    echo "--python-dir            Specify a directory with Python version greater than or equal to 3.7,default is /usr/local/python3.7.5"
    echo "                        example: /usr/local/python3.7.5 or /usr/local/python3.7.5/"
    echo "--subject               set CA request subject"
    echo "                        example: '/CN=Example Root CA'"
    echo "--verbose               print verbose"
    echo ""
    echo "e.g., ./kmsagent.sh --aivault-ip={ip} --aivault-port={port} --cfs-port={port} --cert-op-param={param} --subject={param} --python-dir={python_dir}"
}

DEBUG_CMD=""
python_dir="/usr/local/python3.7.5"

function parse_script_args() {
    if [ $# = 0 ]; then
        print_usage
        return 6
    fi
    local all_para_len
    all_para_len="$*"
    if [[ ${#all_para_len} -gt 1024 ]]; then
        log_error "The total length of the parameter is too long"
        return 1
    fi
    while true; do
        case "$1" in
        --help | -h)
            print_usage
            return 6
            ;;
        --aivault-ip=*)
            aivault_ip=$(echo "$1" | cut -d"=" -f2)
            if [ "$(echo "${aivault_ip}" | grep -cEv '^[0-9.]*$')" -ne 0 ] || [ "$(echo "${aivault_ip}" | grep -cE '^*\.$')" -ne 0 ] || [ "$(echo "${aivault_ip}" | grep -cvE '^((25[0-5]|(2[0-4]|1[0-9]|[1-9]|)[0-9])\.?){4}$')" -ne 0 ]; then
                log_error "The input vaule of [aivault-ip] is invalid, and value needs valid IPv4 address."
                print_usage
                return 1
            fi
            shift
            ;;
        --aivault-port=*)
            aivault_port=$(echo "$1" | cut -d"=" -f2)
            if [ "$(echo "${aivault_port}" | grep -cEv '^[0-9]*$')" -ne 0 ] || [ "${aivault_port}" -lt 1024 ] || [ "${aivault_port}" -gt 65535 ]; then
                log_error "The input value of [aivault-port] is invalid, and value from 1024 to 65535 is available."
                print_usage
                return 1
            fi
            shift
            ;;
        --cfs-port=*)
            cfs_port=$(echo "$1" | cut -d"=" -f2)
            if [ "$(echo "${cfs_port}" | grep -cEv '^[0-9]*$')" -ne 0 ] || [ "${cfs_port}" -lt 1024 ] || [ "${cfs_port}" -gt 65535 ]; then
                log_error "The input value of [cfs-port] is invalid, and value from 1024 to 65535 is available."
                print_usage
                return 1
            fi
            shift
            ;;
        --cert-op-param=*)
            cert_op_param=$(echo "$1" | cut -d"=" -f2)
            shift
            ;;
        --subject=*)
            subject=$(echo "$1" | cut -c11-)
            shift
            ;;
        --python-dir=*)
            python_dir=$(echo "$1" | cut -d"=" -f2)
            if [ "${python_dir: -1}" = / ]; then
                python_dir="${python_dir%?}"
            fi
            shift
            ;;
        --check)
            check_flag=y
            shift
            ;;
        --modify)
            modify_flag=y
            shift
            ;;
        --verbose)
            DEBUG_CMD="-v"
            shift
            ;;
        *)
            if [ "$1" != "" ]; then
                log_error "Unsupported parameters: $1"
                print_usage
                return 1
            fi
            break
            ;;
        esac
    done

    if [ -z "${python_dir}" ]; then
        log_error "parameter error"
        print_usage
        return 1
    fi
}

main() {
    check_log "${BASE_DIR}"/kmsagent.log
    check_log "${BASE_DIR}"/kmsagent_operation.log
    set_permission
    parse_script_args "$@"
    local parse_script_args_status=$?
    if [[ ${parse_script_args_status} != 0 ]]; then
        return ${parse_script_args_status}
    fi
    check_inventory
    local check_inventory_status=$?
    if [[ ${check_inventory_status} != 0 ]]; then
        return ${check_inventory_status}
    fi
    bootstrap
    local bootstrap_status=$?
    if [ ${bootstrap_status} != 0 ]; then
        return ${bootstrap_status}
    fi
    if [ "${check_flag}" = "y" ]; then
        process_check
        local process_check_status=$?
        if [ ${process_check_status} != 0 ]; then
            return ${process_check_status}
        fi
    fi
    if [ "${modify_flag}" = "y" ]; then
        process_modify
        local process_modify_status=$?
        if [ ${process_modify_status} != 0 ]; then
            return ${process_modify_status}
        fi
    fi
    if [ -n "${aivault_ip}" ]; then
        process_deploy
        local process_deploy_status=$?
        if [ ${process_deploy_status} != 0 ]; then
            return ${process_deploy_status}
        fi
    fi
}

main "$@"
main_status=$?
if [[ ${main_status} != 0 ]] && [[ ${main_status} != 6 ]]; then
    operation_log_info "parameter error,run failed"
else
    operation_log_info "$0 $*:Success"
fi
exit ${main_status}
