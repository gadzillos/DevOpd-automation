# This Dockerfile based on CentOS 7 and provide basic postgresql 14 server
# docker-systemctl-replacement - https://github.com/gdraheim/docker-systemctl-replacement
# CMD is required to load postgresql-14.service | otherwise use custom startup.sh
# to manually enable service. This Dcokerfile doesn't create Postgres role and database.

FROM centos:7.9.2009

# update system
#RUN yum -y update

# install python
RUN yum install -y python3 sudo

# Install the repository RPM:
RUN yum install -y https://download.postgresql.org/pub/repos/yum/reporpms/EL-7-x86_64/pgdg-redhat-repo-latest.noarch.rpm

# Install PostgreSQL:
RUN yum install -y postgresql14-server postgresql14-contrib 

# Enable postgresql-14.service startup
RUN systemctl enable postgresql-14.service

# Add systemctl support through script
#COPY systemctl.py /usr/bin/systemctl
#RUN chmod a+x /usr/bin/systemctl

# Add startup script
COPY startup.sh /opt/
RUN chmod a+x /opt/startup.sh

# Initialize a new database cluster
RUN /usr/pgsql-14/bin/postgresql-14-setup initdb

# Run the rest of the commands as the ``postgres`` user created by the ``postgresql14-server``
USER postgres

# Adjust PostgreSQL configuration so that remote connections to the
# database are possible.
RUN echo "host all  all    0.0.0.0/0  md5" >> /var/lib/pgsql/14/data/pg_hba.conf

# And add ``listen_addresses`` to ``/etc/postgresql/14/main/postgresql.conf``
RUN echo "listen_addresses='*'" >> /var/lib/pgsql/14/data/postgresql.conf

# Expose the PostgreSQL port
EXPOSE 5432

# Add VOLUMEs to allow backup of config, logs and databases
VOLUME  ["/etc/postgresql", "/var/log/postgresql", "/var/lib/postgresql"]

# Set the default command to run when starting the container
# loads postgresql-14.service
CMD /opt/startup.sh