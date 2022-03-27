echo "Configuring postgres"
# create temporary directory for postgres in docker
mkdir -p /tmp 

# copy your postgresql.conf to postgresql config location in docker
cp /db_config.conf /var/lib/postgresql/data/postgresql.conf

echo "Done configuring."
