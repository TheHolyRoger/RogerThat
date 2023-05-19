docker_compose_bin=""
docker_compose_version="0.0"
docker_version="0.0"
docker_compose_cmd=$(docker-compose --version 2>/dev/null)
docker_cmd=$(docker compose version)
if [ "${docker_compose_cmd} " != " " ]; then
    docker_compose_version_str=$(echo "$docker_compose_cmd" | awk '{split($0,a,"version "); print a[2]}' | awk '{split($0,a,","); print a[1]}')
    if [ "${docker_compose_version_str} " != " " ]; then
        docker_compose_version=$(echo "$docker_compose_version_str" | awk '{split($0,a,"."); print a[1]"."a[2]}' | tr -d v)
    fi
fi

if [ "${docker_cmd} " != " " ]; then
    docker_version_str=$(echo "$docker_cmd" | awk '{split($0,a,"version "); print a[2]}')
    if [ "${docker_version_str} " != " " ]; then
        if [[ "${docker_version_str}" != *"is not a docker command"* ]]; then
            docker_version=$(echo "$docker_version_str" | awk '{split($0,a,"."); print a[1]"."a[2]}' | tr -d v)
        fi
    fi
fi


compare_str="${docker_compose_version} > ${docker_version}"

compare_ver=$(bc -l <<<"${compare_str}" 2>/dev/null)

if [ "$compare_ver" == "1" ]; then
    docker_compose_bin=$(which docker-compose)
else
    docker_compose_bin="$(which docker) compose"
fi

echo "$docker_compose_bin"
