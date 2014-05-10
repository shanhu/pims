/*==============================================================*/
/* DBMS name:      MySQL 5.0                                    */
/* Created on:     2014/5/10 18:52:59                           */
/*==============================================================*/


drop table if exists pims.attendance;

drop table if exists pims.card;

drop table if exists pims.employee;

drop table if exists pims.material;

drop table if exists pims.material_type;

drop table if exists pims.process;

drop table if exists pims.production;

drop table if exists pims.report_class;

drop table if exists pims.report_employee;

drop table if exists pims.salary_count_config;

drop table if exists pims.salary_time_config;

drop table if exists pims.terminal;

drop table if exists pims.workclass;

drop table if exists pims.workgroup;

drop table if exists pims.workshift;

drop table if exists pims.workshop;

/*==============================================================*/
/* User: pims                                                   */
/*==============================================================*/
create user pims;

/*==============================================================*/
/* Table: attendance                                            */
/*==============================================================*/
create table pims.attendance
(
   ID                   int(11) not null,
   TERMINAL_ID          int(11) not null,
   EMPLOYEE_ID          int(11) not null,
   CARD_ID              int(11) not null,
   TIME                 datetime not null,
   primary key (ID)
);

/*==============================================================*/
/* Table: card                                                  */
/*==============================================================*/
create table pims.card
(
   ID                   int(11) not null auto_increment,
   NUM                  national varchar(20) not null,
   SERIAL_NUM           int(11) not null,
   TYPE                 varchar(1) not null,
   OWNER_ID             int(11),
   STATUS               national varchar(1) not null,
   REMARKS              national varchar(200),
   primary key (ID),
   key SERIAL_NUM (SERIAL_NUM)
);

/*==============================================================*/
/* Table: employee                                              */
/*==============================================================*/
create table pims.employee
(
   ID                   int(11) not null auto_increment,
   NUM                  national varchar(20) not null,
   NAME                 national varchar(20) not null,
   SEX                  national varchar(1) not null,
   IDCARD               national varchar(20) not null,
   TEL                  national varchar(20),
   JOIN_TIME            datetime not null,
   TYPE                 national varchar(1) not null,
   STATUS               national varchar(1) not null,
   CARD_NUM1            national varchar(20),
   CARD_NUM2            national varchar(20),
   REMARKS              national varchar(200),
   primary key (ID)
);

/*==============================================================*/
/* Table: material                                              */
/*==============================================================*/
create table pims.material
(
   ID                   int(11) not null auto_increment,
   NUM                  national varchar(20) not null,
   NAME                 national varchar(20) not null,
   MATERIAL_TYPE_ID     int(11) not null,
   STATUS               national varchar(1) not null,
   CARD_NUM             national varchar(20),
   REMARKS              national varchar(200),
   primary key (ID)
);

/*==============================================================*/
/* Table: material_type                                         */
/*==============================================================*/
create table pims.material_type
(
   ID                   int(11) not null auto_increment,
   NUM                  national varchar(20) not null,
   NAME                 varchar(20) not null,
   STATUS               national varchar(1) not null,
   PARENT_ID            int(11),
   primary key (ID)
);

/*==============================================================*/
/* Table: process                                               */
/*==============================================================*/
create table pims.process
(
   ID                   int(11) not null auto_increment,
   NUM                  national varchar(20) not null,
   NAME                 national varchar(20) not null,
   FIRST_PROCESS_ID     int(11),
   IS_FIRST             national varchar(1) not null,
   MODE                 varchar(1) not null,
   UNIT                 varchar(20),
   STATUS               national varchar(1) not null,
   CARD_NUM             national varchar(20),
   REMARKS              national varchar(200),
   primary key (ID)
);

/*==============================================================*/
/* Table: production                                            */
/*==============================================================*/
create table pims.production
(
   ID                   int(11) not null auto_increment,
   TERMINAL_ID          int(11) not null,
   CARD_ID              int(11) not null,
   EMPLOYEE_ID          int(11) not null,
   MATERIAL_ID          int(11) not null,
   PROCESS_ID           int(11) not null,
   TIME                 datetime not null,
   COUNT                decimal(10,2) not null,
   primary key (ID)
);

