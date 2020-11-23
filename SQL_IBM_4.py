    #1 Connect to the database

%load_ext sql
# Enter the connection string for your Db2 on Cloud database instance below
# %sql ibm_db_sa://my-username:my-password@my-hostname:my-port/my-db-name
%sql ibm_db_sa://
# type in your query to retrieve list of all tables in the database for your db2 schema (username)
#In Db2 the system catalog table called SYSCAT.TABLES contains the table metadata
%sql select TABSCHEMA, TABNAME, CREATE_TIME from SYSCAT.TABLES where TABSCHEMA='YOUR-DB2-USERNAME'
#or, you can retrieve list of all tables where the schema name is not one of the system created ones:
%sql select TABSCHEMA, TABNAME, CREATE_TIME from SYSCAT.TABLES \
      where TABSCHEMA not in ('SYSIBM', 'SYSCAT', 'SYSSTAT', 'SYSIBMADM', 'SYSTOOLS', 'SYSPUBLIC')
#or, just query for a specifc table that you want to verify exists in the database
%sql select * from SYSCAT.TABLES where TABNAME = 'SCHOOLS'

    #2 Query the database system catalog to retrieve column metadata

# type in your query to retrieve the number of columns in the SCHOOLS table
# In Db2 the system catalog table called SYSCAT.COLUMNS contains the column metadata
%sql select count(*) from SYSCAT.COLUMNS where TABNAME = 'SCHOOLS'
#Now retrieve the the list of columns in SCHOOLS table and their column type (datatype) and length.
# type in your query to retrieve all column names in the SCHOOLS table along with their datatypes and length
%sql select COLNAME, TYPENAME, LENGTH from SYSCAT.COLUMNS where TABNAME = 'SCHOOLS'
#or
%sql select distinct(NAME), COLTYPE, LENGTH from SYSIBM.SYSCOLUMNS where TBNAME = 'SCHOOLS'

    #3 How many Elementary Schools are in the dataset?

#Which column specifies the school type e.g. 'ES', 'MS', 'HS'?
#Does the column name have mixed case, spaces or other special characters?
# If so, ensure you use double quotes around the "Name of the Column"
%sql select count(*) from SCHOOLS where "Elementary, Middle, or High School" = 'ES'

    #4 What is the highest Safety Score?

%sql select MAX(Safety_Score) AS MAX_SAFETY_SCORE from SCHOOLS

    #5 Which schools have highest Safety Score?

#In the previous problem we found out that the highest Safety Score is 99, so we can use that as an input in the where clause:
%sql select Name_of_School, Safety_Score from SCHOOLS where Safety_Score = 99
#or, a better way:
%sql select Name_of_School, Safety_Score from SCHOOLS where Safety_Score= (select MAX(Safety_Score) from SCHOOLS)

    #6 What are the top 10 schools with the highest "Average Student Attendance"?

%sql select Name_of_School, Average_Student_Attendance from SCHOOLS \
    order by Average_Student_Attendance desc nulls last limit 10

    #7 Retrieve the list of 5 Schools with the lowest Average Student Attendance sorted in ascending order based on attendance

%sql SELECT Name_of_School, Average_Student_Attendance  \
     from SCHOOLS \
     order by Average_Student_Attendance \
     fetch first 5 rows only

     #8 Now remove the '%' sign from the above result set for Average Student Attendance column

#Use the REPLACE() function to replace '%' with ''
#See documentation for this function at:
#https://www.ibm.com/support/knowledgecenter/en/SSEPGG_10.5.0/com.ibm.db2.luw.sql.ref.doc/doc/r0000843.html
%sql SELECT Name_of_School, REPLACE(Average_Student_Attendance, '%', '') \
     from SCHOOLS \
     order by Average_Student_Attendance \
     fetch first 5 rows only

     #9 Which Schools have Average Student Attendance lower than 70%?

#The datatype of the "Average_Student_Attendance" column is varchar.
#So you cannot use it as is in the where clause for a numeric comparison.
#First use the CAST() function to cast it as a DECIMAL or DOUBLE
#e.g. CAST("Column_Name" as DOUBLE)
#or simply: DECIMAL("Column_Name")
#Don't forget the '%' age sign needs to be removed before casting
%sql SELECT Name_of_School, Average_Student_Attendance  \
     from SCHOOLS \
     where CAST ( REPLACE(Average_Student_Attendance, '%', '') AS DOUBLE ) < 70 \
     order by Average_Student_Attendance
#or,
%sql SELECT Name_of_School, Average_Student_Attendance  \
     from SCHOOLS \
     where DECIMAL ( REPLACE(Average_Student_Attendance, '%', '') ) < 70 \
     order by Average_Student_Attendance

     #10 Get the total College Enrollment for each Community Area

#Verify the exact name of the Enrollment column in the database
#Use the SUM() function to add up the Enrollments for each Community Area
#Don't forget to group by the Community Area
%sql select Community_Area_Name, sum(College_Enrollment) AS TOTAL_ENROLLMENT \
   from SCHOOLS \
   group by Community_Area_Name

   #11 Get the 5 Community Areas with the least total College Enrollment sorted in ascending order

#Order the previous query and limit the number of rows you fetch
%sql select Community_Area_Name, sum(College_Enrollment) AS TOTAL_ENROLLMENT \
   from SCHOOLS \
   group by Community_Area_Name \
   order by TOTAL_ENROLLMENT asc \
   fetch first 5 rows only

   #12 Get the hardship index for the community area which has College Enrollment of 4638

#NOTE: For this solution to work the CHICAGO_SOCIOECONOMIC_DATA table as created in the last lab of Week 3 should already exist
%%sql
select hardship_index
   from chicago_socioeconomic_data CD, schools CPS
   where CD.ca = CPS.community_area_number
      and college_enrollment = 4368

      #13 Get the hardship index for the community area which has the highest value for College Enrollment
#NOTE: For this solution to work the CHICAGO_SOCIOECONOMIC_DATA table as created in the last lab of Week 3 should already exist
%sql select ca, community_area_name, hardship_index from chicago_socioeconomic_data \
   where ca in \
   ( select community_area_number from schools order by college_enrollment desc limit 1 )
