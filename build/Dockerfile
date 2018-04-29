FROM lambci/lambda:build-python2.7
RUN yum install -y mysql-devel
RUN yum install -y MySQL-python
RUN cp /usr/lib64/mysql/libmysqlclient.so.18.0.0 ./libmysqlclient.so.18