/*==============================================================*/
/* Table: report_class                                          */
/*==============================================================*/
create table pims.report_class
(
   ID                   int(11) not null,
   STARTTIME            datetime not null,
   ENDTIME              datetime not null,
   MATERIAL_ID          int(11) not null,
   PROCESS_FIRST_ID     int(11),
   GET_COUNT            decimal(10,2),
   PROCESS_LAST_ID      int(11) not null,
   PUT_COUNT            decimal(10,2) not null,
   AVERAGE_RATE         decimal(10,2) not null,
   primary key (ID)
);

/*==============================================================*/
/* Table: report_employee                                       */
/*==============================================================*/
create table pims.report_employee
(
   ID                   int(11) not null,
   STARTTIME            datetime not null,
   ENDTIME              datetime not null,
   EMPLOYEE_ID          int(11) not null,
   MATERIAL_ID          int(11) not null,
   PROCESS_FIRST_ID     int(11),
   GET_COUNT            decimal(10,2),
   PROCESS_LAST_ID      int(11) not null,
   PUT_COUNT            decimal(10,2) not null,
   AVERAGE_RATE         decimal(10,2) not null,
   primary key (ID)
);

/*==============================================================*/
/* Table: salary_count_config                                   */
/*==============================================================*/
create table pims.salary_count_config
(
   ID                   int(11) not null auto_increment,
   MATERIAL_ID          int(11) not null,
   PROCESS_ID           int(11) not null,
   PRICE                decimal(10,2) not null,
   REMARKS              national varchar(200),
   primary key (ID)
);

/*==============================================================*/
/* Table: salary_time_config                                    */
/*==============================================================*/
create table pims.salary_time_config
(
   ID                   int(11) not null auto_increment,
   PRICE                decimal(10,2) not null,
   REMARKS              varchar(200),
   primary key (ID)
);

/*==============================================================*/
/* Table: terminal                                              */
/*==============================================================*/
create table pims.terminal
(
   ID                   int(11) not null auto_increment,
   NUM                  national varchar(20) not null,
   NAME                 national varchar(20) not null,
   TYPE                 national varchar(1) not null,
   WORKGROUP_ID         int(11) not null,
   IP1                  national varchar(20) not null,
   IP2                  national varchar(20),
   REMARKS              national varchar(200),
   DEFAULT_MATERIAL_ID  int(11),
   DEFAULT_PROCESS_ID   int(11),
   primary key (ID)
);

/*==============================================================*/
/* Table: workclass                                             */
/*==============================================================*/
create table pims.workclass
(
   ID                   int(11) not null auto_increment,
   NUM                  national varchar(20) not null,
   NAME                 national varchar(20) not null,
   TYPE                 national varchar(1) not null,
   STATUS               national varchar(1) not null,
   CARD_NUM             national varchar(20),
   REMARKS              national varchar(200),
   primary key (ID)
);

/*==============================================================*/
/* Table: workgroup                                             */
/*==============================================================*/
create table pims.workgroup
(
   ID                   int(11) not null auto_increment,
   NAME                 national varchar(20) not null,
   REMARKS              national varchar(200),
   WORKSHOP_ID          int(11) not null,
   primary key (ID)
);

/*==============================================================*/
/* Table: workshift                                             */
/*==============================================================*/
create table pims.workshift
(
   ID                   int(11) not null,
   TERMINAL_ID          int(11) not null,
   CARD_ID              int(11) not null,
   TIME                 datetime not null,
   primary key (ID)
);

/*==============================================================*/
/* Table: workshop                                              */
/*==============================================================*/
create table pims.workshop
(
   ID                   int(11) not null auto_increment,
   NAME                 national varchar(20) not null,
   REMARKS              national varchar(200),
   primary key (ID)
);

alter table pims.attendance add constraint FK_Reference_19 foreign key (TERMINAL_ID)
      references pims.terminal (ID) on delete restrict on update restrict;

