# Install custom PostgreSQL

FROM centos:7.9.2009

# update system
RUN yum -y update

# install python
RUN yum install -y python3
#RUN alternatives --set python /usr/bin/python3

# Install the repository RPM:
RUN yum install -y https://download.postgresql.org/pub/repos/yum/reporpms/EL-7-x86_64/pgdg-redhat-repo-latest.noarch.rpm

# Install PostgreSQL:
RUN yum install -y postgresql14-server postgresql14-contrib 

# initialize the database and enable automatic start:
#RUN /usr/pgsql-14/bin/postgresql-14-setup initdb
#RUN systemctl enable postgresql-14
#RUN systemctl start postgresql-14

# Run the rest of the commands as the ``postgres`` user created by the ``postgresql14-server``
USER postgres

RUN  postgresql-14-setup --initdb
# Create a PostgreSQL role named ``docker`` with ``docker`` as the password and
# then create a database `docker` owned by the ``docker`` role.
RUN    /etc/init.d/postgresql start &&\
    psql --command "CREATE USER docker WITH SUPERUSER PASSWORD 'docker';" &&\
    createdb -O docker docker

# Adjust PostgreSQL configuration so that remote connections to the
# database are possible.
RUN echo "host all  all    0.0.0.0/0  md5" >> /etc/postgresql/14/main/pg_hba.conf


# And add ``listen_addresses`` to ``/etc/postgresql/14/main/postgresql.conf``
RUN echo "listen_addresses='*'" >> /etc/postgresql/14/main/postgresql.conf

# Expose the PostgreSQL port
EXPOSE 5432

# Add VOLUMEs to allow backup of config, logs and databases
VOLUME  ["/etc/postgresql", "/var/log/postgresql", "/var/lib/postgresql"]

# Set the default command to run when starting the container
CMD ["/usr/lib/postgresql/14/bin/postgres", "-D", "/var/lib/postgresql/14/main", "-c", "config_file=/etc/postgresql/14/main/postgresql.conf"]
