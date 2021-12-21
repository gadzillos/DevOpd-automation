# This Dockerfile based on CentOS 7 and provide basic postgresql 12 server
# docker-systemctl-replacement - https://github.com/gdraheim/docker-systemctl-replacement
# CMD is required to load postgresql-12.service | otherwise use custom startup.sh
# to manually enable service. This Dcokerfile doesn't create Postgres role and database.

FROM centos:7.9.2009

# update system
#RUN yum -y update

# install python
RUN yum install -y python3 sudo

# Install the repository RPM:
RUN yum install -y https://download.postgresql.org/pub/repos/yum/reporpms/EL-7-x86_64/pgdg-redhat-repo-latest.noarch.rpm

# Install PostgreSQL:
RUN yum install -y postgresql12-server postgresql12-contrib 

# Enable postgresql-12.service startup
RUN systemctl enable postgresql-12.service

# Add systemctl support through script
COPY systemctl.py /usr/bin/systemctl
RUN chmod a+x /usr/bin/systemctl

# Add startup script
COPY startup.sh /opt/
RUN chmod a+x /opt/startup.sh

# Initialize a new database cluster
RUN /usr/pgsql-12/bin/postgresql-12-setup initdb

RUN cd /opt && ./startup.sh

# Run the rest of the commands as the ``postgres`` user created by the ``postgresql12-server``
USER postgres

# Adjust PostgreSQL configuration so that remote connections to the
# database are possible.
RUN echo "host all  all    0.0.0.0/0  md5" >> /var/lib/pgsql/12/data/pg_hba.conf

# And add ``listen_addresses`` to ``/etc/postgresql/12/main/postgresql.conf``
RUN echo "listen_addresses='*'" >> /var/lib/pgsql/12/data/postgresql.conf

# Expose the PostgreSQL port
EXPOSE 5432

# Add VOLUMEs to allow backup of config, logs and databases
VOLUME  ["/etc/postgresql", "/var/log/postgresql", "/var/lib/postgresql"]

# Set the default command to run when starting the container
# loads postgresql-12.service
CMD /usr/bin/systemctl