alter table pims.attendance add constraint FK_Reference_25 foreign key (EMPLOYEE_ID)
      references pims.employee (ID) on delete restrict on update restrict;

alter table pims.attendance add constraint FK_Reference_33 foreign key (CARD_ID)
      references pims.card (ID) on delete restrict on update restrict;

alter table pims.material add constraint MATERIAL_TYPE_ID_refs_ID_7fb616e2 foreign key (MATERIAL_TYPE_ID)
      references pims.material_type (ID);

alter table pims.material_type add constraint PARENT_ID_refs_ID_06b0f457 foreign key (PARENT_ID)
      references pims.material_type (ID);

alter table pims.process add constraint FIRST_PROCESS_ID_refs_ID_21876686 foreign key (FIRST_PROCESS_ID)
      references pims.process (ID);

alter table pims.production add constraint FK_Reference_20 foreign key (CARD_ID)
      references pims.card (ID) on delete restrict on update restrict;

alter table pims.production add constraint FK_Reference_21 foreign key (EMPLOYEE_ID)
      references pims.employee (ID) on delete restrict on update restrict;

alter table pims.production add constraint FK_Reference_22 foreign key (TERMINAL_ID)
      references pims.terminal (ID) on delete restrict on update restrict;

alter table pims.production add constraint FK_Reference_23 foreign key (MATERIAL_ID)
      references pims.material (ID) on delete restrict on update restrict;

alter table pims.production add constraint FK_Reference_24 foreign key (PROCESS_ID)
      references pims.process (ID) on delete restrict on update restrict;

alter table pims.report_class add constraint FK_Reference_30 foreign key (MATERIAL_ID)
      references pims.material (ID) on delete restrict on update restrict;

alter table pims.report_class add constraint FK_Reference_31 foreign key (PROCESS_FIRST_ID)
      references pims.process (ID) on delete restrict on update restrict;

alter table pims.report_class add constraint FK_Reference_32 foreign key (PROCESS_LAST_ID)
      references pims.process (ID) on delete restrict on update restrict;

alter table pims.report_employee add constraint FK_Reference_26 foreign key (MATERIAL_ID)
      references pims.material (ID) on delete restrict on update restrict;

alter table pims.report_employee add constraint FK_Reference_27 foreign key (PROCESS_FIRST_ID)
      references pims.process (ID) on delete restrict on update restrict;

alter table pims.report_employee add constraint FK_Reference_28 foreign key (PROCESS_LAST_ID)
      references pims.process (ID) on delete restrict on update restrict;

alter table pims.report_employee add constraint FK_Reference_29 foreign key (EMPLOYEE_ID)
      references pims.employee (ID) on delete restrict on update restrict;

alter table pims.salary_count_config add constraint MATERIAL_ID_refs_ID_fe6621a2 foreign key (MATERIAL_ID)
      references pims.material (ID);

alter table pims.salary_count_config add constraint PROCESS_ID_refs_ID_ec5e2c1d foreign key (PROCESS_ID)
      references pims.process (ID);

alter table pims.terminal add constraint DEFAULT_MATERIAL_ID_refs_ID_9b2a4116 foreign key (DEFAULT_MATERIAL_ID)
      references pims.material (ID);

alter table pims.terminal add constraint DEFAULT_PROCESS_ID_refs_ID_cc1d86de foreign key (DEFAULT_PROCESS_ID)
      references pims.process (ID);

alter table pims.terminal add constraint WORKGROUP_ID_refs_ID_23839f25 foreign key (WORKGROUP_ID)
      references pims.workgroup (ID);

alter table pims.workgroup add constraint WORKSHOP_ID_refs_ID_3cd5cf8b foreign key (WORKSHOP_ID)
      references pims.workshop (ID);

alter table pims.workshift add constraint FK_Reference_16 foreign key (TERMINAL_ID)
      references pims.terminal (ID) on delete restrict on update restrict;

alter table pims.workshift add constraint FK_Reference_17 foreign key (CARD_ID)
      references pims.card (ID) on delete restrict on update restrict;

